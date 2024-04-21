# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

#
# Unit test for CAS extraction
#

import unittest
import os
import json
from parameterized import parameterized

from drxtract.cas import parse_cas_file_data


class TestScript(unittest.TestCase):
    
    maxDiff = None
    
    def setUp(self):
        os.chdir(os.path.join(os.path.dirname(__file__), 'files', 'cas'))
    

    @parameterized.expand([
        ['AppleGame'],
        
    ])
    def test_cas(self, dir_name: str):
        cas_file = os.path.join(dir_name, dir_name + ".CAS_")
        json_file = os.path.join(dir_name, "data.json")
        
        with open(json_file, mode='rb') as file:
            json_data = file.read().decode('utf-8')
            expectedList = json.loads(json_data)
        
        with open(cas_file, mode='rb') as file:
            fdata = file.read()
            
            # Read cast element list
            actualList = parse_cas_file_data(fdata)
        
            self.assertEqual(expectedList, actualList)

