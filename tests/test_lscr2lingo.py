# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

#
# Unit test for lscr2js
#

import unittest
import os
from parameterized import parameterized

from src.lingosrc.ast import Script
from src.lingosrc.parse import parse_lnam_file, parse_lrcr_file
from src.lingosrc.codegen import generate_lingo_code



class TestScript(unittest.TestCase):
    
    maxDiff = None
    
    def setUp(self):
        os.chdir(os.path.join(os.path.dirname(__file__), 'files', 'lingo/'))
    
    @parameterized.expand([
        ['constants.Lnam', 'constants.Lscr', 'constants.lingo'],
        ['local_var.Lnam', 'local_var.Lscr', 'local_var.lingo'],
        ['if_else.Lnam', 'if_else.Lscr', 'if_else.lingo'],
        ['repeat_while.Lnam', 'repeat_while.Lscr', 'repeat_while.lingo'],
        ['repeat_with.Lnam', 'repeat_with.Lscr', 'repeat_with.lingo'],
        ['if_in_repeat.Lnam', 'if_in_repeat.Lscr', 'if_in_repeat.lingo'],
        ['global_var_fn.Lnam', 'global_var_fn.Lscr', 'global_var_fn.lingo'],
        ['global_var_hdr.Lnam', 'global_var_hdr.Lscr', 'global_var_hdr.lingo'],
        ['inherit.Lnam', 'inherit_main.Lscr', 'inherit_main.lingo'],
        ['inherit.Lnam', 'inherit_animal.Lscr', 'inherit_animal.lingo'],
        ['inherit.Lnam', 'inherit_insect.Lscr', 'inherit_insect.lingo'],
        ['inherit.Lnam', 'inherit_quadruped.Lscr', 'inherit_quadruped.lingo'],
        ['put_after.Lnam', 'put_after.Lscr', 'put_after.lingo'],
        ['put_after_field.Lnam', 'put_after_field.Lscr',
         'put_after_field.lingo'],
        ['keys.Lnam', 'keys.Lscr', 'keys.lingo'],
        ['actor_list.Lnam', 'actor_list.Lscr', 'actor_list.lingo'],
        ['go.Lnam', 'go.Lscr', 'go.lingo'],
        ['sprite_props.Lnam', 'sprite_props.Lscr', 'sprite_props.lingo'],
        ['intersects.Lnam', 'intersects.Lscr', 'intersects.lingo'],
        ['prop_list.Lnam', 'prop_list.Lscr', 'prop_list.lingo'],
        ['predef_constants.Lnam', 'predef_constants.Lscr', 
         'predef_constants.lingo'],
        ['string_sp_op.Lnam', 'string_sp_op.Lscr', 'string_sp_op.lingo'],
        ['video_props.Lnam', 'video_props.Lscr', 'video_props.lingo'],
        
    ])
    def test_script(self, lnam_file: str, lsrc_file: str, lingo_file: str):
        
        name_list = parse_lnam_file(lnam_file)

        script: Script =  parse_lrcr_file(lsrc_file, name_list)
        
        generated: str = generate_lingo_code(script)
        
        with open(lingo_file, mode='rb') as file:
            expected = file.read().decode('UTF-8')
        
        self.assertEqual(expected, generated)