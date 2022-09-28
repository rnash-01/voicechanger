import math
from scipy.fft import rfft, rfftfreq
import numpy as np
import matplotlib.pyplot as plt
import audio

DEBUG=False

def spectrogram_timestep(data, samp_rate):

    # Converts audio wave values to a spectrogram - for simplicity, average
    # of channels is taken
    # data  -- np array of audio wave values of shape (nframes, nchannels)

    window_len = data.shape[0]
    
    # Pass the frames through the appropriate FFT function
    yf = np.abs(rfft(data))[::-1]
    xf = rfftfreq(window_len, 1/samp_rate)

    # Return spectogram embedding
    return xf, yf

def spectrogram(data, samp_rate, window_size, stride, pad=False):

    # Computes spectrogram for data along numerous timesteps
    # data          -- ndarray of audio data, np.int16 shape (nframes, [channels])
    # samp_rate     -- number of audio frames captured per second, integer
    # window_size   -- size of the window *in seconds*
    # stride        -- how many frames to proceed by in each timestep
    # pad           -- whether or not to pad data with zeros if time_steps is initially non-integer, true/false
    # Returns the range of frequencies measured and the spectrogram itself

    # Ensure that audio data does not have multiple channels
    if (data.ndim == 2):
        data = np.mean(data, axis=1)
    elif (data.ndim > 2):
        return (np.array([]), np.array([]))

    sgram = []
    window_size_frames = int(window_size * samp_rate)
    stride_frames = int(stride * samp_rate)
    time_steps = (len(data) - (window_size_frames))/stride_frames + 1
    if (math.floor(time_steps) <= 0):
        return (np.array([]), np.array([]))

    if pad:
        excess = int(((time_steps) - math.floor(time_steps)) * stride_frames)
        padding = stride_frames - excess
        if padding < stride_frames:
            pad_array = np.zeros((padding,) + data.shape[1:])
            data = np.concatenate((data, pad_array), axis=0)
            time_steps = math.ceil(time_steps)
        else:
            time_steps = math.floor(time_steps)
    else:
        time_steps = math.floor(time_steps)
    
    for i in range(time_steps):
        data_window = data[i*stride_frames:window_size_frames + i*(stride_frames)]
        # if (np.max(data_window) > 0):
        #     data_window = (data_window/np.max(data_window))

        xf, yf = spectrogram_timestep(data_window, samp_rate)

        sgram.append(yf)
    

    if DEBUG:
        plt.imsave("spectrogram.png", np.transpose(np.log(1+np.array(sgram)/np.array(sgram).max())), cmap='viridis')

    return xf, np.array(sgram)

if DEBUG:
    duration = 5

    freqs = [(400, 0.3), (700, 0.4), (1000, 0.1), (5000, 0.2)]

    samp_rate = 44100
    x = np.linspace(0, duration, duration * samp_rate)
    y = np.empty((x.shape[0], 2))
    for fw in freqs:
        freq, weight = fw
        y[:, 0] += weight * np.sin(x * freq * 2 * np.pi)
    y[:, 1] = y[:, 0]

    y_norm = np.int16((y/y.max()) * 32737)

    plt.plot(y_norm[:1000])
    plt.savefig("wave.png")
    plt.cla()

    spectrogram(y_norm, samp_rate, 0.05, 200/44100, False)