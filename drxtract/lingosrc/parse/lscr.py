# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from typing import List, cast
from ..ast import Script, FunctionDef, Node, LocalVariable, ParameterName
from ..model import Context, Header
from ..util import escape_string, unpack_float80
from ..opcodes import OPCODES, Opcode, BiOpcode, TriOpcode, \
    Param1Opcode, Param2Opcode, BI_OPCODES, TRI_OPCODES
from .loop_detection import condition_detect, loop_detect
import struct
import logging

DEBUG_OPCODES: bool = True

#
# Parse LSCR file data
# 
# =============================================================================
def parse_lrcr_file_data(fdata: bytes, name_list: List[str]) -> Script:
    """
    Parse a LSCR file and return the AST of the code inside it.
    
    Parameters
    ----------
    fdata : bytes
        The bytes inside the LNAM file to parse.
    name_list: List[str]
        The list of variables names and function names.
        
    Returns
    -------
    script
        a script object with the Abstract-Syntax-Tree.
        
    Raises
    ------
    ValueError
        If some field inside the file is not compliant with the expected
        file structure.
        
    """
    
    context = Context()
    context.name_list = name_list
    
    # Parse the file header
    header = parse_lrcr_file_header(fdata)
    
    # Read the constants descriptors
    context.constants = parse_lrcr_crb(fdata, header)
    context.bytes_per_constant = header.bytes_per_constant
    
    # Read the properties record blocks
    script = Script()
    script.properties = parse_lrcr_prb(fdata, header, name_list)
    context.properties = script.properties
    
    # Read the global vars record blocks
    script.global_vars = parse_lrcr_grb(fdata, header, name_list)
    
    # Read the function record blocks once to get the local function names
    parse_frb_func_names(fdata, header, context)
    
    # Read the function record blocks to get the function code as an AST
    parse_frb(fdata, header, context, script)


    return script


#
# Parse the function record blocks
# 
# =============================================================================
def parse_frb(fdata: bytes, header: Header, context: Context, script: Script):
    """
    Parse the function record blocks inside the LSCR file.
    
    Parameters
    ----------
    fdata : bytes
        The bytes inside the LNAM file to parse.
    header: Header
        The header of the LSRC file.
    context: Context
        The file parsing context.
    script: Script
        The script object where the parsed functions will be added.
        
        
    Raises
    ------
    ValueError
        If some field inside the file is not compliant with the expected
        file structure.
        
    """
    
    logging.debug("====== parse LSCR func record block (code)===============")
    lsrc_bit_order = '>'
    idx = header.frb_offset
    for i in range(0, header.frb_nrecords):

        logging.debug("Function Record Block: %i (starts in: %x)"%(i, idx)) 
        # $0000-$0001  uint16  Namelist index for the function's name,
        # or 0xFFFF if there is no name(?)
        namelist_index = struct.unpack(lsrc_bit_order+"h", fdata[idx:idx+2])[0]
        idx += 2

        # $0002-$0003  uint16  Unknown
        unknown_rb0 = struct.unpack(lsrc_bit_order+"h", fdata[idx:idx+2])[0]
        idx += 2

        # $0004-$0007  uint32  Length of the function bytecode in bytes
        bc_length = struct.unpack(lsrc_bit_order+"i", fdata[idx:idx+4])[0]
        idx += 4

        # $0008-$000B  uint32  Offset to the function bytecode
        bc_off = struct.unpack(lsrc_bit_order+"i", fdata[idx:idx+4])[0]
        idx += 4

        # $000C-$000D  uint16 Number of arguments
        bc_narg = struct.unpack(lsrc_bit_order+"h", fdata[idx:idx+2])[0]
        idx += 2

        # $000E-$0011  uint32  Offset of arguments name
        argnames_off = struct.unpack(lsrc_bit_order+"i", fdata[idx:idx+4])[0]
        idx += 4

        # $0012-$0013  uint16  Number of local variables
        bc_nlocal = struct.unpack(lsrc_bit_order+"h", fdata[idx:idx+2])[0]
        idx += 2

        # $0014-$0017  uint32  Local variables offset
        localnames_off = struct.unpack(lsrc_bit_order+"i", fdata[idx:idx+4])[0]
        idx += 4

        # $0018-$0019  uint16  Count (C)
        count_c = struct.unpack(lsrc_bit_order+"h", fdata[idx:idx+2])[0]
        idx += 2

        # $001A-$001D  uint32  Unknown
        unknown_rb3 = struct.unpack(lsrc_bit_order+"i", fdata[idx:idx+4])[0]
        idx += 4

        # $001E-$0021  uint32  Unknown
        unknown_rb4 = struct.unpack(lsrc_bit_order+"i", fdata[idx:idx+4])[0]
        idx += 4

        # $0022-$0023  uint16  Unknown
        unknown_rb5 = struct.unpack(lsrc_bit_order+"h", fdata[idx:idx+2])[0]
        idx += 2

        # $0024-$0025  uint16  Count (D)
        count_d = struct.unpack(lsrc_bit_order+"h", fdata[idx:idx+2])[0]
        idx += 2

        # $0026-$0029  uint32  Unknown
        unknown_rb6 = struct.unpack(lsrc_bit_order+"i", fdata[idx:idx+4])[0]
        idx += 4

        logging.debug("namelist_index = %x"%(namelist_index)) 
        logging.debug("unknown_rb0 = %x"%(unknown_rb0)) 
        logging.debug("bc_length = %x"%(bc_length)) 
        logging.debug("bc_off = %x"%(bc_off)) 
        logging.debug("bc_narg = %x"%(bc_narg)) 
        logging.debug("argnames_off = %x"%(argnames_off)) 
        logging.debug("bc_nlocal = %x"%(bc_nlocal)) 
        logging.debug("localnames_off = %x"%(localnames_off)) 
        logging.debug("count_c = %x"%(count_c)) 
        logging.debug("unknown_rb3 = %x"%(unknown_rb3)) 
        logging.debug("unknown_rb4 = %x"%(unknown_rb4)) 
        logging.debug("unknown_rb5 = %x"%(unknown_rb5)) 
        logging.debug("count_d = %x"%(count_d)) 
        logging.debug("unknown_rb6 = %x"%(unknown_rb6)) 


        logging.debug("Function Record Block: %i (ends in: %x)"%(i, idx)) 

        fname = 'noname'
        if namelist_index >= 0 and namelist_index < len(context.name_list):
            fname = context.name_list[namelist_index]
        
        fn = FunctionDef(fname, idx)
        
        # Read the local variable names record block
        for nl in range(0, bc_nlocal):
            idxl = 2*nl + localnames_off
            n = struct.unpack(lsrc_bit_order+"h", fdata[idxl:idxl+2])[0]
            logging.debug("idxl = %x n=%s"%(idxl, n))
            logging.debug('localvs[%s] = "%s"'%(nl, context.name_list[n]))
            fn.local_vars.append(
                LocalVariable(context.name_list[n], idxl))

        # Read the parameter names record block
        for nl in range(0, bc_narg):
            idxl = 2*nl + argnames_off
            n = struct.unpack(lsrc_bit_order+"h", fdata[idxl:idxl+2])[0]
            logging.debug("idxl = %x n=%s"%(idxl, n))
            logging.debug('paramns[%s] = "%s"'%(nl, context.name_list[n]))
            fn.parameters.append(
                ParameterName(context.name_list[n], idxl))
            
        parse_opcodes(fdata, context, bc_off, bc_length, fn)
        script.functions.append(fn)
        
#
# Parse the code of a function.
# 
# =============================================================================
def parse_opcodes(fdata: bytes, context: Context, bc_off: int,
                  bc_length: int, fn: FunctionDef):
    """
    Parse the function operation codes and generates an AST.
    
    Parameters
    ----------
    fdata : bytes
        The bytes inside the LNAM file to parse.
    context: Context
        The file parsing context.
    bc_off: int
        Offset to the begining of the function opcodes.
    bc_length: int
        Length of the function opcodes.
    fn: FunctionDef
        The function which opcodes we are parsing.
        
        
    Raises
    ------
    ValueError
        If some field inside the file is not compliant with the expected
        file structure.
        
    """
    stack: List[Node] = []
    idxc = bc_off
    index = idxc
    while (idxc - bc_off) < bc_length:
        opcode = int(fdata[idxc])
        idxc = idxc + 1

        if opcode in OPCODES.keys():
            parse_obj:Opcode = OPCODES[opcode]
            
            if parse_obj.nbytes == 2:
                opcode2 = int(fdata[idxc])
                idxc = idxc + 1
                if DEBUG_OPCODES:
                    logging.debug("[%s] op0: %s op1: %s"%(index, hex(opcode),
                                                          hex(opcode2)))
                
                if isinstance(parse_obj, BiOpcode):
                    op_idx = opcode * 256 + opcode2
                    parse_obj = BI_OPCODES[op_idx]
                else:
                    cast(Param1Opcode, parse_obj).param1 = opcode2
            elif parse_obj.nbytes == 3:
                opcode2 = int(fdata[idxc])
                idxc = idxc + 1 
                opcode3 = int(fdata[idxc])
                idxc = idxc + 1
                
                if DEBUG_OPCODES:
                    logging.debug("[%s] op0: %s op1: %s op2: %s"%(index,
                                                             hex(opcode),
                                                             hex(opcode2),
                                                             hex(opcode3)))
                
                if isinstance(parse_obj, TriOpcode):
                    op_idx = opcode * 65536 + opcode2 * 256 + opcode3
                    parse_obj = TRI_OPCODES[op_idx]
                else:
                    cast(Param2Opcode, parse_obj).param1 = opcode2
                    cast(Param2Opcode, parse_obj).param2 = opcode3
            elif DEBUG_OPCODES:
                logging.debug("[%s] op0: %s"%(index, hex(opcode)))
                    
            parse_obj.process(context, stack, fn, index)
            index = idxc
            if DEBUG_OPCODES:
                logging.debug("-> %s"%(parse_obj.__class__.__name__))
            
        else:
            raise Exception("opcode not implemented: %s"%(opcode))

    condition_detect(fn)
    loop_detect(fn)
    

#
# Get local function names from function record blocks
# 
# =============================================================================
def parse_frb_func_names(fdata: bytes, header: Header, context: Context):
    """
    Parse a the function record blocks and save all the local function names
    in the Context.
    
    Parameters
    ----------
    fdata : bytes
        The bytes inside the LNAM file to parse.
    header: Header
        The header of the LSRC file.
    context: Context
        The file parsing context.
        
        
    Raises
    ------
    ValueError
        If some field inside the file is not compliant with the expected
        file structure.
        
    """
    
    logging.debug("====== parse LSCR func record block (names)===============")
    lsrc_bit_order = '>'    
    idx = header.frb_offset
    context.local_func_names = []
    for i in range(0, header.frb_nrecords):
        # $0000-$0001  uint16  Namelist index for the function's name,
        # or 0xFFFF if there is no name(?)
        namelist_index = struct.unpack(lsrc_bit_order+"h", fdata[idx:idx+2])[0]
        idx += 42
        
        fname = 'noname'
        if namelist_index >= 0 and namelist_index < len(context.name_list):
            fname = context.name_list[namelist_index]
        logging.debug('lfnames[%d]=%s'%(i, fname))
        context.local_func_names.append(fname)
    
    
#
# Parse LSCR properties record blocks
# 
# =============================================================================
def parse_lrcr_prb(fdata: bytes, header: Header, name_list: List[str]
                   ) -> List[str]:
    """
    Parse a LSCR properties record blocks and return a list of string with
    the properties names.
    
    Parameters
    ----------
    fdata : bytes
        The bytes inside the LNAM file to parse.
    header: Header
        The header of the LSRC file.
    name_list: List[str]
        The list of variables names and function names.
        
    Returns
    -------
    constants
        a list of strings with the properties names.
        
    Raises
    ------
    ValueError
        If some field inside the file is not compliant with the expected
        file structure.
        
    """
    
    logging.debug("====== parse LSCR properties record block =================")
    lsrc_bit_order = '>'    
    pnames: List[str] = []
    if header.grb_offset != header.prb_offset:
        # Read the properties record blocks once to get all the properties names
        idx = header.prb_offset
        i = 0
        while idx < header.grb_offset:
            # $0000-$0001  uint16  Namelist index for the property's name,
            # or 0xFFFF if there is no name(?)
            namelist_index = struct.unpack(lsrc_bit_order+"h", fdata[
                idx:idx+2])[0]
            idx += 2

            fname = 'noname'
            if namelist_index >= 0 and namelist_index < len(name_list):
                fname = name_list[namelist_index]
            logging.debug('pnames[%d]=%s'%(i, fname))
            i += 1
            pnames.append(fname)            
    

    return pnames

#
# Parse LSCR global vars record blocks
# 
# =============================================================================
def parse_lrcr_grb(fdata: bytes, header: Header, name_list: List[str]
                   ) -> List[str]:
    """
    Parse a LSCR global vars record blocks and return a list of string with
    the global var names.
    
    Parameters
    ----------
    fdata : bytes
        The bytes inside the LNAM file to parse.
    header: Header
        The header of the LSRC file.
    name_list: List[str]
        The list of variables names and function names.
        
    Returns
    -------
    constants
        a list of strings with the global var names.
        
    Raises
    ------
    ValueError
        If some field inside the file is not compliant with the expected
        file structure.
        
    """
    
    logging.debug("====== parse LSCR global vars record block ===============")
    lsrc_bit_order = '>'    
    gnames: List[str] = []
    if header.frb_offset != header.grb_offset:
        # Read the global vars record blocks once to get all the
        # global vars names
        idx = header.grb_offset
        i = 0
        while idx < header.frb_offset:
            # $0000-$0001  uint16  Namelist index for the property's name,
            # or 0xFFFF if there is no name(?)
            namelist_index = struct.unpack(lsrc_bit_order+"h", fdata[
                idx:idx+2])[0]
            idx += 2

            fname = 'noname'
            if namelist_index >= 0 and namelist_index < len(name_list):
                fname = name_list[namelist_index]
            logging.debug('gnames[%d]=%s'%(i, fname))
            i += 1
            gnames.append(fname)            
    

    return gnames


#
# Parse LSCR constant record blocks
# 
# =============================================================================
def parse_lrcr_crb(fdata: bytes, header: Header) -> List[str]:
    """
    Parse a LSCR constant record blocks and return a list of string with
    the constant values.
    
    Parameters
    ----------
    fdata : bytes
        The bytes inside the LNAM file to parse.
    header: Header
        The header of the LSRC file.
        
    Returns
    -------
    constants
        a list of strings with the constant values.
        
    Raises
    ------
    ValueError
        If some field inside the file is not compliant with the expected
        file structure.
        
    """
    
    lsrc_bit_order = '>'
    constants: List[str] = []

    bytes_per_const = 6
    idx = header.crb_offset

    logging.debug("====== parse LSCR constants record block =================")
    for i in range(0, header.crb_nconstants):
        logging.debug("idx = %s"%(idx))
        if bytes_per_const == 8:
            # uint32: Value type ID 
            logging.debug("4 bytes constant ID")
            constant_type = struct.unpack(lsrc_bit_order+"i",
                                          fdata[idx:idx+4])[0]
            idx += 4
        else:
            # uint16: Value type ID
            logging.debug("2 bytes constant ID")
            constant_type = struct.unpack(lsrc_bit_order+"h",
                                          fdata[idx:idx+2])[0]
            idx += 2
            if constant_type == 0:
                logging.debug("It may be a 4 bytes constant ID")
                constant_type = struct.unpack(lsrc_bit_order+"h",
                                              fdata[idx:idx+2])[0]
                idx += 2
                bytes_per_const = 8

        # uint32: Data address, relative to the base address given in the header 
        constant_offset = struct.unpack(lsrc_bit_order+"i", fdata[idx:idx+4])[0]
        idx += 4

        #logging.debug("constant_type = %s"%(constant_type)) 
        #logging.debug("constant_offset = %s"%(constant_offset))

        if constant_type == 1:
            # Text constant
            idxc = header.con_offset + constant_offset

            # uint32: String length
            strlength = struct.unpack(lsrc_bit_order+"i",
                                      fdata[idxc:idxc+4])[0] - 1
            idxc += 4
            #logging.debug("strlength = %s"%(strlength)) 

            strval = fdata[idxc:idxc+strlength].decode('ISO-8859-1')
            constants.append(escape_string(strval))


        elif constant_type == 4:
            # 32 bits integer constant
            constants.append(constant_offset)

        elif constant_type == 9:
            # Floating point
            idxc = header.con_offset + constant_offset
            
            # uint32: Float length
            floatlength = struct.unpack(lsrc_bit_order+"i",
                                        fdata[idxc:idxc+4])[0]
            idxc += 4
            #logging.debug("floatlength = %s"%(floatlength))
            
            float_val =  unpack_float80(fdata[idxc:idxc+floatlength])
            #logging.debug("float Value = %s"%(float_val))
            constants.append(float_val)


        else:
            # Unknown
            logging.error("Unknown constant type: %s"%(constant_type))
            raise ValueError("Unknown constant type!")

        logging.debug("constants[%s] = %s"%(i, constants[i]))
        
    header.bytes_per_constant = bytes_per_const
    return constants
        

#
# Parse LSCR header
# 
# =============================================================================
def parse_lrcr_file_header(fdata: bytes) -> Header:
    """
    Parse a LSCR file and return the AST of the code inside it.
    
    Parameters
    ----------
    fdata : bytes
        The bytes inside the LNAM file to parse.
        
    Returns
    -------
    header
        a header object with the offset to the different sections
        int a LSCR file.
        
    Raises
    ------
    ValueError
        If some field inside the file is not compliant with the expected
        file structure.
        
    """
    
    lsrc_bit_order = '>'

    idx = 0
    scr_type = struct.unpack(lsrc_bit_order+"i", fdata[idx:idx+4])[0]
    idx += 4
    unknown_01 =  struct.unpack(lsrc_bit_order+"i", fdata[idx:idx+4])[0]
    idx += 4
    filesize0 =  struct.unpack(lsrc_bit_order+"i", fdata[idx:idx+4])[0]
    idx += 4
    filesize1 =  struct.unpack(lsrc_bit_order+"i", fdata[idx:idx+4])[0]
    idx += 4
    unknown_04 =  struct.unpack(lsrc_bit_order+"i", fdata[idx:idx+4])[0]
    idx += 4
    unknown_05 =  struct.unpack(lsrc_bit_order+"i", fdata[idx:idx+4])[0]
    idx += 4
    unknown_06 =  struct.unpack(lsrc_bit_order+"i", fdata[idx:idx+4])[0]
    idx += 4
    unknown_07 =  struct.unpack(lsrc_bit_order+"i", fdata[idx:idx+4])[0]
    idx += 4
    unknown_08 =  struct.unpack(lsrc_bit_order+"i", fdata[idx:idx+4])[0]
    idx += 4
    unknown_09 =  struct.unpack(lsrc_bit_order+"i", fdata[idx:idx+4])[0]
    idx += 4
    unknown_10 =  struct.unpack(lsrc_bit_order+"i", fdata[idx:idx+4])[0]
    idx += 4
    unknown_11 =  struct.unpack(lsrc_bit_order+"i", fdata[idx:idx+4])[0]
    idx += 4
    unknown_12 =  struct.unpack(lsrc_bit_order+"i", fdata[idx:idx+4])[0]
    idx += 4
    unknown_13 =  struct.unpack(lsrc_bit_order+"i", fdata[idx:idx+4])[0]
    idx += 4
    unknown_14 =  struct.unpack(lsrc_bit_order+"i", fdata[idx:idx+4])[0]
    idx += 4
    unknown_15 =  struct.unpack(lsrc_bit_order+"i", fdata[idx:idx+4])[0]
    idx += 4

    logging.debug("====== parse LSCR file header ============================")
    logging.debug("scr_type = %08x"%(scr_type)) 
    logging.debug("unknown_01 = %08x"%(unknown_01)) 
    logging.debug("filesize0 = %s"%(filesize0)) 
    logging.debug("filesize1 = %s"%(filesize1)) 
    logging.debug("unknown_04 = %08x"%(unknown_04)) 
    logging.debug("unknown_05 = %08x"%(unknown_05)) 
    logging.debug("unknown_06 = %08x"%(unknown_06)) 
    logging.debug("unknown_07 = %08x"%(unknown_07)) 
    logging.debug("unknown_08 = %08x"%(unknown_08)) 
    logging.debug("unknown_09 = %08x"%(unknown_09)) 
    logging.debug("unknown_10 = %08x"%(unknown_10)) 
    logging.debug("unknown_11 = %08x"%(unknown_11)) 
    logging.debug("unknown_12 = %08x"%(unknown_12)) 
    logging.debug("unknown_13 = %08x"%(unknown_13)) 
    logging.debug("unknown_14 = %08x"%(unknown_14)) 
    logging.debug("unknown_15 = %08x"%(unknown_15)) 

    if filesize1 != filesize0 or filesize1 != len(fdata):
        logging.error("bad filesize (%s, %s, %s)"%(filesize1, filesize0, len(fdata))) 
        raise ValueError("Bad file size!")

    # $0040-$0041 uint16 Offset to the properties records block  
    prb_offset = struct.unpack(lsrc_bit_order+"h", fdata[idx:idx+2])[0]
    idx += 2

    # $0042-$0043 uint16 Number of global var records  
    grb_nrecords =  struct.unpack(lsrc_bit_order+"h", fdata[idx:idx+2])[0]
    idx += 2
    unknown_18 =  struct.unpack(lsrc_bit_order+"h", fdata[idx:idx+2])[0]
    idx += 2

    # $0045-$0046 uint16 Offset to the global_vars records block  
    grb_offset = struct.unpack(lsrc_bit_order+"h", fdata[idx:idx+2])[0]
    idx += 2

    logging.debug("prb_offset = %s"%(prb_offset)) 
    logging.debug("grb_nrecords = %s"%(grb_nrecords)) 
    logging.debug("unknown_18 = %s"%(unknown_18)) 
    logging.debug("frb_offset = %s"%(grb_offset)) 


    # $0048-$0049 uint16 Number of function records 
    frb_nrecords = struct.unpack(lsrc_bit_order+"h", fdata[idx:idx+2])[0]
    idx += 2

    unknown_19 =  struct.unpack(lsrc_bit_order+"h", fdata[idx:idx+2])[0]
    idx += 2

    # $0052-$0053 Offset to the function records block
    frb_offset = struct.unpack(lsrc_bit_order+"h", fdata[idx:idx+2])[0]
    idx += 2

    logging.debug("frb_nrecords = %s"%(frb_nrecords)) 
    logging.debug("unknown_19 = %s"%(unknown_19)) 
    logging.debug("frb_offset = %s"%(frb_offset)) 

    # $004E-$004F    uint16  Number of constants 
    crb_nconstants = struct.unpack(lsrc_bit_order+"h", fdata[idx:idx+2])[0]
    idx += 2

    unknown_20 =  struct.unpack(lsrc_bit_order+"h", fdata[idx:idx+2])[0]
    idx += 2

    # $0052-$0053  uint16 Offset to the constant records block 
    crb_offset = struct.unpack(lsrc_bit_order+"h", fdata[idx:idx+2])[0]
    idx += 2

    unknown_21 =  struct.unpack(lsrc_bit_order+"h", fdata[idx:idx+2])[0]
    idx += 2

    # Size in bytes of the constants area???
    unknown_22 =  struct.unpack(lsrc_bit_order+"h", fdata[idx:idx+2])[0]
    idx += 2

    unknown_23 =  struct.unpack(lsrc_bit_order+"h", fdata[idx:idx+2])[0]
    idx += 2

    # $005A-$005B uint16 Base address for constant data
    con_offset = struct.unpack(lsrc_bit_order+"h", fdata[idx:idx+2])[0]
    idx += 2

    logging.debug("crb_nconstants = %s"%(crb_nconstants))
    logging.debug("unknown_20 = %s"%(unknown_20))
    logging.debug("crb_offset = %s"%(crb_offset))
    logging.debug("unknown_21 = %s"%(unknown_21))
    logging.debug("unknown_22 = %s"%(unknown_22))
    logging.debug("unknown_23 = %s"%(unknown_23))
    logging.debug("con_offset = %s"%(con_offset))

    header = Header()
    header.con_offset = con_offset
    header.crb_offset = crb_offset
    header.crb_nconstants = crb_nconstants
    header.frb_nrecords = frb_nrecords
    header.frb_offset = frb_offset
    header.prb_offset = prb_offset
    header.grb_nrecords = grb_nrecords
    header.grb_offset = grb_offset
    return header
