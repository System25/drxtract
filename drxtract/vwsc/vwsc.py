# Author: Abraham Macias Paredes
# E-mail: system252001@yahoo.es
# License: GNU GPL v2 (see LICENSE file for details).

from typing import Dict, List, Any
import struct
import math
import logging
from ..lingosrc.util import vsprintf
from .cparser import VwscChannelParser
from .dir4cparser import D4VwscChannelParser
from .dir5cparser import D5VwscChannelParser


CHANNEL_PARSERS: Dict[int, VwscChannelParser] = {
    20: D4VwscChannelParser(),
    24: D5VwscChannelParser()
}

#
# Reads from VWSC data the score elements
# =============================================================================
def parse_vwsc_data(fdata: bytes) -> List[Any]:
    """
    Parse a VWSC file score elements and return its content.
    
    Parameters
    ----------
    fdata : bytes
        The bytes in the VWSC file that contain the score elements.
        
    Returns
    -------
    List[Any]
        a dictionary that contains the data.

    Raises
    ------
    ValueError
        If some field inside the file is not compliant with the expected
        file structure. 
        
    """
    logging.debug("parse_vwsc_data ======================")
    vwsc_data: List[Any] = []
    
    idx = 0
    dataSize = struct.unpack(">i", fdata[idx:idx+4])[0]
    idx = idx + 4
    logging.debug("dataSize = %08x", dataSize)

    dataMarker = struct.unpack(">i", fdata[idx:idx+4])[0]
    idx = idx + 4
    logging.debug("dataMarker = %08x", dataMarker)

    if dataMarker != 0x14:
        raise ValueError('Can\'f find data marker in VWSC data!')
    
    if len(fdata) != dataSize:
        msg = vsprintf('Bad VWSC data size: (%d != %d)', len(fdata), dataSize)
        raise ValueError(msg)
        
    frame_count =  struct.unpack(">i", fdata[idx:idx+4])[0]
    idx += 4
    logging.debug("frame_count = %08x", frame_count)
    
    unknown01 =  struct.unpack(">h", fdata[idx:idx+2])[0]
    idx += 2
    logging.debug("unknown01 = %04x", unknown01)
    
    frame_size =  struct.unpack(">h", fdata[idx:idx+2])[0]
    idx += 2
    logging.debug("frame_size = %04x", frame_size)
    
    channel_count =  struct.unpack(">h", fdata[idx:idx+2])[0]
    idx += 2
    logging.debug("channel_count = %04x", channel_count)
    
    unknown02 =  struct.unpack(">h", fdata[idx:idx+2])[0]
    idx += 2
    logging.debug("unknown02 = %04x", unknown02)
    
    channelDataList = bytearray(channel_count * frame_size)
    
    cparser: VwscChannelParser = CHANNEL_PARSERS[frame_size]
    
    column = 0
    while idx < dataSize:
        column += 1
        logging.debug("column: %d idx: %08x", column, idx)
        channelSize = struct.unpack(">h", fdata[idx:idx+2])[0]
        idx = idx + 2
        logging.debug("channelSize: %d", channelSize)
        if channelSize == 2:
            logging.debug('This frame is equals to the previous one!')
            last_idx = len(vwsc_data) - 1
            vwsc_data.append(vwsc_data[last_idx])
            continue
        
        channelSize -= 2
        
        # Channel data
        if channelSize > 0:
            # Apply the differences from the previous channel
            while channelSize > 0:
                delta_size = struct.unpack(">h", fdata[idx:idx+2])[0]
                if (delta_size > channelSize) or (delta_size <= 0):
                    logging.warning("Delta size out of limits: %d > %d",
                                 delta_size, channelSize)
                    break
                idx = idx + 2
                delta_offset = struct.unpack(">h", fdata[idx:idx+2])[0]
                if delta_offset < 0:
                    delta_offset = (delta_offset & 0xFF)
                
                idx = idx + 2
                channelSize -= 4
            
                logging.debug("delta_size: %d", delta_size)
                logging.debug("delta_offset: %d", delta_offset)

                deltaData = fdata[idx:idx+delta_size]
                idx = idx + delta_size
                channelSize -= delta_size
                
                for i in range(0, delta_size):
                    p = delta_offset + i
                    channelDataList[p] = deltaData[i]
            
            vwsc_data.append(cparser.parse_vwsc_channels(channelDataList,
                                                         column))
            
        else:
            logging.debug('Empty channel!')
            vwsc_data.append([])
        
        idx += channelSize
        
    
    return vwsc_data

#
# Parse VWSC file data 
# =============================================================================
def parse_vwsc_file_data(fdata: bytes) -> List[Any]:
    """
    Parse a VWSC file data and return its content.
    
    Parameters
    ----------
    fdata : bytes
        The bytes in the VWSC file.
        
    Returns
    -------
    List[Any]
        a dictionary that contains the data.

    Raises
    ------
    ValueError
        If some field inside the file is not compliant with the expected
        file structure. 
        
    """
    # Check if the real VWSC data is wrapped into other data
    indx = 0
    dataSize = struct.unpack(">i", fdata[indx:indx+4])[0]
    indx = indx + 4
    
    dataMarker = struct.unpack(">i", fdata[indx:indx+4])[0]
    indx = indx + 4
    
    logging.debug("parse_vwsc_file ===========================================")
    logging.debug("dataSize: %d", dataSize)
    logging.debug("dataMarker: %d", dataMarker)
    
    if dataMarker != 0x14:
        # VWSC data is wrapped into other data (DIR file and not DRX file)
        if len(fdata) != dataSize:
            msg = vsprintf('Bad VWSC file size: (%d != %d)', len(fdata),
                          dataSize)
            raise ValueError(msg)
        
        unknown_01 =  struct.unpack(">i", fdata[indx:indx+4])[0]
        indx += 4
        logging.debug("unknown_01 = %08x", unknown_01)
        
        nmarkers =  struct.unpack(">i", fdata[indx:indx+4])[0]
        indx += 4
        logging.debug("nmarkers = %08x", nmarkers)
        
        nmarkers1 =  struct.unpack(">i", fdata[indx:indx+4])[0]
        indx += 4
        logging.debug("nmarkers1 = %08x", nmarkers1)
        
        lastMarker =  struct.unpack(">i", fdata[indx:indx+4])[0]
        indx += 4
        logging.debug("lastMarker = %08x", lastMarker)
        
        
        # Skip the markers because at this moment I don't know what are they
        # useful for
        indx += nmarkers1 * 4
        
        dataSize = struct.unpack(">i", fdata[indx:indx+4])[0]
        indx = indx + 4

        dataMarker = struct.unpack(">i", fdata[indx:indx+4])[0]
        indx = indx + 4
    
    if dataMarker != 0x14:
        raise ValueError('Can\'f find data marker in VWSC file!')
    
    indx -= 8
    data = fdata[indx:indx+dataSize]
    indx += dataSize
    
    # VWSC data structure depends on Director version
    vwsc_data = parse_vwsc_data(data)
    
    # Check of many data is left
    logging.debug('Data left: %d', len(fdata)-indx)
        
    return vwsc_data

#
# Converts VWSC data into a common score format 
# =============================================================================
def vwsc_to_score(vwsc_elements: List[Any]) -> Dict[str, Any]:
    """
    Converts a VWSC file data into a common score data format.
    
    Parameters
    ----------
    vwsc_elements : List[Any]
        VWSC file content.
        
    Returns
    -------
    Dict[str, Any]
        a dictionary that contains the score data.

    Raises
    ------
    ValueError
        If some field inside the file is not compliant with the expected
        file structure. 
        
    """
    # Transform the elements to the appropriate format
    data: Dict[str, Any] = {}
    data['lastChannel'] = 0
    data['lastFrame'] = len(vwsc_elements)
    if data['lastFrame'] > 0:
        data['lastChannel'] = len(vwsc_elements[0]['score'])
    
    data['transition'] = []
    data['palette'] = []
    data['sound1'] = []
    data['sound2'] = []
    data['tempo'] = []
    data['script'] = []
    data['sprite'] = []
    for i in range(0, data['lastChannel']):
        data['sprite'].append([])
        
    for i in range(0, data['lastFrame']):
        main = vwsc_elements[i]['main']
        if ('transition_id' in main and main['transition_id'] != ''):
            tran = {}
            tran['frame'] = i+1
            # TODO! Convert this into casting member
            tran['transition_id'] = main['transition_id']
            tran['transition_chunk_size'] = main['transition_chunk_size']
            tran['transition_duration'] = main['transition_duration']
            
            data['transition'].append(tran)
        
        if ('sound1_cast' in main and main['sound1_cast'] > 0):    
            
            prev = {}
            if len(data['sound1']) > 0:
                last_idx = len(data['sound1']) - 1
                if data['sound1'][last_idx]['endFrame'] == i:
                    prev = data['sound1'][last_idx]

            if (prev and prev['castId'] == main['sound1_cast']):
                # This is the same as the previous sound
                prev['endFrame'] = i+1
                
            else:
                # This is a new sound
                snd = {}
                snd['startFrame'] = i+1
                snd['endFrame'] = i+1
                snd['castId'] = main['sound1_cast']
                data['sound1'].append(snd)
            
        if ('sound2_cast' in main and main['sound2_cast'] > 0):
            prev = {}
            if len(data['sound2']) > 0:
                last_idx = len(data['sound2']) - 1
                if data['sound2'][last_idx]['endFrame'] == i:
                    prev = data['sound2'][last_idx]

            if (prev and prev['castId'] == main['sound2_cast']):
                # This is the same as the previous sound
                prev['endFrame'] = i+1
                
            else:
                # This is a new sound
                snd = {}
                snd['startFrame'] = i+1
                snd['endFrame'] = i+1
                snd['castId'] = main['sound2_cast']
                data['sound2'].append(snd)
          
        if ('script' in main and main['script'] > 0):
            scr = {}
            scr['frame'] = i+1
            scr['castId'] = main['script']
            data['script'].append(scr)
        
        if ('fps' in main and main['fps'] > 0):
            fps = {}
            fps['frame'] = i+1
            fps['fps'] = main['fps']
            data['tempo'].append(fps)
        
        if 'palette_id' in vwsc_elements[i]['palette']:
            pal = {}
            pal['frame'] = i+1
            pal['palette_id'] = vwsc_elements[i]['palette']['palette_id']
            data['palette'].append(pal)
        
    for i in range(0, data['lastFrame']):
        for j in range(0, data['lastChannel']):
            score = vwsc_elements[i]['score']
            if 'castId' in score[j]:
                sprite = {}
                sprite['castId'] = score[j]['castId']
                sprite['backColor'] = score[j]['backgroundColor']
                sprite['foreColor'] = score[j]['foregroundColor']
                sprite['width'] = score[j]['width']
                sprite['height'] = score[j]['height']
                sprite['ink'] = score[j]['ink_type']
                sprite['type'] = score[j]['spriteType']
                sprite['locH'] = score[j]['x']
                sprite['locV'] = score[j]['y']
                sprite['editable'] = score[j]['editable']
                sprite['moveable'] = score[j]['moveable']
                sprite['trails'] = score[j]['trails']
                
                prev = {}
                if len(data['sprite'][j]) > 0:
                    last_idx = len(data['sprite'][j]) - 1
                    if (data['sprite'][j][last_idx]['endFrame'] == i):
                        prev = data['sprite'][j][last_idx]
                    
                if (prev and prev['castId'] == sprite['castId'] and
                    prev['castId'] == sprite['castId'] and
                    prev['backColor'] == sprite['backColor'] and
                    prev['foreColor'] == sprite['foreColor'] and
                    prev['width'] == sprite['width'] and
                    prev['height'] == sprite['height'] and
                    prev['ink'] == sprite['ink'] and
                    prev['type'] == sprite['type'] and
                    prev['locH'] == sprite['locH'] and
                    prev['locV'] == sprite['locV'] and
                    prev['editable'] == sprite['editable'] and
                    prev['moveable'] == sprite['moveable'] and
                    prev['trails'] == sprite['trails']):
                    
                    # This is the same as previous sprite
                    prev['endFrame'] = i+1
                
                else:
                    # This is a new sprite
                    sprite['startFrame'] = i+1
                    sprite['endFrame'] = i+1
                    sprite['locZ'] = j+1
                    sprite['left'] = math.ceil(sprite['locH'] -
                                               sprite['width']/2)
                    sprite['top'] = math.ceil(sprite['locV'] -
                                              sprite['height']/2)
                    sprite['right'] = sprite['left'] + sprite['width']
                    sprite['bottom'] = sprite['top'] + sprite['height']

                    data['sprite'][j].append(sprite)
                    
    return data
