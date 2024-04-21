# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from typing import List
import struct
import logging
from ..lingosrc.util import Dictionary

#
# Marker class.
# 
class Marker(Dictionary):
    """This class represents a marker in the score"""
    
    def __init__(self, name: str, frame: int):
        super().__init__()
        self['name'] = name
        self['frame'] = frame

#
# Reads from VWLB file the markers channel of the score and its frame
# =============================================================================
def parse_vwlb_data(fdata: bytes) -> List[Marker]:
    """
    Parse a VWLB file and return its content.
    
    Parameters
    ----------
    fdata : bytes
        The bytes in the VWLB file that contain the marker elements.
        
    Returns
    -------
    List[Marker]
        a dictionary that contains the data.

    Raises
    ------
    ValueError
        If some field inside the file is not compliant with the expected
        file structure. 
        
    """
    logging.debug("parse_vwsc_data ======================")
    vwlb_data: List[Marker] = []
    
    indx = 0
    nmarkers = struct.unpack(">h", fdata[(indx):(indx+2)])[0]
    indx = indx + 2
    logging.debug("N Markers: %d", nmarkers)
    
    mnidx = 2 + 4 * (nmarkers + 1)
    
    for _ in range(0, nmarkers):
        frame = struct.unpack(">h", fdata[(indx):(indx+2)])[0]
        indx = indx + 2
        logging.debug("Frame: %d", frame)
        
        name_start = mnidx + struct.unpack(">h", fdata[(indx):(indx+2)])[0]
        indx = indx + 2
        logging.debug("name_start: %d", name_start)
        
        name_end = mnidx + struct.unpack(">h", fdata[(indx+2):(indx+4)])[0]
        logging.debug("name_end: %d", name_end)
        
        name = fdata[name_start:name_end].decode('utf-8')
        logging.debug("Name: %s", name)
        
        vwlb_data.append(Marker(name, frame))
    
    return vwlb_data
