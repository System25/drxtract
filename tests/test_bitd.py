# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

#
# Unit test for BITD extraction
#

import unittest
import os
import json
from parameterized import parameterized

from drxtract.bitd import bitd2bmp
from drxtract.clut import clut2palette


class TestScript(unittest.TestCase):
    
    maxDiff = None
    
    def setUp(self):
        os.chdir(os.path.join(os.path.dirname(__file__), 'files', 'bitd'))
    

    @parameterized.expand([
        ['apple'],
        ['appleInPipe'],
        ['superman'],
        ['line'],
        ['porteus'],
        ['postbox16b'],
        ['postbox24b'],
        
    ])
    def test_bitd_using_system_palette(self, dir_name: str):
        bitd_file = os.path.join(dir_name, dir_name + ".BITD")
        bmp_file = os.path.join(dir_name, dir_name + ".bmp")
        json_file = os.path.join(dir_name, "data.json")
        
        clutData =  bytes()
        
        with open(json_file, mode='rb') as file:
            json_data = file.read().decode('utf-8')
            castData = json.loads(json_data)
        
        with open(bmp_file, mode='rb') as file:
            expected_bmp = file.read()

        with open(bitd_file, mode='rb') as file:
            fdata = file.read()
            
            # Convert BITD to bmp file data
            bmp = bitd2bmp(castData, clutData, fdata)

        #with open(os.path.join(dir_name, "test.bmp"), mode='wb') as file:
        #    file.write(bmp)
        
            self.assertEqual(expected_bmp, bmp)

    @parameterized.expand([
        ['rectangle'],
        ['bars'],
    ])
    def test_bitd_using_custom_palette(self, dir_name: str):
        clut_file = os.path.join(dir_name, dir_name + ".CLUT")
        bitd_file = os.path.join(dir_name, dir_name + ".BITD")
        bmp_file = os.path.join(dir_name, dir_name + ".bmp")
        json_file = os.path.join(dir_name, "data.json")
        
        
        with open(clut_file, mode='rb') as file:
            fdata = file.read()
            clutData = clut2palette(fdata)
        
        with open(json_file, mode='rb') as file:
            json_data = file.read().decode('utf-8')
            castData = json.loads(json_data)
        
        with open(bmp_file, mode='rb') as file:
            expected_bmp = file.read()

        with open(bitd_file, mode='rb') as file:
            fdata = file.read()
            
            # Convert BITD to bmp file data
            bmp = bitd2bmp(castData, clutData, fdata)

        #with open(os.path.join(dir_name, "test.bmp"), mode='wb') as file:
            #file.write(bmp)
        
            self.assertEqual(expected_bmp, bmp)