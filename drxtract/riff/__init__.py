# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from .riff_chunk import parse_chunk_id, Chunk
from .riff import RiffData, parse_riff
from .imap import InputMAP, parse_imap
from .mmap import MemoryMAP, parse_mmap, MMapResource
