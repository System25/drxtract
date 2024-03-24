# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from typing import List, Dict, Any
import logging
from ..vwlb import Marker, parse_vwlb_data
from ..riff import RiffData, parse_riff, InputMAP, MemoryMAP, \
    parse_imap, parse_mmap, Chunk, MMapResource
from ..key import parse_key_file_data
from ..vwcf import parse_vwcf_file_data
from ..cas import parse_cas_file_data
from ..lctx import parse_lctx_file_data, LingoScripReference
from ..cast import parse_cast_file_data
from ..vwsc import parse_vwsc_file_data, vwsc_to_score
from ..stxt import parse_stxt_data, TextData
from ..fmap import parse_fmap_data, FontInfo
from ..snd import snd_to_sampled, SampledSound
from ..bitd import bitd2bmp
from ..clut import clut2palette
from ..lingosrc.ast import Script
from ..lingosrc.parse.lnam import parse_lnam_file_data
from ..lingosrc.parse.lscr import parse_lrcr_file_data
from ..lingosrc.codegen.lingo import generate_lingo_code
from ..lingosrc.codegen.js import generate_js_code


IMAP_FILE_FORMAT = 'imap'
MMAP_FILE_FORMAT = 'mmap'


#
# DirectorFile class.
# 
# =============================================================================
class DirectorFile:
    """This class represents the content of a director file"""
    
    def __init__(self, info: Dict[str, Any], cast: List[Dict[str, Any]],
                 lingoScr: Dict[int, str], jsScr: Dict[int, str],
                 markers: List[Marker], score: Dict[str, Any]):
        self.info = info
        self.cast = cast
        self.lingoScr = lingoScr
        self.jsScr = jsScr
        self.markers = markers
        self.score = score

#
# Check if a chunk exists in the MMap resources list by its chunk ID.
# =============================================================================
def exists_chunk(resources: List[MMapResource], chunkId: str) -> bool:
    """
    Checks if a chunk exists by its chunk ID in the resources list.
    
    Parameters
    ----------
    resources : List[MMapResource]
        List of MMapResources
    chunkId: str
        Chunk ID.
        
    Returns
    -------
    bool
        True if the chunk exists.
    """
    
    for resource in resources:
        if resource.chunkID == chunkId:
            return True
    
    return False
    

#
# Locate a chunk in the MMap resources list by its chunk ID.
# =============================================================================
def locate_chunk(resources: List[MMapResource], chunkId: str) -> MMapResource:
    """
    Locates a chunk by its chunk ID in the resources list.
    
    Parameters
    ----------
    resources : List[MMapResource]
        List of MMapResources
    chunkId: str
        Chunk ID.
        
    Returns
    -------
    MMapResource
        a resource.

    Raises
    ------
    ValueError
        If some field inside the file is not compliant with the expected
        file structure. 
    """
    
    for resource in resources:
        if resource.chunkID == chunkId:
            return resource
    
    raise ValueError("Couldn't locate the resource with Chunk ID: " + chunkId)
        
#
# Reads all the information from a DIR file
# =============================================================================
def parse_dir_file_data(byte_order: str, rifx_offset, \
                        fdata: bytes) -> DirectorFile:
    """
    Parse a DIR file and return its content.
    
    Parameters
    ----------
    byte_order : str
        Python's struct module byte order.
    rifx_offset: int
        Offset to the begining of the RIFF structure.
    fdata : bytes
        The bytes in the CAS file that contain the casting element index inside
        the Director file.
        
    Returns
    -------
    DirectorFile
        a class that represents a Director file.

    Raises
    ------
    ValueError
        If some field inside the file is not compliant with the expected
        file structure. 
        
    """
    # Parse the RIFF data
    riffData: RiffData = parse_riff(fdata, rifx_offset, byte_order)
    
    # Parse the imap block
    chunk: Chunk = riffData.chunks[0]
    if IMAP_FILE_FORMAT != chunk.identifier:
        raise ValueError("Coudn't locate the IMAP file!")
    
    imap: InputMAP = parse_imap(chunk.data, byte_order)
    
    # Get the memory map
    chunk = riffData.get_by_offset(imap.offset - rifx_offset)
    if MMAP_FILE_FORMAT != chunk.identifier:
        raise ValueError("Coudn't locate the MMAP file!")
    mmap: MemoryMAP = parse_mmap(chunk.data, byte_order)
    
    # Read the KEY chunk
    logging.debug('Parse KEY* chunk')
    res = locate_chunk(mmap.resources, 'KEY*')
    chunk = riffData.get_by_offset(res.offset - rifx_offset)
    key_elements = parse_key_file_data(byte_order, chunk.data)
    
    # Read the VWCF chunk
    logging.debug('Parse VWCF chunk')
    res = locate_chunk(mmap.resources, 'VWCF')
    chunk = riffData.get_by_offset(res.offset - rifx_offset)
    info = parse_vwcf_file_data(chunk.data)
    
    # Read the CAS chunk
    logging.debug('Parse CAS* chunk')
    res = locate_chunk(mmap.resources, 'CAS*')
    chunk = riffData.get_by_offset(res.offset - rifx_offset)
    cas_elements = parse_cas_file_data(chunk.data)
    
    # Read the Lctx chunk (if exists)
    lctx_elements: List[LingoScripReference] = []
    lingoScr: Dict[int, str] = {}
    jsScr: Dict[int, str] = {}
    if exists_chunk(mmap.resources, 'Lctx'):
        logging.debug('Parse Lctx chunk')
        res = locate_chunk(mmap.resources, 'Lctx')
        chunk = riffData.get_by_offset(res.offset - rifx_offset)
        lctx_elements = parse_lctx_file_data(chunk.data)
        
        # Read the Lnam chunk
        name_list: List[str] = []
        if exists_chunk(mmap.resources, 'Lnam'):
            logging.debug('Parse Lnam chunk')
            res = locate_chunk(mmap.resources, 'Lnam')
            chunk = riffData.get_by_offset(res.offset - rifx_offset)
            name_list = parse_lnam_file_data(chunk.data)

        for lscr_ref in lctx_elements:
            # Decompile scripts
            lscr_idx = lscr_ref['index']
            if lscr_idx < 0:
                logging.debug("No script")
                continue
            logging.debug("Decompile script %d", lscr_idx)

            res = mmap.resources[lscr_idx]
            chunk = riffData.get_by_offset(res.offset - rifx_offset)
            lscr:Script = parse_lrcr_file_data(chunk.data, name_list)
            if lscr.cont_scr_num < 0:
                n = lscr.scr_num
                logging.debug("New script: %d", n)
                lingoScr[n] =  generate_lingo_code(lscr)
                jsScr[n] = generate_js_code(lscr)
                
            else:
                n = lscr.cont_scr_num
                logging.debug("Continue a previous script: %d", n)
                lingoScr[n] += "\n" + generate_lingo_code(lscr)
                jsScr[n] += "\n" + generate_js_code(lscr)
            
    
    # Read the VWLB chunk (if exists)
    markers: List[Marker] = []
    if exists_chunk(mmap.resources, 'VWLB'):
        logging.debug('Parse VWLB chunk')
        res = locate_chunk(mmap.resources, 'VWLB')
        chunk = riffData.get_by_offset(res.offset - rifx_offset)
        markers = parse_vwlb_data(chunk.data)
    
    # Read the VWSC chunk (if exists)
    score: Dict[str, Any] = {}
    if exists_chunk(mmap.resources, 'VWSC'):
        logging.debug('Parse VWSC chunk')
        res = locate_chunk(mmap.resources, 'VWSC')
        chunk = riffData.get_by_offset(res.offset - rifx_offset)
        score = vwsc_to_score(parse_vwsc_file_data(chunk.data))
    
    # Read the fontmap (if any)
    fontmap: List[FontInfo] = []
    if exists_chunk(mmap.resources, 'Fmap'):
        logging.debug('Parse Fmap chunk')
        res = locate_chunk(mmap.resources, 'Fmap')
        chunk = riffData.get_by_offset(res.offset - rifx_offset)
        fontmap = parse_fmap_data(chunk.data)
    
    # Read the casting elements
    cast: List[Dict[str, Any]] = []
    for cas_index in cas_elements:
        # Parse CASt chunk data
        res = mmap.resources[cas_index]
        chunk = riffData.get_by_offset(res.offset - rifx_offset)
        castData = parse_cast_file_data(chunk.data)
        
        # Find the related elements
        if cas_index in key_elements:
            kelm = key_elements[cas_index]
            for rf in kelm:
                logging.debug("Related data: %d %s", rf['index'], rf['chunkID'])
                rf_idx = rf['index']
                res = mmap.resources[rf_idx]
                if rf['chunkID'] != res.chunkID:
                    raise ValueError("Chunk ID mismatch!")
                
                chunk = riffData.get_by_offset(res.offset - rifx_offset)
                if res.chunkID == 'STXT':
                    text_data: TextData = parse_stxt_data(chunk.data, fontmap)
                    castData['text'] = text_data['text']
                    castData['txt_format'] = text_data['txt_format']
                    
                elif res.chunkID == 'snd ':
                    snd_data: SampledSound = snd_to_sampled(chunk.data)
                    castData['sampled_sound'] = snd_data
                
                elif res.chunkID == 'CLUT':
                    clutData: bytes = clut2palette(chunk.data)
                    castData['palette'] = clutData
                
                elif res.chunkID == 'THUM':
                    logging.info("Thumnail are ignored!")
                
                elif res.chunkID == 'BITD':
                    clutData = bytes()
                    paletteId = int(castData['palette'])
                    if paletteId > 0:
                        p = paletteId - 1
                        clutData = cast[p]['palette']
                    bmp_data: bytes = bitd2bmp(castData, clutData, chunk.data)
                    castData['bitmap'] = bmp_data
                    
                else:
                    raise ValueError("Unknown related element: " + res.chunkID)
                
             
        
        cast.append(castData)
    
    
    # Return the DirectorFile structure
    return DirectorFile(info, cast, lingoScr, jsScr, markers, score)
    
