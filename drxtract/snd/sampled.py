# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

SAMPLE_RATE_11_KHZ = 11127
SAMPLE_RATE_16_KHZ = 16000
SAMPLE_RATE_22_KHZ = 22254
SAMPLE_RATE_44_KHZ = 44100

#
# Sampled sound class.
# 
class SampledSound:
    """This class represents a sampled sound"""
    
    def __init__(self):
        self.num_channels: int = 1
        """Number of channels"""
    
        self.bits_per_sample: int = 8
        """Bits per sample"""

        self.sample_rate: int = SAMPLE_RATE_16_KHZ
        """Sample rate"""

        self.samples: bytes = bytes()
        """Sound samples"""
