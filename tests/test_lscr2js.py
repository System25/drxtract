# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

#
# Unit test for lscr2js
#

import unittest
import os
from parameterized import parameterized

from drxtract.lingosrc.ast import Script
from drxtract.lingosrc.parse import parse_lnam_file, parse_lrcr_file
from drxtract.lingosrc.codegen import generate_js_code



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
        ['tell.Lnam', 'tell.Lscr', 'tell.js'],
        ['beepon.Lnam', 'beepon.Lscr', 'beepon.js'],
        ['menuitem.Lnam', 'menuitem.Lscr', 'menuitem.js'],
        ['list_sp_op.Lnam', 'list_sp_op_movie.Lscr', 'list_sp_op_movie.js'],
        ['list_sp_op.Lnam', 'list_sp_op_frame.Lscr', 'list_sp_op_frame.js'],
        ['string_lv_sp_op.Lnam', 'string_lv_sp_op.Lscr', 'string_lv_sp_op.js'],
        ['string_gv_sp_op.Lnam', 'string_gv_sp_op.Lscr', 'string_gv_sp_op.js'],
        ['string_fi_sp_op.Lnam', 'string_fi_sp_op.Lscr', 'string_fi_sp_op.js'],
        ['field_props.Lnam', 'field_props.Lscr', 'field_props.js'],
        ['sound_props.Lnam', 'sound_props.Lscr', 'sound_props.js'],
        ['cast_props.Lnam', 'cast_props.Lscr', 'cast_props.js'],
        ['hilite_op.Lnam', 'hilite_op.Lscr', 'hilite_op.js'],
        ['system_props.Lnam', 'system_props.Lscr', 'system_props.js'],
        ['date_time.Lnam', 'date_time.Lscr', 'date_time.js'],
        ['prop_list_init.Lnam', 'prop_list_init.Lscr', 'prop_list_init.js'],
        ['exit_repeat.Lnam', 'exit_repeat.Lscr', 'exit_repeat.js'],
        ['gv_as_sym.Lnam', 'gv_as_sym.Lscr', 'gv_as_sym.js'],
        ['last.Lnam', 'last.Lscr', 'last.js'],
        ['sprite_loc.Lnam', 'sprite_loc.Lscr', 'sprite_loc.js'],
        ['sound_fn.Lnam', 'sound_fn.Lscr', 'sound_fn.js'],
        
    ])
    def test_script(self, lnam_file: str, lsrc_file: str, lingo_file: str):
        
        name_list = parse_lnam_file(lnam_file)

        script: Script =  parse_lrcr_file(lsrc_file, name_list)
        
        generated: str = generate_js_code(script)
        
        with open(lingo_file, mode='rb') as file:
            expected = file.read().decode('UTF-8')
        
        self.assertEqual(expected, generated)
