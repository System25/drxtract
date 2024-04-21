# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

#
# Unit test for VWCF extraction
#

import unittest
import os
import json
from parameterized import parameterized

from drxtract.vwcf import parse_vwcf_file_data


class TestScript(unittest.TestCase):
    
    maxDiff = None
    
    def setUp(self):
        os.chdir(os.path.join(os.path.dirname(__file__), 'files', 'vwcf'))
    

    @parameterized.expand([
        ['AppleGame'],
        
    ])
    def test_vwcf(self, dir_name: str):
        cas_file = os.path.join(dir_name, dir_name + ".VWCF")
        json_file = os.path.join(dir_name, "config.json")
        
        with open(json_file, mode='rb') as file:
            json_data = file.read().decode('utf-8')
            expectedData = json.loads(json_data)
        
        with open(cas_file, mode='rb') as file:
            fdata = file.read()
            
            # Read the basic file information
            actualData = parse_vwcf_file_data(fdata)
        
            self.assertEqual(expectedData, actualData)

