import math
from scipy.fft import rfft, rfftfreq
import numpy as np
import matplotlib.pyplot as plt
import audio

DEBUG=True

def spectrogram_timestep(data, samp_rate):
    # Converts audio wave values to a spectrogram - for simplicity, average
    # of channels is taken
    # data  -- np array of audio wave values of shape (nframes, nchannels)

    window_len = len(data)
    
    # Pass the frames through the appropriate FFT function
    yf = np.abs(rfft(data))
    xf = rfftfreq(window_len, 1/samp_rate)

    # Return spectogram embedding
    return xf, yf

def spectrogram(data, samp_rate, window_size, stride, pad=False):
    # Computes spectrogram for data along numerous timesteps
    # data          -- ndarray of audio data, np.int16 shape (nframes, channels)
    # samp_rate     -- number of audio frames captured per second, integer
    # window_size   -- size of the window *in seconds*
    # stride        -- how many frames to proceed by in each timestep
    # pad           -- whether or not to pad data with zeros if time_steps is initially non-integer, true/false

    sgram = []
    window_size_frames = int(window_size * samp_rate)
    time_steps = (len(data) - (window_size_frames))/stride + 1
    if (math.floor(time_steps) <= 0):
        return np.array([])

    if pad:
        excess = int(((time_steps) - math.floor(time_steps)) * stride)
        padding = stride - excess
        pad_array = np.zeros((padding,) + data.shape[1:])
        data = np.concatenate((data, pad_array), axis=0)
        time_steps = math.ceil(time_steps)
    else:
        time_steps = math.floor(time_steps)
    
    for i in range(time_steps):
        data_window = data[i*stride:window_size_frames + i*(stride)]
        xf, yf = spectrogram_timestep(data_window, samp_rate)
        sgram.append(yf)

    if DEBUG:
        plt.imsave("spectrogram.png", np.transpose(np.log(1+np.array(sgram))), cmap='inferno')


if DEBUG:
    duration = 5

    freq1 = 500
    freq2 = 700

    samp_rate = 44100
    x = np.linspace(0, duration, duration * samp_rate)
    y = np.sin(x * freq1 * 2 * np.pi) + 0.3 * np.sin(x * freq2 * 2 * np.pi)

    y_norm = np.int16((y/y.max()) * 32737)

    plt.plot(y_norm[:1000])
    plt.savefig("wave.png")
    plt.cla()

    spectrogram(y_norm, samp_rate, 0.5, 200, True)
