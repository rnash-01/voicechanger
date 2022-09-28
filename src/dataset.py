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
    freq_ubound = int(10000/SAMP_RATE * ((WIN_SIZE * SAMP_RATE)/2))             # Typical human speech shouldn't really be exceeding 10000Hz
    
    f_win_size_frames = int(FILE_WINDOW_SIZE * SAMP_RATE)
    f_stride_frames = int(FILE_STRIDE_SIZE * SAMP_RATE)
    num_examples = (len(frames) - f_win_size_frames)//f_stride_frames + 1
    num_examples = np.max([num_examples, 0])                                    # if num_examples is negative, that means the window size is 
                                                                                # greater than the number of frames

    # Loop over audio in FILE_WINDOW_SIZE second intervals
    for i in range(num_examples):
        lbound = i * int(FILE_STRIDE_SIZE * SAMP_RATE)
        ubound = int(f_win_size_frames + i * f_stride_frames)
        ubound = np.min([ubound, frames.shape[0]])
        window = frames[lbound:ubound]
    
        print(lbound, ubound, len(window))
        xf, yf = spectrogram(window, SAMP_RATE, WIN_SIZE, STRIDE)
        dataset.append(yf[:, -freq_ubound:])
        print(yf.shape)
    
    # Normalize data on a logarithmic scale
    dataset = np.array(dataset)
    diff = np.max(dataset) - np.min(dataset)
    mini = diff/(np.exp(8) - 1)                                                 # ^1
    dataset = np.log(dataset + mini)

    return (xf[:freq_ubound], np.array(dataset))

xf, dataset = create_dataset('audio/donkey kong punch.wav')
for i, yf in enumerate(dataset):
    plt.imsave(f"spectrogram_real_{i}.png", np.transpose(yf), cmap='inferno')

# Footnotes
# 1 the number contained in np.exp(x) denotes how many powers of e the resulting spectrogram values should range over.
# this is useful because it allows use to control how significant a change in intensity is. The more powers of e to range over,
# the larger change in intensity needed to display a significantly different value.
# For example, if we're ranging over 1 power of e, and say our data's minimum was conveniently e^1: then the resulting range would be
# however much we would have to add to our minimum to bring our result to 2 - i.e., to get to the next power of e, e^2