# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

#
# Unit test for RIFF extraction
#

import unittest
import os
import json
import wave
from parameterized import parameterized

from drxtract.dir import parse_dir_file_data, DirectorFile


class TestScript(unittest.TestCase):
    
    maxDiff = None
    
    def setUp(self):
        os.chdir(os.path.join(os.path.dirname(__file__), 'files', 'cast'))
    

    @parameterized.expand([
        ['<', 'd4tf0001'],
        ['<', 'd4tf0002'],
        ['<', 'd4tf0003'],
        ['<', 'd4tf0004'],
        ['<', 'd4tf0005'],
        ['<', 'd4tf0006'],
        ['<', 'd4tf0007'],
        ['<', 'd4tf0008'],
        ['<', 'd4tf0009'],
        ['<', 'd4tf0010'],
        ['<', 'd4tf0011'],
        ['<', 'd4tf0012'],
        ['<', 'd4tf0013'],
        ['<', 'd4tf0014'],
        ['<', 'd4tf0015'],
    ])
    def test_text_fields(self, byte_order: str, dir_name: str):
        dir_file = os.path.join('text', dir_name, dir_name + ".DIR")
        json_file = os.path.join('text', dir_name, "data.json")
        
        with open(json_file, mode='rb') as file:
            expectedData = file.read().decode('utf-8')
        
        with open(dir_file, mode='rb') as file:
            fdata = file.read()
            
            # Parse the director file
            dirFile: DirectorFile = parse_dir_file_data(byte_order, 0, fdata)
            
            # Get the first element of the casting
            actualData = json.dumps(dirFile.cast[0], indent=4, sort_keys=True)
            
            
        #with open(os.path.join('text', dir_name, "test.json"), mode='wb') as file:
        #    file.write(actualData.encode('utf-8'))
        
            self.assertEqual(expectedData, actualData)

    @parameterized.expand([
        ['<', 'd4bt0001'],
        ['<', 'd4bt0002'],
        ['<', 'd4bt0003'],
        ['<', 'd4bt0004']
    ])
    def test_buttons(self, byte_order: str, dir_name: str):
        dir_file = os.path.join('button', dir_name, dir_name + ".DIR")
        json_file = os.path.join('button', dir_name, "data.json")
        
        with open(json_file, mode='rb') as file:
            expectedData = file.read().decode('utf-8')
        
        with open(dir_file, mode='rb') as file:
            fdata = file.read()
            
            # Parse the director file
            dirFile: DirectorFile = parse_dir_file_data(byte_order, 0, fdata)
            
            # Get the first element of the casting
            actualData = json.dumps(dirFile.cast[0], indent=4, sort_keys=True)
            
            
        #with open(os.path.join('text', dir_name, "test.json"), mode='wb') as file:
        #    file.write(actualData.encode('utf-8'))
        
            self.assertEqual(expectedData, actualData)
            
    @parameterized.expand([
        ['<', 'd4sn0001'],
        ['<', 'd4sn0002']
    ])
    def test_sound(self, byte_order: str, dir_name: str):
        dir_file = os.path.join('sound', dir_name, dir_name + ".DIR")
        json_file = os.path.join('sound', dir_name, "data.json")
        wav_file = os.path.join('sound', dir_name, "sound.wav")
        
        with open(json_file, mode='rb') as file:
            expectedData = json.loads(file.read().decode('utf-8'))
        
        with open(dir_file, mode='rb') as file:
            fdata = file.read()
            
            # Parse the director file
            dirFile: DirectorFile = parse_dir_file_data(byte_order, 0, fdata)
            
            # Get the first element of the casting
            elm = dirFile.cast[0]
            self.assertEqual(expectedData['type'], elm['type'])
            self.assertEqual(expectedData['loop'], elm['loop'])
            self.assertEqual(expectedData['content']['name'],
                             elm['content']['name'])
            sound = elm['sampled_sound']
            self.assertEqual(expectedData['channelCount'], sound.num_channels)
            self.assertEqual(expectedData['sampleRate'], sound.sample_rate)
            self.assertEqual(expectedData['sampleSize'], sound.bits_per_sample)

            # Compare sounds
            wavef = wave.open(wav_file,'r')
            self.assertEqual(wavef.getnchannels(), sound.num_channels)
            self.assertEqual(wavef.getsampwidth(), int(sound.bits_per_sample/8))
            self.assertEqual(wavef.getframerate(), sound.sample_rate)

            wav_frames = wavef.readframes(wavef.getnframes())
            self.assertEqual(wav_frames, sound.samples)

            wavef.close()

            
