# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

#
# Unit test for CLUT extraction
#

import unittest
import os
import json
from parameterized import parameterized

from drxtract.clut import clut2rgb


class TestScript(unittest.TestCase):
    
    maxDiff = None
    
    def setUp(self):
        os.chdir(os.path.join(os.path.dirname(__file__), 'files', 'clut'))
    

    @parameterized.expand([
        ['mspaint'],
        
    ])
    def test_clut(self, dir_name: str):
        clut_file = os.path.join(dir_name, dir_name + ".CLUT")
        json_file = os.path.join(dir_name, "data.json")
        
        clutData =  bytes()
        
        with open(json_file, mode='rb') as file:
            json_data = file.read().decode('utf-8')
            castData = json.loads(json_data)
        
        with open(clut_file, mode='rb') as file:
            fdata = file.read()
            
            # Convert CLUT to color list
            colors = clut2rgb(fdata)
        
            self.assertEqual(castData['palette'], colors)

