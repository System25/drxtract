# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from typing import Any, Dict
import logging
from ..lingosrc.util import vsprintf, get_keys
from .decoder import Decoder
from .decoder2b import Decoder2b
from .decoder4b import Decoder4b
from .decoder8b import Decoder8b
from .decoder16b import Decoder16b
from .decoder24b import Decoder24b

DECODERS: Dict[int, Decoder] = {
    2: Decoder2b(),
    4: Decoder4b(),
    8: Decoder8b(),
    16: Decoder16b(),
    24: Decoder24b(),
    32: Decoder24b()
    
}

#
# Transforms the BITD data into a BMP image
# =============================================================================
def bitd2bmp(castData: Dict[str, Any], clutData: bytes,
    fdata: bytes) -> bytes:
    """
    Parse a BITD file and return its content as a bitmap image.
    
    Parameters
    ----------
    cast: Dict[str, Any]
        Casting object information.
    clutData: bytes
        Custom color palette
    fdata : bytes
        The bytes in the BITD file that contains the image.
        
    Returns
    -------
    bytes
        a byte array with the BMP image.

    Raises
    ------
    ValueError
        If some field inside the file is not compliant with the expected
        file structure. 
        
    """
    bmp_height:int = castData['height']
    bmp_width:int = castData['width']
    bmp_bpp:int = castData['depth']
    bmp_padding_w:int = castData['w_padding']
    bmp_padding_h:int = castData['h_padding']
    bmp_palette: str = 'none'
    if bmp_bpp == 8:
        bmp_palette = str(castData['palette_txt'])
    elif bmp_bpp == 2:
        bmp_palette = 'black and white'          

    # Check if the palette is a casting member number (custom palette)
    if bmp_palette.isnumeric():
        logging.debug('Using a custom palette: %s', bmp_palette)
        
    else:
        logging.debug('Using a default palette: %s', bmp_palette)


    if bmp_bpp in get_keys(DECODERS):
        return DECODERS[bmp_bpp].decode(fdata, bmp_width, bmp_height,
               bmp_padding_w, bmp_padding_h, bmp_palette, clutData)

    else:
        msg = vsprintf("Bad BPP value (%s)", bmp_bpp)
        logging.error(msg)
        raise ValueError(msg)

