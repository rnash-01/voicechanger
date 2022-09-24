# This file contains functions to open, read from and write to WAVE files
import wave
import numpy as np
from data_conversion import *

print(__name__)

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
            frames[i][j] = binary_to_decimal(channel_string)

    return frames

def open_file(file):
    try:
        return wave.open(file)
    except:
        return None

def read(file, nframes):
    # Gets byte data from file and converts it to numpy array
    # file - open Wave_read object
    # t - length of time in seconds to extract from file
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
