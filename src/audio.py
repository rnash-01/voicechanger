# This file contains functions to open, read from and write to WAVE files
import wave
import numpy as np
from data_conversion import *

def open_file(file):
    try:
        return wave.open(file)
    except:
        return None

def read(file, t):
    # Gets byte data from file and converts it to numpy array
    # file - open Wave_read object
    # t - length of time in seconds to extract from file
    NFRAMES = file.getnframes()         # Total number of frames in the file
    CHANNELS = file.getnchannels()      # Number of audio channels
    SAMPWIDTH = file.getsampwidth()     # Bytes per sample
    FRAMERATE = file.getframerate()     # Frames/second

    # Get bytes
    frames = file.readframes()

    # Convert to binary
    frames = hexToBinary(frames)
    
    # Convert to decimal/float
    frames = binaryToDec(frames)

    # Store in numpy array
    frames = np.array(frames)

    return frames
