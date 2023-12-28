# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from typing import List
from ..lingosrc.util import vsprintf


#
# Reads the palette information from a CLUT file and returns a list of colors
# =============================================================================
def clut2rgb(fdata: bytes) -> List[str]:
    """
    Parse a CLUT file and return its content as a colors list.
    
    Parameters
    ----------
    fdata : bytes
        The bytes in the CLUT file.
        
    Returns
    -------
    List[str]
        a list of colors in '#RRGGBB' format.

    Raises
    ------
    ValueError
        If some field inside the file is not compliant with the expected
        file structure. 
        
    """
    idx = 0
    palette = []
    while idx < len(fdata):
        r0 = fdata[idx]
        idx += 2
        g0 = fdata[idx]
        idx += 2            
        b0 = fdata[idx]
        idx += 2
        
        # Set colors in #RRGGBB format
        color = vsprintf('#%02x%02x%02x', r0, g0, b0)
        palette.append(color)

    
    return palette

#
# Reads the palette information from a CLUT file and returns a BMP palette
# =============================================================================
def clut2palette(fdata: bytes) -> bytes:
    """
    Parse a CLUT file and return its content as a BMP color palette.
    
    Parameters
    ----------
    fdata : bytes
        The bytes in the CLUT file.
        
    Returns
    -------
    bytes
        a 256 color palette for BMP files (BGRA format).

    Raises
    ------
    ValueError
        If some field inside the file is not compliant with the expected
        file structure. 
        
    """
    clutData = bytearray(256*4)
    idx = 0
    cindx = 0
    for _ in range(0, 256):
        r0 = fdata[idx]
        idx += 2
        g0 = fdata[idx]
        idx += 2            
        b0 = fdata[idx]
        idx += 2
        
        clutData[cindx] = b0
        cindx += 1
        clutData[cindx] = g0
        cindx += 1
        clutData[cindx] = r0
        cindx += 1
        clutData[cindx] = 0  # Alpha
        cindx += 1
    
    return clutData
