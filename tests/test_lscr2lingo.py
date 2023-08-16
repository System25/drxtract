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
from drxtract.lingosrc.codegen import generate_lingo_code



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
        ['delete.Lnam', 'delete.Lscr', 'delete.lingo'],
        ['call_fn_ext_glb.Lnam', 'call_fn_ext_glb.Lscr',
         'call_fn_ext_glb.lingo'],
        ['hilite.Lnam', 'hilite.Lscr', 'hilite.lingo'],
        ['assign_sp_prop.Lnam', 'assign_sp_prop.Lscr', 'assign_sp_prop.lingo'],
        ['sprite_rect.Lnam', 'sprite_rect.Lscr', 'sprite_rect.lingo'],
        ['tell.Lnam', 'tell.Lscr', 'tell.lingo'],
        ['beepon.Lnam', 'beepon.Lscr', 'beepon.lingo'],
        ['menuitem.Lnam', 'menuitem.Lscr', 'menuitem.lingo'],
        ['list_sp_op.Lnam', 'list_sp_op_movie.Lscr', 'list_sp_op_movie.lingo'],
        ['list_sp_op.Lnam', 'list_sp_op_frame.Lscr', 'list_sp_op_frame.lingo'],
        ['string_lv_sp_op.Lnam', 'string_lv_sp_op.Lscr', \
         'string_lv_sp_op.lingo'],
        ['string_gv_sp_op.Lnam', 'string_gv_sp_op.Lscr', \
         'string_gv_sp_op.lingo'],
        ['string_fi_sp_op.Lnam', 'string_fi_sp_op.Lscr', \
         'string_fi_sp_op.lingo'],
        ['field_props.Lnam', 'field_props.Lscr', 'field_props.lingo'],
        ['sound_props.Lnam', 'sound_props.Lscr', 'sound_props.lingo'],
        ['cast_props.Lnam', 'cast_props.Lscr', 'cast_props.lingo'],
        ['hilite_op.Lnam', 'hilite_op.Lscr', 'hilite_op.lingo'],
        ['system_props.Lnam', 'system_props.Lscr', 'system_props.lingo'],
        ['date_time.Lnam', 'date_time.Lscr', 'date_time.lingo'],
        ['prop_list_init.Lnam', 'prop_list_init.Lscr', 'prop_list_init.lingo'],
        ['exit_repeat.Lnam', 'exit_repeat.Lscr', 'exit_repeat.lingo'],
        ['gv_as_sym.Lnam', 'gv_as_sym.Lscr', 'gv_as_sym.lingo'],
        ['last.Lnam', 'last.Lscr', 'last.lingo'],
        ['sprite_loc.Lnam', 'sprite_loc.Lscr', 'sprite_loc.lingo'],
        ['sound_fn.Lnam', 'sound_fn.Lscr', 'sound_fn.lingo'],
        
    ])
    def test_script(self, lnam_file: str, lsrc_file: str, lingo_file: str):
        
        name_list = parse_lnam_file(lnam_file)

        script: Script =  parse_lrcr_file(lsrc_file, name_list)
        
        generated: str = generate_lingo_code(script)
        
        with open(lingo_file, mode='rb') as file:
            expected = file.read().decode('UTF-8')
        
        self.assertEqual(expected, generated)
