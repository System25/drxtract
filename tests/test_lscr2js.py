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
        ['repeat_while.Lnam', 'repeat_while.Lscr', 'repeat_while.js'],
        ['repeat_with.Lnam', 'repeat_with.Lscr', 'repeat_with.js'],
        ['if_in_repeat.Lnam', 'if_in_repeat.Lscr', 'if_in_repeat.js'],
        ['global_var_fn.Lnam', 'global_var_fn.Lscr', 'global_var_fn.js'],
        ['global_var_hdr.Lnam', 'global_var_hdr.Lscr', 'global_var_hdr.js'],
        ['inherit.Lnam', 'inherit_main.Lscr', 'inherit_main.js'],
        ['inherit.Lnam', 'inherit_animal.Lscr', 'inherit_animal.js'],
        ['inherit.Lnam', 'inherit_insect.Lscr', 'inherit_insect.js'],
        ['inherit.Lnam', 'inherit_quadruped.Lscr', 'inherit_quadruped.js'],
        ['put_after.Lnam', 'put_after.Lscr', 'put_after.js'],
        ['put_after_field.Lnam', 'put_after_field.Lscr', 'put_after_field.js'],
        ['keys.Lnam', 'keys.Lscr', 'keys.js'],
        ['actor_list.Lnam', 'actor_list.Lscr', 'actor_list.js'],
        ['go.Lnam', 'go.Lscr', 'go.js'],
        ['sprite_props.Lnam', 'sprite_props.Lscr', 'sprite_props.js'],
        ['intersects.Lnam', 'intersects.Lscr', 'intersects.js'],
        ['prop_list.Lnam', 'prop_list.Lscr', 'prop_list.js'],
        ['string_sp_op.Lnam', 'string_sp_op.Lscr', 'string_sp_op.js'],
        ['video_props.Lnam', 'video_props.Lscr', 'video_props.js'],
        ['delete.Lnam', 'delete.Lscr', 'delete.js'],
        ['call_fn_ext_glb.Lnam', 'call_fn_ext_glb.Lscr', 'call_fn_ext_glb.js'],
        ['hilite.Lnam', 'hilite.Lscr', 'hilite.js'],
        ['assign_sp_prop.Lnam', 'assign_sp_prop.Lscr', 'assign_sp_prop.js'],
        ['sprite_rect.Lnam', 'sprite_rect.Lscr', 'sprite_rect.js'],
    ])
    def test_script(self, lnam_file: str, lsrc_file: str, lingo_file: str):
        
        name_list = parse_lnam_file(lnam_file)

        script: Script =  parse_lrcr_file(lsrc_file, name_list)
        
        generated: str = generate_js_code(script)
        
        with open(lingo_file, mode='rb') as file:
            expected = file.read().decode('UTF-8')
        
        self.assertEqual(expected, generated)
