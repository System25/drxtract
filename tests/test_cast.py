# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

#
# Unit test for CAST extraction
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
        ['<', 'd4tf0016'],
        ['<', 'd4tf0017'],
        ['<', 'd4tf0018'],
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
        ['<', 'd4rect0001'],
        ['<', 'd4rect0002'],
        ['<', 'd4rect0003'],
        ['<', 'd4rect0004'],
        ['<', 'd4rect0005'],
        ['<', 'd4rect0006'],
        ['<', 'd4rect0007'],
        ['<', 'd4rore0001'],
        ['<', 'd4oval0001'],
        ['<', 'd4line0001'],
    ])
    def test_shapes(self, byte_order: str, dir_name: str):
        dir_file = os.path.join('shape', dir_name, dir_name + ".DIR")
        json_file = os.path.join('shape', dir_name, "data.json")
        
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

    @parameterized.expand([
        ['<', 'apple', 0],
        ['<', 'appleInPipe', 0],
        ['<', 'bars', 1],
        ['<', 'line', 1],
        ['<', 'porteus', 0],
        ['<', 'superman', 1],
    ])
    def test_image(self, byte_order: str, dir_name: str, cast_idx: int):
        dir_file = os.path.join('bitmap', dir_name, dir_name + ".DIR")
        json_file = os.path.join('bitmap', dir_name, "data.json")
        bmp_file = os.path.join('bitmap', dir_name, dir_name + ".bmp")
        
        with open(json_file, mode='rb') as file:
            expectedData = json.loads(file.read().decode('utf-8'))
        
        with open(bmp_file, mode='rb') as file:
            expected_bmp = file.read()
        
        with open(dir_file, mode='rb') as file:
            fdata = file.read()
            
            # Parse the director file
            dirFile: DirectorFile = parse_dir_file_data(byte_order, 0, fdata)
            
            # Get the first element of the casting
            bmp = dirFile.cast[cast_idx]
            
            self.assertEqual(expectedData['type'], bmp['type'])
            self.assertEqual(expectedData['depth'], bmp['depth'])
            self.assertEqual(expectedData['content']['name'],
                             bmp['content']['name'])
            self.assertEqual(expectedData['width'], bmp['width'])
            self.assertEqual(expectedData['height'], bmp['height'])
            self.assertEqual(expectedData['locH'], bmp['locH'])
            self.assertEqual(expectedData['locV'], bmp['locV'])
            self.assertEqual(expectedData['top'], bmp['top'])
            self.assertEqual(expectedData['bottom'], bmp['bottom'])
            self.assertEqual(expectedData['left'], bmp['left'])
            self.assertEqual(expectedData['right'], bmp['right'])       
            self.assertEqual(expectedData['h_padding'], bmp['h_padding'])
            self.assertEqual(expectedData['w_padding'], bmp['w_padding'])
            self.assertEqual(expectedData['palette'], bmp['palette'])
            self.assertEqual(expectedData['palette_txt'], bmp['palette_txt'])

            self.assertEqual(expected_bmp, bmp['bitmap'])

    @parameterized.expand([
        ['<', 'factory', 0]
    ])
    def test_script(self, byte_order: str, dir_name: str, cast_idx: int):
        dir_file = os.path.join('script', dir_name, dir_name + ".DIR")
        json_file = os.path.join('script', dir_name, "data.json")
        lingo_file = os.path.join('script', dir_name, dir_name + ".lingo")
        js_file = os.path.join('script', dir_name, dir_name + ".js")
        
        with open(json_file, mode='rb') as file:
            expectedData = file.read().decode('utf-8')
        
        with open(lingo_file, mode='rb') as file:
            expected_lingo = file.read().decode('utf-8')
        
        with open(js_file, mode='rb') as file:
            expected_js = file.read().decode('utf-8')
        
        with open(dir_file, mode='rb') as file:
            fdata = file.read()
            
            # Parse the director file
            dirFile: DirectorFile = parse_dir_file_data(byte_order, 0, fdata)
            
            # Get the first element of the casting
            lscr = dirFile.cast[cast_idx]
            actualData = json.dumps(lscr, indent=4, sort_keys=True)
            
            self.assertEqual(expectedData, actualData)

            # Check lingo script reference
            lscr_idx = lscr['content']['basic']['script_index'] - 1            
            self.assertEqual(expected_lingo, dirFile.lingoScr[lscr_idx])
            
            self.assertEqual(expected_js, dirFile.jsScr[lscr_idx])
