# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from ..ast import Node
from typing import List, Optional

#
# Lingo script decompiler context.
#
class Context:
    """This class represents the context of the Lingo script decompiler"""
    
    def __init__(self):
        self.constants: List[str] = []
        self.bytes_per_constant: int = None
        self.name_list: List[str] = []
        self.local_func_names: List[str] = []
        self.properties: List[str] = []
        self.tell_object: Optional[Node] = None
