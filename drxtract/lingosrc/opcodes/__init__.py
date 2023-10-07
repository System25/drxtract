# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

#
# Opcodes.
# 
from typing import List, Dict
from .opcode import Opcode, BiOpcode, TriOpcode, Param1Opcode, Param2Opcode

from .binary_op import MultiplyOpcode, AddOpcode, SubOpcode, DivOpcode, \
	ModOpcode, ConcatOpcode, ConcatSpcOpcode, ContainsOpcode, \
	StartsWithOpcode, LessThanOpcode, LessThanEqOpcode, NotEqOpcode, \
	EqualOpcode, GreaterThanOpcode, GreaterThanEqOpcode, AndOpcode, \
	OrOpcode, IntersectsOpcode, WithinOpcode

from .assign_op import AssignGlobalVariableOpcode, AssignGlobalVarOpcode, \
	LoadPropertyOpcode, AssignPropertyOpcode, \
	AssignValToPropertyOpcode, AssignParameterOpcode, \
	AssignLocalVariableOpcode, AssignIntoLocalVarOpcode, \
	AssignIntoFieldOpcode, AssignAfterLocalVarOpcode, \
	AssignAfterFieldOpcode, AssignBeforeLocalVarOpcode, \
	AssignBeforeFieldOpcode

from .exit_op import ExitOpcode

from .jump_op import JumpOpcode, FowardJumpOpcode, ConditionalJumpOpcode

from .tell_op import WindowTellStartOpcode, WindowTellEndOpcode

from .call_op import CallLocalOpcode, CallExternalOpcode, \
	CallFuncWithExtGlobalOpcode, CallExternalMethodOpcode

from .property_op import SpecialPropertiesOpcode, \
	AssignSpecialPropertiesOpcode, NumberOfElementsOpcode, \
	MenuitemPropertiesOpcode, AssignMenuitemPropertiesOpcode, \
	SpritePropertiesOpcode, AssignSpritePropertiesOpcode, \
	SystemPropertiesOpcode, AssignSystemPropertiesOpcode, \
	CastPropertiesOpcode, AssignCastPropertiesOpcode, \
	VideoPropertiesOpcode, AssignVideoPropertiesOpcode, \
	PropertyAccesorOpcode, AssignPropertyAccesorOpcode, \
	KeyPropertyAccesorOpcode, FieldPropertiesOpcode, \
	NumberOfCastElementsOpcode, NameOfCastElementsOpcode, \
	AssignFieldPropertiesOpcode, SoundPropertiesOpcode, \
	AssignSoundPropertiesOpcode

from .stack_op import CopySymbolOpcode, DiscardSymbolsOpcode

from .conversion_op import ToListOpcode, ToDictionaryOpcode, LoadListOpcode, \
	LoadLListOpcode, LoadLongListOpcode, LoadLongLListOpcode

from .unary_op import MinusOpcode, NotOpcode, FieldOpcode

from .variable_op import VariableOpcode, GlobalVariableOpcode, \
	GlobalVarOpcode, PropertyNameOpcode, ParameterNameOpcode, \
	LocalVariableOpcode, TellPropertyOpcode

from .constant_op import ZeroOpcode, Int1bOpcode, Int2bOpcode, LiteralOpcode, \
	Literal2Opcode, SymbolOpcode, PropertyOpcode

from .string_op import StringOperationOpcode, HiliteOpcode, \
		DeleteFromFieldOpcode, PutIntoFieldOpcode, \
		PutAfterListOpcode, PutBeforeListOpcode, PutIntoListOpcode, \
		DeleteFromListOpcode, PutBeforeStringOpcode, \
		PutAfterStringOpcode, PutIntoStringOpcode, DeleteFromStringOpcode, \
		PutAfterFieldOpcode, PutBeforeFieldOpcode, PutIntoFieldSpOpcode

TRI_OPCODES_LIST : List[TriOpcode] = [
]

BI_OPCODES_LIST : List[BiOpcode] = [
	AssignIntoLocalVarOpcode(),
	AssignIntoFieldOpcode(),
	AssignAfterLocalVarOpcode(),
	AssignAfterFieldOpcode(),
	AssignBeforeLocalVarOpcode(),
	AssignBeforeFieldOpcode(),
	
	SpecialPropertiesOpcode(),
	AssignSpecialPropertiesOpcode(),
	NumberOfElementsOpcode(),
	MenuitemPropertiesOpcode(),
	AssignMenuitemPropertiesOpcode(),
	SpritePropertiesOpcode(),
	AssignSpritePropertiesOpcode(),
	SystemPropertiesOpcode(),
	AssignSystemPropertiesOpcode(),
	CastPropertiesOpcode(),
	AssignCastPropertiesOpcode(),
	VideoPropertiesOpcode(),
	AssignVideoPropertiesOpcode(),
	FieldPropertiesOpcode(),
	DeleteFromFieldOpcode(),
	NumberOfCastElementsOpcode(),
	NameOfCastElementsOpcode(),
	AssignFieldPropertiesOpcode(),
	SoundPropertiesOpcode(),
	AssignSoundPropertiesOpcode(),
	
	PutIntoFieldOpcode(),
	PutAfterListOpcode(),
	PutBeforeListOpcode(),
	PutIntoListOpcode(),
	DeleteFromListOpcode(),
	PutBeforeStringOpcode(),
	PutAfterStringOpcode(),
	PutIntoStringOpcode(),
	DeleteFromStringOpcode(),
	PutAfterFieldOpcode(),
	PutBeforeFieldOpcode(),
	PutIntoFieldSpOpcode()
]	

OPCODES_LIST: List[Opcode] = [
	AddOpcode(),
	SubOpcode(),
	MultiplyOpcode(),
	DivOpcode(),
	ModOpcode(),
	ConcatOpcode(),
	ConcatSpcOpcode(),
	ContainsOpcode(),
	StartsWithOpcode(),
	LessThanOpcode(),
	LessThanEqOpcode(),
	NotEqOpcode(),
	EqualOpcode(),
	GreaterThanOpcode(),
	GreaterThanEqOpcode(),
	AndOpcode(),
	OrOpcode(),
	IntersectsOpcode(),
	WithinOpcode(),
	
	AssignGlobalVariableOpcode(),
	AssignGlobalVarOpcode(),
	LoadPropertyOpcode(),
	AssignPropertyOpcode(),
	AssignValToPropertyOpcode(),
	AssignParameterOpcode(),
	AssignLocalVariableOpcode(),
	AssignIntoLocalVarOpcode(),
	AssignIntoFieldOpcode(),
	AssignAfterLocalVarOpcode(),
	AssignAfterFieldOpcode(),
	AssignBeforeLocalVarOpcode(),
	AssignBeforeFieldOpcode(),
	
	ExitOpcode(),
	
	JumpOpcode(),
	FowardJumpOpcode(),
	ConditionalJumpOpcode(),
	
	WindowTellStartOpcode(),
	WindowTellEndOpcode(),
	
	CallLocalOpcode(),
	CallExternalOpcode(),
	CallFuncWithExtGlobalOpcode(),
	CallExternalMethodOpcode(),
	
	SpecialPropertiesOpcode(),
	AssignSpecialPropertiesOpcode(),
	NumberOfElementsOpcode(),
	MenuitemPropertiesOpcode(),
	AssignMenuitemPropertiesOpcode(),
	SpritePropertiesOpcode(),
	AssignSpritePropertiesOpcode(),
	SystemPropertiesOpcode(),
	AssignSystemPropertiesOpcode(),
	CastPropertiesOpcode(),
	AssignCastPropertiesOpcode(),
	VideoPropertiesOpcode(),
	AssignVideoPropertiesOpcode(),
	PropertyAccesorOpcode(),
	AssignPropertyAccesorOpcode(),
	KeyPropertyAccesorOpcode(),
	FieldPropertiesOpcode(),
	NumberOfCastElementsOpcode(),
	NameOfCastElementsOpcode(),
	AssignFieldPropertiesOpcode(),
	SoundPropertiesOpcode(),
	AssignSoundPropertiesOpcode(),
	
	CopySymbolOpcode(),
	DiscardSymbolsOpcode(),
	
	ToListOpcode(),
	ToDictionaryOpcode(),
	LoadListOpcode(),
	LoadLListOpcode(),
	LoadLongListOpcode(),
	LoadLongLListOpcode(),
	
	MinusOpcode(),
	NotOpcode(),
	FieldOpcode(),
	
	VariableOpcode(),
	GlobalVariableOpcode(),
	GlobalVarOpcode(),
	PropertyNameOpcode(),
	ParameterNameOpcode(),
	LocalVariableOpcode(),
	TellPropertyOpcode(),
	
	ZeroOpcode(), 
	Int1bOpcode(), 
	Int2bOpcode(), 
	LiteralOpcode(),
	Literal2Opcode(), 
	SymbolOpcode(), 
	PropertyOpcode(),
	
	StringOperationOpcode(),
	HiliteOpcode(),
	DeleteFromFieldOpcode(),
	PutIntoFieldOpcode(),
	PutAfterListOpcode(),
	PutBeforeListOpcode(),
	PutIntoListOpcode(),
	DeleteFromListOpcode(),
	PutBeforeStringOpcode(),
	PutAfterStringOpcode(),
	PutIntoStringOpcode(),
	DeleteFromStringOpcode(),
	PutAfterFieldOpcode(),
	PutBeforeFieldOpcode(),
	PutIntoFieldSpOpcode()
]

OPCODES: Dict[int, Opcode] = {}
for op in OPCODES_LIST:
	idx: int = op.opcode
	OPCODES[idx] = op


BI_OPCODES: Dict[int, BiOpcode] = {}
for op in BI_OPCODES_LIST:
	idxb: int = op.opcode * 256 + op.opcode2
	BI_OPCODES[idxb] = op

TRI_OPCODES: Dict[int, TriOpcode] = {}
for op in TRI_OPCODES_LIST:
	idxt: int = op.opcode * 65536 + op.opcode2*256 + op.opcode3
	TRI_OPCODES[idxt] = op

