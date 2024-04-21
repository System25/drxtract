# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from typing import Dict, Any, List
import struct
import logging
import base64
import re
from ..lingosrc.util import vsprintf, get_keys
from .castparser import CastParser, DIR_CLUT_TYPE, DIR_IMAGE_TYPE, \
    DIR_LSCR_TYPE, DIR_PUSH_BUTTON_TYPE, DIR_SHAPE_TYPE, DIR_SND_TYPE, \
    DIR_TEXT_INPUT_TYPE, DIR_TEXT_TYPE, DIR_TRAN_TYPE
    
from .button import ButtonParser
from .image import ImageParser
from .palette import PaletteParser
from .script import ScriptParser
from .shape import ShapeParser
from .sound import SoundParser
from .text import TextParser
from .textinput import TextInputParser
from .transition import TransitionParser

PARSERS: Dict[int, CastParser] = {
    DIR_PUSH_BUTTON_TYPE: ButtonParser(),
    DIR_IMAGE_TYPE: ImageParser(),
    DIR_CLUT_TYPE: PaletteParser(),
    DIR_LSCR_TYPE: ScriptParser(),
    DIR_SHAPE_TYPE: ShapeParser(),
    DIR_SND_TYPE: SoundParser(),
    DIR_TEXT_INPUT_TYPE: TextInputParser(),
    DIR_TEXT_TYPE: TextParser(),
    DIR_TRAN_TYPE: TransitionParser()
}

PURGE_PRIORITY: List[str] = ['Normal', 'Never', 'Last', 'Next']

#
# Cast data structure class
# 
# =============================================================================
class CastDataStruct:
    """This class represents the main structure of a Cast file"""
    
    def __init__(self, dataType: int, headerData: bytes, basicData: bytes):
        self.dataType: int = dataType
        self.headerData: bytes = headerData
        self.basicData: bytes = basicData


#
# Reads the basic data structure from a Director 4 Cast file.
# =============================================================================
def parse_cast_data_struct_dir4(fdata: bytes) -> CastDataStruct:
    """
    Parse a CAST file and return its content.
    
    Parameters
    ----------
    fdata : bytes
        The bytes in the Cast file that contain the information about a casting
        member.
        
    Returns
    -------
    CastDataStruct
        The basic data structure of the Cast file.

    Raises
    ------
    ValueError
        If some field inside the file is not compliant with the expected
        file structure. 
        
    """
    idx = 0
        
    header_size = struct.unpack(">h", fdata[idx:idx+2])[0]
    idx += 2
    logging.debug("header_size = %04x", header_size)
    
    additional_size = struct.unpack(">i", fdata[idx:idx+4])[0]
    idx += 4
    logging.debug("additional_size = %08x", additional_size)
    
    expected_length =  6 + header_size + additional_size
    if expected_length != len(fdata):
        msg = vsprintf("Bad data size! (%d != %d)", expected_length,
                       len(fdata))
        raise ValueError(msg)
        
    data_type = int(fdata[idx])
    idx += 1
    logging.debug("data_type = %02x", data_type)
    
    header_data = fdata[idx:idx + header_size - 1]
    idx += header_size - 1
    
    if additional_size > 0:
        basic_data = fdata[idx:idx + additional_size]
        idx += additional_size
    else:
        basic_data = bytearray()

    return CastDataStruct(data_type, header_data, basic_data)

#
# Reads the basic data structure from a Director 5 Cast file.
# =============================================================================
def parse_cast_data_struct_dir5(fdata: bytes) -> CastDataStruct:
    """
    Parse a CAST file and return its content.
    
    Parameters
    ----------
    fdata : bytes
        The bytes in the Cast file that contain the information about a casting
        member.
        
    Returns
    -------
    CastDataStruct
        The basic data structure of the Cast file.

    Raises
    ------
    ValueError
        If some field inside the file is not compliant with the expected
        file structure. 
        
    """
    idx = 0
    data_type = struct.unpack(">i", fdata[idx:idx+4])[0]
    idx += 4

    logging.debug("data_type = %08x", data_type)
    
    additional_size = struct.unpack(">i", fdata[idx:idx+4])[0]
    idx += 4
    logging.debug("additional_size = %08x", additional_size)

    header_size =  struct.unpack(">i", fdata[idx:idx+4])[0]
    idx += 4
    logging.debug("header_size = %08x", header_size)
    
    expected_length =  12 + header_size + additional_size
    if expected_length != len(fdata):
        msg = vsprintf("Bad data size! (%d != %d)", expected_length,
                       len(fdata))
        raise ValueError(msg)
    
    if additional_size > 0:
        basic_data = fdata[idx:idx + additional_size]
        idx += additional_size
    else:
        basic_data = bytearray()
    
    header_data = fdata[idx:idx + header_size]
    idx += header_size

    return CastDataStruct(data_type, header_data, basic_data)


#
# Reads the information from the basic data structure.
# =============================================================================
def parse_basic_cast_data(basic_data: bytes) -> Dict[str, Any]:
    """
    Parse the basic data structure and return its content.
    
    Parameters
    ----------
    fdata : bytes
        The bytes in the basic data structure.
        
    Returns
    -------
    Dict[str, Any]
        The basic data structure information.

    Raises
    ------
    ValueError
        If some field inside the file is not compliant with the expected
        file structure. 
        
    """
    if len(basic_data) <= 0:
        return {}
    
    content:Dict[str, Any] = {}
    
    # Parse main data
    idx = 0
    numbers_size =  struct.unpack(">i", basic_data[idx:idx+4])[0]
    idx += 4
    logging.debug("Numbers buffer size = %08x", numbers_size)
    
    if numbers_size < 0x00000014:
        msg = vsprintf("Bad numbers size %08x", numbers_size)
        raise ValueError(msg)
    
    # Content found!
    content['basic'] = {}
    
    script_key =  struct.unpack(">I", basic_data[idx:idx+4])[0]
    idx += 4
    logging.debug("basic_data00 = %08x", script_key)

    basic_data01 =  struct.unpack(">i", basic_data[idx:idx+4])[0]
    idx += 4
    logging.debug("basic_data01 = %08x", basic_data01)

    # The two higher bits are the purge priority
    # The two lower bits are other things
    basic_data02 =  struct.unpack(">i", basic_data[idx:idx+4])[0]
    idx += 4
    logging.debug("basic_data02 = %08x", basic_data02)

    script_index =  struct.unpack(">i", basic_data[idx:idx+4])[0]
    idx += 4
    logging.debug("script_index: %08x", script_index)
    
    content['basic']['script_key'] = script_key
    content['basic']['basic_data1'] = basic_data01
    content['basic']['basic_data2'] = basic_data02
    content['basic']['purge_priority'] = PURGE_PRIORITY[(basic_data02 >> 2) & 3]
    content['basic']['script_index'] = script_index
    
    nelems: int =  int((numbers_size - 0x00000014) / 4)
    for i in range(0, nelems):
        unknown =  struct.unpack(">i", basic_data[idx:idx+4])[0]
        idx += 4
        logging.debug("unknown[%d]: %08x", i, unknown)        

    nstruct =  struct.unpack(">h", basic_data[idx:idx+2])[0]
    idx += 2
    logging.debug("number of structures contained = %d", nstruct)

    if nstruct > 0:
        content['extra'] = []
    
        struct_indx = []
        for i in range(0, nstruct+1):
            stindx =  struct.unpack(">i", basic_data[idx:idx+4])[0]
            idx += 4
            logging.debug("stindx[%d] = %08x", i, stindx)
            struct_indx.append(stindx)

        for i in range(0, nstruct):
            p = i + 1
            stlen = struct_indx[p] - struct_indx[i]
            logging.debug("The %d element of the structure is %d bytes long",
                          i, stlen)
            if stlen > 0:
                stdata = basic_data[idx:idx+stlen]
                idx += stlen
                
                encodedBytes = base64.b64encode(stdata)
                encodedStr = encodedBytes.decode('ascii')
                
                content['extra'].append(encodedStr)
            else:
                content['extra'].append('')

        # Check if there is a CAST member name
        if len(content['extra']) > 1 and content['extra'][1] != '':
            stdata = base64.b64decode(content['extra'][1])
            nchars = int(stdata[0])
            cast_elm_name = stdata[1:nchars+1].decode('ISO-8859-1')
            cast_elm_name = re.sub(r"[^A-Za-z0-9\-_\. ]", "_", cast_elm_name)
            content['name'] = cast_elm_name
            logging.debug("Cast member name: '%s'", cast_elm_name)
        else:
            content['name'] = ''


    return content

#
# Reads from Cast data the casting element information.
# =============================================================================
def parse_cast_file_data(fdata: bytes) -> Dict[str, Any]:
    """
    Parse a CAS file and return its content.
    
    Parameters
    ----------
    fdata : bytes
        The bytes in the Cast file that contain the information about a casting
        member.
        
    Returns
    -------
    Dict[str, Any]
        a dictionary with the data.

    Raises
    ------
    ValueError
        If some field inside the file is not compliant with the expected
        file structure. 
        
    """
    castData: Dict[str, Any] = {}
        
    idx = 0
    data_type = struct.unpack(">i", fdata[idx:idx+4])[0]

    if (data_type & 0xFFFFFF00) != 0:
        # Director 4 structure
        logging.debug("Director 4 CASt file!")
        dataSt = parse_cast_data_struct_dir4(fdata)
        
    else:
        # Director 5 structure
        logging.debug("Director 5 CASt file!")
        dataSt = parse_cast_data_struct_dir5(fdata)

    content = parse_basic_cast_data(dataSt.basicData)
    
    dt = dataSt.dataType
    if dt in get_keys(PARSERS):
        parser = PARSERS[dt]
        castData = parser.parse(dataSt.headerData, content)
    else:
        logging.warning("data_type unknown (%s)!", data_type)

    castData['content'] = content
    return castData
