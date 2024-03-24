# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

#
# Unit test for Fmap extraction
#

import unittest
import os
import json
from parameterized import parameterized

from drxtract.fmap import parse_fmap_data


class TestScript(unittest.TestCase):
    
    maxDiff = None
    
    def setUp(self):
        os.chdir(os.path.join(os.path.dirname(__file__), 'files', 'fmap'))
    

    @parameterized.expand([
        ['test1font'],
        
    ])
    def test_exe(self, dir_name: str):
        fmap_file = os.path.join(dir_name, dir_name + ".Fmap")
        json_file = os.path.join(dir_name, "fonts.json")
        with open(json_file, mode='rb') as file:
            expected_json = file.read().decode('utf-8')

        with open(fmap_file, mode='rb') as file:
            fdata = file.read()
            
            # Parser Fmap file data
            data = parse_fmap_data(fdata)
            actual_json = json.dumps(data, indent=4,sort_keys=True)
            
            self.assertEqual(expected_json, actual_json)


