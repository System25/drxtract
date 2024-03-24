# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

#
# Unit test for KEY extraction
#

import unittest
import os
import json
from parameterized import parameterized

from drxtract.key import parse_key_file_data


class TestScript(unittest.TestCase):
    
    maxDiff = None
    
    def setUp(self):
        os.chdir(os.path.join(os.path.dirname(__file__), 'files', 'key'))
    

    @parameterized.expand([
        ['>', 'AppleGame'],
        
    ])
    def test_key(self, byte_order: str, dir_name: str):
        key_file = os.path.join(dir_name, dir_name + ".KEY_")
        json_file = os.path.join(dir_name, "data.json")
        
        with open(json_file, mode='rb') as file:
            json_data = file.read().decode('utf-8')
        
        with open(key_file, mode='rb') as file:
            fdata = file.read()
            
            # Read the key file data
            actualData = parse_key_file_data(byte_order, fdata)
            
        #with open(os.path.join(dir_name, "test.json"), mode='wb') as file:
        #    file.write(json.dumps(actualData).encode('utf-8'))
        
            self.assertEqual(json_data, json.dumps(actualData))

