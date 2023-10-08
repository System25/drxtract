# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from .opcode import BiOpcode, Param1Opcode
from ..ast import FunctionDef, Sprite, StringOperationNames, \
    LocalVariable, PropertyName, DateTimeFunction, UnaryStringOperation, \
    BinaryOperation, BinaryOperationNames, \
    MenuitemAccessorOperation, Menu, MenuItem, PropertyAccessorOperation, \
    Cast, Node, ConstantValue, KeyPropertyAccessorOperation, \
    LoadListOperation, Statement, UnaryOperation, UnaryOperationNames, \
    MenuitemsAccessorOperation, SoundChannel
from ..model import Context
from typing import List, cast, Optional

SPECIAL_PROPERTIES = ['floatPrecision', 'mouseDownScript', 'mouseUpScript',
                      'keyDownScript', 'keyUpScript', 'timeoutScript']

DATE_TIME_FUNCTIONS = ['short time', 'abbr time', 'long time',
                       'short date', 'abbr date', 'long date']

OPERATION_TYPES: List[StringOperationNames] = [StringOperationNames.UNKNOWN,
                                               StringOperationNames.CHAR,
                                               StringOperationNames.WORD,
                                               StringOperationNames.ITEM,
                                               StringOperationNames.LINE]

MENUITEM_PROPERTIES = ['UNKNOWN0', 'name', 'checkMark', 'enabled', 'script']

NUM_OF_TYPES = ['UNKNOWN0', 'perFrameHook', 'castMembers', 'menus']

SPRITE_PROPERTIES = ['UNKNOWN0', 'type', 'backColor', 'bottom', 'castNum',
                     'constraint', 'cursor', 'foreColor', 'height', 'UNKNOWN1',
                     'ink', 'left', 'lineSize', 'locH', 'locV', 'movieRate',
                     'movieTime', 'UNKNOWN2', 'puppet', 'right',
                     'startTime', 'stopTime', 'stretch', 'top', 'trails',
                     'visible', 'volume', 'width', 'blend', 'scriptNum',
                     'moveableSprite', 'editabletext', 'scoreColor', 'loc',
                     'rect']

CAST_PROPERTIES = ['UNKNOWN0', 'name', 'text', 'textStyle', 'textFont',
                   'textHeight', 'textAlign', 'textSize', 'picture',
                   'hilite', 'number', 'size', 'UNKNOWN8', 'UNKNOWN9',
                   'UNKNOWNA', 'UNKNOWNB',
                   'UNKNOWNC', 'foreColor', 'backColor']

SOUND_PROPERTIES = ['UNKNOWN0', 'volume']

VIDEO_PROPERTIES = ['UNKNOWN0', 'UNKNOWN1', 'UNKNOWN2', 'UNKNOWN3', 'UNKNOWN4',
                    'UNKNOWN5', 'UNKNOWN6', 'UNKNOWN7', 'UNKNOWN8',
                    'UNKNOWN9', 'UNKNOWNA', 'UNKNOWNB', 'loop',
                    'duration', 'controller', 'directToStage', 'sound']

SYSTEM_PROPERTIES = {
    'UNKNOWN_SYSTEM_PROPERTY_00': 'UNKNOWN',
    'beepOn': '_movie',
    'buttonStyle': '_movie',
    'centerStage': '_movie',
    'checkBoxAccess': '_system',
    'checkBoxType': '_system',
    'colorDepth': '_system',
    'UNKNOWN_SYSTEM_PROPERTY_07': 'UNKNOWN',
    'exitLock': '_movie',
    'fixStageSize': '_movie',
    'UNKNOWN_SYSTEM_PROPERTY_0A': 'UNKNOWN',
    'UNKNOWN_SYSTEM_PROPERTY_0B': 'UNKNOWN',
    'UNKNOWN_SYSTEM_PROPERTY_0C': 'UNKNOWN',
    'UNKNOWN_SYSTEM_PROPERTY_0D': 'UNKNOWN',
    'UNKNOWN_SYSTEM_PROPERTY_0E': 'UNKNOWN',
    'UNKNOWN_SYSTEM_PROPERTY_0F': 'UNKNOWN',
    'UNKNOWN_SYSTEM_PROPERTY_10': 'UNKNOWN',
    'UNKNOWN_SYSTEM_PROPERTY_11': 'UNKNOWN',
    'UNKNOWN_SYSTEM_PROPERTY_12': 'UNKNOWN',
    'timeoutLapsed': '_system',
    'UNKNOWN_SYSTEM_PROPERTY_14': 'UNKNOWN',
    'UNKNOWN_SYSTEM_PROPERTY_15': 'UNKNOWN',
    'UNKNOWN_SYSTEM_PROPERTY_16': 'UNKNOWN',
    'selEnd': '_movie',
    'selStart': '_movie',
    'soundEnabled': '_sound',
    'soundLevel': '_sound',
    'stageColor': '_movie',
    'UNKNOWN_SYSTEM_PROPERTY_1C': 'UNKNOWN',
    'switchColorDepth': '_player',
    'timeoutKeyDown': '_system',
    'timeoutLength': '_system',
    'timeoutMouse': '_system',
    'timeoutPlay': '_system',
    'timer': '_system'
}

#
# Special properties Opcode.
#
class SpecialPropertiesOpcode(BiOpcode):
    def __init__(self):
        super().__init__(0x5C, 0x00)
    
    def process(self, context: Context, stack: List[Node], \
                fn: FunctionDef, index: int):
        param: ConstantValue = cast(ConstantValue, stack.pop())
        property_index = int(param.name)
        op: Optional[Node] = None
        if property_index < 6:
            op = PropertyName(SPECIAL_PROPERTIES[property_index], index)
        
        elif property_index < 12:
            idx_6: int = property_index - 6
            op = DateTimeFunction(DATE_TIME_FUNCTIONS[idx_6], index)
        
        else:
            op = UnaryStringOperation(UnaryOperationNames.LAST, index)
            idx_11: int = property_index - 11
            op.type = OPERATION_TYPES[idx_11]
            op.of = stack.pop()
        
        stack.append(op)
    
#
# Assign Special properties Opcode.
#
class AssignSpecialPropertiesOpcode(SpecialPropertiesOpcode):
    def __init__(self):
        super().__init__()
        self.opcode = 0x5D
        
    def process(self, context: Context, stack: List[Node], \
                fn: FunctionDef, index: int):
        super().process(context, stack, fn, index)
        op = BinaryOperation(BinaryOperationNames.ASSIGN, index)
        op.left = stack.pop()
        op.right = stack.pop()
        fn.statements.append(Statement(op, index))
    
#
# Number of ... Opcode.
#
class NumberOfElementsOpcode(BiOpcode):
    def __init__(self):
        super().__init__(0x5C, 0x01)
    
    def process(self, context: Context, stack: List[Node], \
                fn: FunctionDef, index: int):
        param: ConstantValue = cast(ConstantValue, stack.pop())
        optype = int(param.name)        
        op = UnaryStringOperation(UnaryOperationNames.NUMBER, index)
        op.type = OPERATION_TYPES[optype]
        op.of = stack.pop()
        stack.append(op)


#
# Name of elements ... Opcode.
#
class NameOfCastElementsOpcode(BiOpcode):
    def __init__(self):
        super().__init__(0x5C, 0x02)
    
    def process(self, context: Context, stack: List[Node], \
                fn: FunctionDef, index: int):
        param1: ConstantValue = cast(ConstantValue, stack.pop())
        optype = int(param1.name)
        
        param2: ConstantValue = cast(ConstantValue, stack.pop())
        
        if optype == 1:
            op = UnaryStringOperation(UnaryOperationNames.NAME, index)
            op.of = Menu(param2.name, index)
        
        elif optype == 2:
            op = UnaryStringOperation(UnaryOperationNames.NUMBER, index)
            op.of = MenuitemsAccessorOperation(Menu(param2.name, index), index) 
        
        else:
            raise Exception("Unknown op type: %s"%(optype))           
        
        stack.append(op)

#
# Menuitem properties Opcode.
#
class MenuitemPropertiesOpcode(BiOpcode):
    def __init__(self):
        super().__init__(0x5C, 0x03)
    
    def process(self, context: Context, stack: List[Node], \
                fn: FunctionDef, index: int):
        property_index = int(cast(ConstantValue, stack.pop()).name)
        menu_id = cast(ConstantValue, stack.pop()).name
        menu_item_id = cast(ConstantValue, stack.pop()).name
        
        mia = MenuitemAccessorOperation(Menu(menu_id, index),
                                        MenuItem(menu_item_id, index),
                                        index)
        pac = PropertyAccessorOperation(mia,
                                        MENUITEM_PROPERTIES[property_index],
                                        index)
        
        stack.append(pac)
    
#
# Assign Menuitem properties Opcode.
#
class AssignMenuitemPropertiesOpcode(BiOpcode):
    def __init__(self):
        super().__init__(0x5D, 0x03)
    
    
    def process(self, context: Context, stack: List[Node], \
                fn: FunctionDef, index: int):
        
        property_index = int(cast(ConstantValue, stack.pop()).name)
        value = stack.pop()
        menu_id = cast(ConstantValue, stack.pop()).name
        menu_item_id = cast(ConstantValue, stack.pop()).name
        
        mia = MenuitemAccessorOperation(Menu(menu_id, index),
                                        MenuItem(menu_item_id, index),
                                        index)
        pac = PropertyAccessorOperation(mia,
                                        MENUITEM_PROPERTIES[property_index],
                                        index)        
        
        op = BinaryOperation(BinaryOperationNames.ASSIGN, index)
        op.left = pac
        op.right = value
        fn.statements.append(Statement(op, index))


#
# Sound properties Opcode.
#
class SoundPropertiesOpcode(BiOpcode):
    def __init__(self):
        super().__init__(0x5C, 0x04)
    
    def process(self, context: Context, stack: List[Node], \
                fn: FunctionDef, index: int):
        property_index = int(cast(ConstantValue, stack.pop()).name)
        channel_id = cast(ConstantValue, stack.pop()).name
        sound_channel = SoundChannel(channel_id, index)
        prop = SOUND_PROPERTIES[property_index]
        op = PropertyAccessorOperation(sound_channel, prop, index)
        stack.append(op)

#
# Assign Sound properties Opcode.
#
class AssignSoundPropertiesOpcode(BiOpcode):
    def __init__(self):
        super().__init__(0x5D, 0x04)


    def process(self, context: Context, stack: List[Node], \
                fn: FunctionDef, index: int):
        property_index = int(cast(ConstantValue, stack.pop()).name)
        value = stack.pop()
        channel_id = cast(ConstantValue, stack.pop()).name
        
        sound_channel = SoundChannel(channel_id, index)
        prop = SOUND_PROPERTIES[property_index]
        accessor = PropertyAccessorOperation(sound_channel, prop, index)

        op = BinaryOperation(BinaryOperationNames.ASSIGN, index)
        op.left = accessor
        op.right = value
        fn.statements.append(Statement(op, index))  


#
# Sprite properties Opcode.
#
class SpritePropertiesOpcode(BiOpcode):
    def __init__(self):
        super().__init__(0x5C, 0x06)
    
    def process(self, context: Context, stack: List[Node], \
                fn: FunctionDef, index: int):
        property_index = int(cast(ConstantValue, stack.pop()).name)
        sprite_id = cast(ConstantValue, stack.pop()).name
        sprite = Sprite(sprite_id, index)
        prop = SPRITE_PROPERTIES[property_index]
        op = PropertyAccessorOperation(sprite, prop, index)
        stack.append(op)

#
# Assign Sprite properties Opcode.
#
class AssignSpritePropertiesOpcode(BiOpcode):
    def __init__(self):
        super().__init__(0x5D, 0x06)


    def process(self, context: Context, stack: List[Node], \
                fn: FunctionDef, index: int):
        property_index = int(cast(ConstantValue, stack.pop()).name)
        value = stack.pop()
        sprite_id = cast(ConstantValue, stack.pop()).name
        
        sprite = Sprite(sprite_id, index)
        prop = SPRITE_PROPERTIES[property_index]
        accessor = PropertyAccessorOperation(sprite, prop, index)

        op = BinaryOperation(BinaryOperationNames.ASSIGN, index)
        op.left = accessor
        op.right = value
        fn.statements.append(Statement(op, index))    

    
#
# System properties Opcode.
#
class SystemPropertiesOpcode(BiOpcode):
    def __init__(self):
        super().__init__(0x5C, 0x07)

    def process(self, context: Context, stack: List[Node], \
                fn: FunctionDef, index: int):
        property_index = int(cast(ConstantValue, stack.pop()).name)
        property_name = list(SYSTEM_PROPERTIES.keys())[property_index]
        
        obj: Node = LocalVariable(SYSTEM_PROPERTIES[property_name], index)
        if context.tell_object is not None:
            obj = LocalVariable('tell_obj', index)
        op: Node = PropertyAccessorOperation(obj, property_name, index)
        
        stack.append(op)
    
#
# Assign System properties Opcode.
#
class AssignSystemPropertiesOpcode(SystemPropertiesOpcode):
    def __init__(self):
        super().__init__()
        self.opcode = 0x5D
    
    
    def process(self, context: Context, stack: List[Node], \
                fn: FunctionDef, index: int):
        SystemPropertiesOpcode.process(self, context, stack, fn, \
                                       index)
        op = BinaryOperation(BinaryOperationNames.ASSIGN, index)
        op.left = stack.pop()
        op.right = stack.pop()
        fn.statements.append(Statement(op, index))  

#
# Number of elements ... Opcode.
#
class NumberOfCastElementsOpcode(BiOpcode):
    def __init__(self):
        super().__init__(0x5C, 0x08)
    
    def process(self, context: Context, stack: List[Node], \
                fn: FunctionDef, index: int):
        param: ConstantValue = cast(ConstantValue, stack.pop())
        optype = int(param.name)

        op = UnaryStringOperation(UnaryOperationNames.NUMBER, index)
        op.of = LocalVariable(NUM_OF_TYPES[optype], index)
        stack.append(op)
    
#
# Cast properties Opcode.
#
class CastPropertiesOpcode(BiOpcode):
    def __init__(self):
        super().__init__(0x5C, 0x09)
    
    def process(self, context: Context, stack: List[Node], \
                fn: FunctionDef, index: int):
        p_index: ConstantValue = cast(ConstantValue, stack.pop())
        property_index = int(p_index.name)
        cast_id: ConstantValue = cast(ConstantValue, stack.pop())
        cast_member = Cast(cast_id.name, index)
        prop = CAST_PROPERTIES[property_index]
        op = PropertyAccessorOperation(cast_member, prop, index)
        stack.append(op)

#
# Assign Cast properties Opcode.
#
class AssignCastPropertiesOpcode(BiOpcode):
    def __init__(self):
        super().__init__(0x5D, 0x09)
    
    
    def process(self, context: Context, stack: List[Node], \
                fn: FunctionDef, index: int):
        p_index: ConstantValue = cast(ConstantValue, stack.pop())
        property_index = int(p_index.name)
        value = stack.pop()
        cast_id: ConstantValue = cast(ConstantValue, stack.pop())
        
        cast_member = Cast(cast_id.name, index)
        prop = CAST_PROPERTIES[property_index]
        accessor = PropertyAccessorOperation(cast_member, prop, index)
        
        op = BinaryOperation(BinaryOperationNames.ASSIGN, index)
        op.left = accessor
        op.right = value
        fn.statements.append(Statement(op, index)) 

#
# Field properties Opcode.
#
class FieldPropertiesOpcode(BiOpcode):
    def __init__(self):
        super().__init__(0x5C, 0x0b)
    
    def process(self, context: Context, stack: List[Node], \
                fn: FunctionDef, index: int):
        p_index: ConstantValue = cast(ConstantValue, stack.pop())
        property_index = int(p_index.name)
        field = UnaryOperation(UnaryOperationNames.FIELD, index)
        field.operand = stack.pop()
        prop = CAST_PROPERTIES[property_index]
        op = PropertyAccessorOperation(field, prop, index)
        stack.append(op)


#
# Assign Field properties Opcode.
#
class AssignFieldPropertiesOpcode(BiOpcode):
    def __init__(self):
        super().__init__(0x5D, 0x0b)
    
    
    def process(self, context: Context, stack: List[Node], \
                fn: FunctionDef, index: int):
        property_index = int(cast(ConstantValue, stack.pop()).name)
        value = stack.pop()
        cast_id = cast(ConstantValue, stack.pop()).name
        cast_node = Cast(cast_id, index)
        prop = CAST_PROPERTIES[property_index]
        accessor = PropertyAccessorOperation(cast_node, prop, index)
        
        op = BinaryOperation(BinaryOperationNames.ASSIGN, index)
        op.left = accessor
        op.right = value
        fn.statements.append(Statement(op, index)) 

#
# Video cast properties Opcode.
#
class VideoPropertiesOpcode(BiOpcode):
    def __init__(self):
        super().__init__(0x5C, 0x0d)
    
    def process(self, context: Context, stack: List[Node], \
                fn: FunctionDef, index: int):
        property_index = int(cast(ConstantValue, stack.pop()).name)
        cast_id = cast(ConstantValue, stack.pop()).name
        cast_node = Cast(cast_id, index)
        prop = VIDEO_PROPERTIES[property_index]
        op = PropertyAccessorOperation(cast_node, prop, index)
        stack.append(op)

#
# Assign Video cast properties Opcode.
#
class AssignVideoPropertiesOpcode(BiOpcode):
    def __init__(self):
        super().__init__(0x5D, 0x0d)
    
    
    def process(self, context: Context, stack: List[Node], \
                fn: FunctionDef, index: int):
        property_index = int(cast(ConstantValue, stack.pop()).name)
        value = stack.pop()
        cast_id = cast(ConstantValue, stack.pop()).name
        cast_node = Cast(cast_id, index)
        prop = VIDEO_PROPERTIES[property_index]
        accessor = PropertyAccessorOperation(cast_node, prop, index)
        
        op = BinaryOperation(BinaryOperationNames.ASSIGN, index)
        op.left = accessor
        op.right = value
        fn.statements.append(Statement(op, index)) 
    
#
# Property accesor Opcode.
#
class PropertyAccesorOpcode(Param1Opcode):
    def __init__(self):
        super().__init__(0x61)
    
    def process(self, context: Context, stack: List[Node], \
                fn: FunctionDef, index: int):
        op1 = self.param1
        prop = context.name_list[op1]
        op = PropertyAccessorOperation(stack.pop(), prop, index)
        stack.append(op)

#
# Assign Property accessor Opcode.
#
class AssignPropertyAccesorOpcode(Param1Opcode):
    def __init__(self):
        super().__init__(0x62)
    
    
    def process(self, context: Context, stack: List[Node], \
                fn: FunctionDef, index: int):
        op1 = self.param1
        value = stack.pop()
        node = stack.pop()
        prop = context.name_list[op1]
        accessor = PropertyAccessorOperation(node, prop, index)
        
        op = BinaryOperation(BinaryOperationNames.ASSIGN, index)
        op.left = accessor
        op.right = value
        fn.statements.append(Statement(op, index))

#
# Key Property accesor Opcode.
#
class KeyPropertyAccesorOpcode(Param1Opcode):
    def __init__(self):
        super().__init__(0x66)
    
    def process(self, context: Context, stack: List[Node], \
                fn: FunctionDef, index: int):
        op1 = self.param1
        prop = context.name_list[op1]
        empty_val = stack.pop()
        if (not isinstance(empty_val, LoadListOperation)
            or len(cast(LoadListOperation, empty_val).operands) > 0):
            raise Exception("The KeyPropertyAccessorOperation parameter should" 
                            + " be an empty list")
        op = KeyPropertyAccessorOperation(prop, index)
        stack.append(op)
