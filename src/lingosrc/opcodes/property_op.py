# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from .opcode import BiOpcode, Param1Opcode
from ..ast import Function, Sprite, StringOperationNames, \
    GlobalVariable, PropertyName, DateTimeFunction, UnaryStringOperation, \
    UnaryOperationNames, BinaryOperation, BinaryOperationNames, \
    MenuitemAccessorOperation, Menu, MenuItem, PropertyAccessorOperation, \
    Cast, Node, ConstantValue, KeyPropertyAccessorOperation, \
    LoadListOperation, Statement, UnaryOperation, UnaryOperationNames
from ..model import Context
from typing import List, cast, Optional

SPECIAL_PROPERTIES = ['floatPrecision', 'mouseDownScript', 'mouseUpScript',
                      'keyDownScript', 'keyUpScript', 'timeoutScript']

DATE_TIME_FUNCTIONS = ['short time', 'abbreviated time', 'long time',
                       'short date', 'abbreviated date', 'long date']

OPERATION_TYPES: List[StringOperationNames] = [StringOperationNames.UNKNOWN,
                                               StringOperationNames.CHAR,
                                               StringOperationNames.WORD,
                                               StringOperationNames.ITEM,
                                               StringOperationNames.LINE]

MENUITEM_PROPERTIES = ['name', 'checkMark', 'enabled', 'script']

SPRITE_PROPERTIES = ['UNKNOWN0', 'type', 'backColor', 'bottom', 'castNum',
                     'constraint', 'cursor', 'foreColor', 'height', 'UNKNOWN1',
                     'ink', 'left', 'lineSize', 'locH', 'locV', 'movieRate',
                     'movieTime', 'UNKNOWN2', 'puppet', 'right',
                     'startTime', 'stopTime', 'stretch', 'top', 'trails',
                     'visible', 'volume', 'width', 'blend', 'scriptNum',
                     'moveableSprite', 'UNKNOWN3', 'scoreColor']

CAST_PROPERTIES = ['UNKNOWN0', 'name', 'text', 'UNKNOWN2', 'UNKNOWN3', 'UNKNOWN4',
                   'UNKNOWN5', 'UNKNOWN6', 'picture', 'hilite', 'number',
                   'size', 'UNKNOWN8', 'UNKNOWN9', 'UNKNOWNA', 'UNKNOWNB',
                   'UNKNOWNC', 'foreColor', 'backColor']

VIDEO_PROPERTIES = ['UNKNOWN1', 'UNKNOWN2', 'UNKNOWN3', 'UNKNOWN4',
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
    'stillDown': '_movie',
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
        BiOpcode.__init__(self, 0x5C, 0x00)
    
    def process(self, context: Context, stack: List[Node], \
                function: Function, index: int):
        param: ConstantValue = cast(ConstantValue, stack.pop())
        property_index = int(param.name)
        op: Optional[Node] = None
        if property_index < 6:
            op = PropertyName(SPECIAL_PROPERTIES[property_index], index)
        
        elif property_index < 12:
            op = DateTimeFunction(DATE_TIME_FUNCTIONS[property_index-6], index)
        
        else:
            op = UnaryStringOperation(UnaryOperationNames.LAST, index)
            op.type = OPERATION_TYPES[property_index-12]
            op.of = stack.pop()
        
        stack.append(op)
    
#
# Assign Special properties Opcode.
#
class AssignSpecialPropertiesOpcode(SpecialPropertiesOpcode):
    def __init__(self):
        SpecialPropertiesOpcode.__init__(self)
        self.opcode = 0x5D
        
    def process(self, context: Context, stack: List[Node], \
                function: Function, index: int):
        SpecialPropertiesOpcode.process(self, context, stack, function, \
                                        index)
        op = BinaryOperation(BinaryOperationNames.ASSIGN, index)
        op.left = stack.pop()
        op.right = stack.pop()
        stack.append(op)
    
#
# Number of ... Opcode.
#
class NumberOfElementsOpcode(BiOpcode):
    def __init__(self):
        BiOpcode.__init__(self, 0x5C, 0x01)
    
    def process(self, context: Context, stack: List[Node], \
                function: Function, index: int):
        param: ConstantValue = cast(ConstantValue, stack.pop())
        optype = int(param.name)        
        op = UnaryStringOperation(UnaryOperationNames.NUMBER, index)
        op.type = OPERATION_TYPES[optype]
        op.of = stack.pop()
        stack.append(op)


#
# Menuitem properties Opcode.
#
class MenuitemPropertiesOpcode(BiOpcode):
    def __init__(self):
        BiOpcode.__init__(self, 0x5C, 0x03)
    
    def process(self, context: Context, stack: List[Node], \
                function: Function, index: int):
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
        BiOpcode.__init__(self, 0x5D, 0x03)
    
    
    def process(self, context: Context, stack: List[Node], \
                function: Function, index: int):
        
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
        function.statements.append(Statement(op, index))

#
# Sprite properties Opcode.
#
class SpritePropertiesOpcode(BiOpcode):
    def __init__(self):
        BiOpcode.__init__(self, 0x5C, 0x06)
    
    def process(self, context: Context, stack: List[Node], \
                function: Function, index: int):
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
        BiOpcode.__init__(self, 0x5D, 0x06)


    def process(self, context: Context, stack: List[Node], \
                function: Function, index: int):
        property_index = int(cast(ConstantValue, stack.pop()).name)
        value = stack.pop()
        sprite_id = cast(ConstantValue, stack.pop()).name
        
        sprite = Sprite(sprite_id, index)
        prop = SPRITE_PROPERTIES[property_index]
        accessor = PropertyAccessorOperation(sprite, prop, index)

        op = BinaryOperation(BinaryOperationNames.ASSIGN, index)
        op.left = accessor
        op.right = value
        function.statements.append(Statement(op, index))    

    
#
# System properties Opcode.
#
class SystemPropertiesOpcode(BiOpcode):
    def __init__(self):
        BiOpcode.__init__(self, 0x5C, 0x07)

    def process(self, context: Context, stack: List[Node], \
                function: Function, index: int):
        property_index = int(cast(ConstantValue, stack.pop()).name)
        property_name = list(SYSTEM_PROPERTIES.keys())[property_index]
        
    
        obj = GlobalVariable(SYSTEM_PROPERTIES[property_name], index)
        op = PropertyAccessorOperation(obj, property_name, index)
        stack.append(op)
    
#
# Assign System properties Opcode.
#
class AssignSystemPropertiesOpcode(SystemPropertiesOpcode):
    def __init__(self):
        SystemPropertiesOpcode.__init__(self)
        self.opcode = 0x5D
    
    
    def process(self, context: Context, stack: List[Node], \
                function: Function, index: int):
        SystemPropertiesOpcode.process(self, context, stack, function, \
                                       index)
        op = BinaryOperation(BinaryOperationNames.ASSIGN, index)
        op.left = stack.pop()
        op.right = stack.pop()
        function.statements.append(Statement(op, index))  
    
    
#
# Cast properties Opcode.
#
class CastPropertiesOpcode(BiOpcode):
    def __init__(self):
        BiOpcode.__init__(self, 0x5C, 0x09)
    
    def process(self, context: Context, stack: List[Node], \
                function: Function, index: int):
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
        BiOpcode.__init__(self, 0x5D, 0x09)
    
    
    def process(self, context: Context, stack: List[Node], \
                function: Function, index: int):
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
        function.statements.append(Statement(op, index)) 

#
# Field properties Opcode.
#
class FieldPropertiesOpcode(BiOpcode):
    def __init__(self):
        BiOpcode.__init__(self, 0x5C, 0x0b)
    
    def process(self, context: Context, stack: List[Node], \
                function: Function, index: int):
        p_index: ConstantValue = cast(ConstantValue, stack.pop())
        property_index = int(p_index.name)
        field = UnaryOperation(UnaryOperationNames.FIELD, index)
        field.operand = stack.pop()
        prop = CAST_PROPERTIES[property_index]
        op = PropertyAccessorOperation(field, prop, index)
        stack.append(op)

#
# Video cast properties Opcode.
#
class VideoPropertiesOpcode(BiOpcode):
    def __init__(self):
        BiOpcode.__init__(self, 0x5C, 0x0d)
    
    def process(self, context: Context, stack: List[Node], \
                function: Function, index: int):
        property_index = int(cast(ConstantValue, stack.pop()).name)
        cast_id = cast(ConstantValue, stack.pop()).name
        cast = Cast(cast_id, index)
        prop = VIDEO_PROPERTIES[property_index]
        op = PropertyAccessorOperation(cast, prop, index)
        stack.append(op)

#
# Assign Video cast properties Opcode.
#
class AssignVideoPropertiesOpcode(VideoPropertiesOpcode):
    def __init__(self):
        BiOpcode.__init__(self, 0x5D, 0x0d)
    
    
    def process(self, context: Context, stack: List[Node], \
                function: Function, index: int):
        property_index = int(cast(ConstantValue, stack.pop()).name)
        value = stack.pop()
        cast_id = cast(ConstantValue, stack.pop()).name
        cast = Cast(cast_id, index)
        prop = VIDEO_PROPERTIES[property_index]
        accessor = PropertyAccessorOperation(cast, prop, index)
        
        op = BinaryOperation(BinaryOperationNames.ASSIGN, index)
        op.left = accessor
        op.right = value
        function.statements.append(Statement(op, index)) 
    
#
# Property accesor Opcode.
#
class PropertyAccesorOpcode(Param1Opcode):
    def __init__(self):
        Param1Opcode.__init__(self, 0x61)
    
    def process(self, context: Context, stack: List[Node], \
                function: Function, index: int):
        op1 = self.param1
        prop = context.name_list[op1]
        op = PropertyAccessorOperation(stack.pop(), prop, index)
        stack.append(op)

#
# Assign Property accessor Opcode.
#
class AssignPropertyAccesorOpcode(PropertyAccesorOpcode):
    def __init__(self):
        PropertyAccesorOpcode.__init__(self)
        self.opcode = 0x62
    
    
    def process(self, context: Context, stack: List[Node], \
                function: Function, index: int):
        PropertyAccesorOpcode.process(self, context, stack, function, \
                                      index)
        value = stack.pop()
        op = BinaryOperation(BinaryOperationNames.ASSIGN, index)
        op.left = stack.pop()
        op.right = value
        stack.append(op) 

#
# Key Property accesor Opcode.
#
class KeyPropertyAccesorOpcode(Param1Opcode):
    def __init__(self):
        Param1Opcode.__init__(self, 0x66)
    
    def process(self, context: Context, stack: List[Node], \
                function: Function, index: int):
        op1 = self.param1
        prop = context.name_list[op1]
        empty_val = stack.pop()
        if (not isinstance(empty_val, LoadListOperation)
            or len(cast(LoadListOperation, empty_val).operands) > 0):
            raise Exception("The KeyPropertyAccessorOperation parameter should" +
                            " be an empty list")
        op = KeyPropertyAccessorOperation(prop, index)
        stack.append(op)
