# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

#
# Unit test for lscr2lingo
#

import unittest
import os
from parameterized import parameterized

from src.lingosrc.ast import Script
from src.lingosrc.parse import parse_lnam_file, parse_lrcr_file
from src.lingosrc.codegen import generate_js_code



class TestScript(unittest.TestCase):
    
    maxDiff = None
    
    def setUp(self):
        os.chdir(os.path.join(os.path.dirname(__file__), 'files', 'lingo/'))
    
    @parameterized.expand([
        ['constants.Lnam', 'constants.Lscr', 'constants.js'],
        ['local_var.Lnam', 'local_var.Lscr', 'local_var.js'],
        ['if_else.Lnam', 'if_else.Lscr', 'if_else.js'],
    ])
    def test_script(self, lnam_file: str, lsrc_file: str, lingo_file: str):
        
        name_list = parse_lnam_file(lnam_file)

        script: Script =  parse_lrcr_file(lsrc_file, name_list)
        
        generated: str = generate_js_code(script)
        
        with open(lingo_file, mode='rb') as file:
            expected = file.read().decode('UTF-8')
        
        self.assertEqual(expected, generated)
