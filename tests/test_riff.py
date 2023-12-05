# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

#
# Unit test for RIFF extraction
#

import unittest
import os
import re
from parameterized import parameterized

from drxtract.riff.riff import parse_riff, find_riff_in_exe, RiffData, Chunk
from drxtract.riff.imap import InputMAP, parse_imap
from drxtract.riff.mmap import MemoryMAP, parse_mmap
from drxtract.lingosrc.util import vsprintf

MV93_FILE_TYPE = 'MV93'
RIFX_FILE_FORMAT = 'RIFX'
IMAP_FILE_FORMAT = 'imap'
MMAP_FILE_FORMAT = 'mmap'
FREE_FILE_FORMAT = 'free'
JUNK_FILE_FORMAT = 'junk'

CHUNKS_TO_IGNORE = (RIFX_FILE_FORMAT, IMAP_FILE_FORMAT, MMAP_FILE_FORMAT,
                    FREE_FILE_FORMAT, JUNK_FILE_FORMAT)

class TestScript(unittest.TestCase):
    
    maxDiff = None
    
    def setUp(self):
        os.chdir(os.path.join(os.path.dirname(__file__), 'files', 'riff/'))
    
    def compare_chunk(self, chunk: Chunk, number: int, folder: str):
        file_name =  vsprintf("%s.%s", number, chunk.identifier)
        file_name = re.sub(r"[^A-Za-z0-9\-_\.]", "_", file_name)
        
        with open(os.path.join(folder, file_name), 'rb') as file:
            fileContent: bytes = file.read()
            self.assertEqual(fileContent, chunk.data,
                             "Difference in: " + file_name)
    
    def compare_dir(self, byte_order: str, dir_file: str, output_folder: str):
        rifx_offset: int = 0
        with open(dir_file, mode='rb') as file:
            fileContent: bytes = file.read()
            if dir_file.upper().endswith('.EXE'):
                # Try to find DRX header inside the EXE file
                rifx_offset = find_riff_in_exe(fileContent)
            
            riffData: RiffData = parse_riff(fileContent, rifx_offset, byte_order)
            
            # Parse the imap block
            chunk: Chunk = riffData.chunks[0]
            self.assertEqual(IMAP_FILE_FORMAT, chunk.identifier)
            imap: InputMAP = parse_imap(chunk.data, byte_order)
            
            # Get the memory map
            chunk = riffData.get_by_offset(imap.offset - rifx_offset)
            self.assertEqual(MMAP_FILE_FORMAT, chunk.identifier)
            mmap: MemoryMAP = parse_mmap(chunk.data, byte_order)
            idx = -1
            for resource in mmap.resources:
                idx += 1
                if ((resource.chunkID in CHUNKS_TO_IGNORE) or
                    (resource.size <= 0)):
                    continue
                
                offset: int = resource.offset
                chunk = riffData.get_by_offset(offset - rifx_offset)
                self.assertEqual(resource.chunkID, chunk.identifier)

                
                self.compare_chunk(chunk, idx, output_folder)
    
    @parameterized.expand([
        ['>', 'AppleGame'],
        ['<', 'Lorem'],
        
    ])
    def test_riff(self, byte_order: str, dir_name: str):
        dir_file = os.path.join(dir_name, dir_name + ".dir")
        output_folder = os.path.join(dir_name, "files", "bin")
        
        self.compare_dir(byte_order, dir_file, output_folder)

    @parameterized.expand([
        ['Lorem_proj'],
        
    ])
    def test_exe(self, dir_name: str):
        dir_file = os.path.join(dir_name, dir_name + ".exe")
        output_folder = os.path.join(dir_name, "files", "bin")
        
        self.compare_dir('<', dir_file, output_folder)

