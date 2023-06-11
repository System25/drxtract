# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

#
# Lingo script header.
#
class Header:
    """This class represents the content of the Lingo script header"""
    
    def __init__(self):
        self.prb_offset: int = -1
        """Offset to the properties records block"""
        
        self.frb_offset: int = -1
        """Offset to the function records block"""
        
        self.frb_nrecords: int = -1
        """Number of function records"""
        
        self.crb_nconstants: int = -1
        """Number of constants"""
        
        self.crb_offset: int = -1
        """Offset to the constant records block"""
        
        self.con_offset: int = -1
        """Base address for constant data"""
        
        self.grb_nrecords: int = -1
        """Number of global vars in the header"""
        
        self.grb_offset: int = -1
        """Offset to the global vars records block"""
        
        self.bytes_per_constant: int = -1
        """Bytes per constant in the constant record block"""
        
        
        
        