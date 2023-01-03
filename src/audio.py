# This file contains functions to open, read from and write to WAVE files
import wave
import numpy as np
import os
from data_conversion import *

def frames_from_binary(string, file_params):

    channels, sampwidth = file_params
    sampwidth_bits = sampwidth * 8
    strlen = len(string)
    if (strlen == 0):
        return None

    # Check that there is actually an even split
    if strlen/(channels * sampwidth_bits) != strlen//(channels * sampwidth_bits):
        raise Exception('Binary string cannot be split evenly')
    
    # Now go through and split up the binary string into:
    # [[channel1_string, channel2_string, ..., channel_n_string], ...]
    # (an array containing one array for each frame, with one string for each channel)
    nframes = strlen//(channels * sampwidth_bits)
    frames = np.empty((nframes, channels), np.int32)

    for i in range(nframes):
        frame_string = string[i * channels * sampwidth_bits:(i+1) * channels * sampwidth_bits]
        for j in range(channels):
            channel_string = frame_string[j * sampwidth_bits:(j+1) * sampwidth_bits]
            frames[i][j] = binary_to_decimal(channel_string, big_endian=True)

    return frames

def open_file(file):

    try:
        return wave.open(file)
    except:
        return None

def open_write(file, channels, sampwidth, framerate):
    # file      -- name of the file to write to
    # channels  -- number of channels of the file
    # sampwidth -- number of bytes per frame
    # framerate -- number of frames per second

    try:
        f = wave.open(file, 'wb')
        f.setnchannels(channels)
        f.setsampwidth(sampwidth)
        f.setframerate(framerate)
        return f
    except:
        return None

def read(file, nframes):

    # Gets byte data from file and converts it to numpy array
    # file  -- open Wave_read object
    # t     -- length of time in seconds to extract from file
    NFRAMES = file.getnframes()         # Total number of frames in the file
    CHANNELS = file.getnchannels()      # Number of audio channels
    SAMPWIDTH = file.getsampwidth()     # Bytes per sample
    FRAMERATE = file.getframerate()     # Frames/second

    # Get bytes
    frames = file.readframes(nframes)

    # Convert to binary and split into frames into decimal data
    frames = bytes_to_binary(frames)
    
    try:
        frames = frames_from_binary(frames, (CHANNELS, SAMPWIDTH))
    except:
        frames = None

    return frames

def write(file, frames):

    # Writes data to file
    # file      -- open Wave_write object
    # frames    -- buffer of decimal frame data with shape (nframes, nchannels)

    # Normalise frames to sampwidth
    sampwidth = file.getsampwidth()
    bits = sampwidth * 8
    max_val = 0.8 * (2**(bits-1) - 1)

    data_norm = np.int32(((frames - np.min(frames))/(np.max(frames) - np.min(frames)) * 2 - 1) * max_val)

    # Convert to bytes
    byte_frames = bytearray()

    for i in range(frames.shape[0]):
        frame = data_norm[i, :]
        hex_data = b''
        for c in range(frames.shape[1]):
            channel = frame[c]
            binary_string = decimal_to_binary(channel, sampwidth, big_endian=True, signed=True)
            hex_data += binary_to_bytes(binary_string)[::-1]

        
        # Write frame_bytes to file
        file.writeframes(hex_data)
    
    