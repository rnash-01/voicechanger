# This file uses functions from audio.py, data_conversion.py and preprocessing.py to
# create a dataset - namely, an array of groups of spectrographic timesteps from a single audio file
import numpy as np
import matplotlib.pyplot as plt
from audio import *
from preprocessing import *
from hyperparams import *

def create_dataset(filename):
    # Open file and get sample rate and duration
    audio_file = open_file(filename)
    SAMP_RATE = audio_file.getframerate()
    NFRAMES = audio_file.getnframes()
    DURATION = NFRAMES/SAMP_RATE

    WIN_SIZE = 0.05
    STRIDE = WIN_SIZE/4

    x = np.linspace(0, DURATION, NFRAMES)
    frames = read(audio_file, NFRAMES)

    dataset = []
    
    # Loop over audio in FILE_WINDOW_SIZE second intervals
    xf, yf = spectrogram(frames, SAMP_RATE, WIN_SIZE, STRIDE)

    diff = np.max(yf) - np.min(yf)
    mini = diff/(np.exp(10) - 1)
    yf = np.log(yf + mini)

    return xf, yf

xf, yf = create_dataset('audio/donkey kong punch.wav')
plt.imsave("spectrogram_real.png", np.transpose(yf), cmap='inferno')