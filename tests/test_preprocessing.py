import unittest
import numpy as np
import set_test_env
from preprocessing import *

class TestPreprocessing(unittest.TestCase):
    def test_spectrogram_timestep(self):
        
        # Generate 5 seconds of 44.1KHz audio, containing two sine waves: 1233Hz and 734Hz
        # The 734Hz tone is made less powerful to allow 1233Hz to be the 'argmax' value
        SAMP_RATE = 44100
        DURATION = 5
        freq1 = 1233
        freq2 = 734

        x = np.linspace(0, 5, DURATION * SAMP_RATE)
        y = np.sin(x * freq1 * 2 * np.pi) + 0.5 * np.sin(x * freq2 * 2 * np.pi)

        # For good measure, normalise y
        y_norm = np.int16(y/np.max(y) * 32767)
        
        xf, yf = spectrogram_timestep(y_norm, SAMP_RATE)

        self.assertEqual(yf.shape[0], y.shape[0]//2 + 1)
        self.assertAlmostEqual(xf[np.argmax(yf)], freq1)

        # Squash frequency down, 734 should be the next highest after
        yf[np.argmax(yf)] = 0

        self.assertAlmostEqual(xf[np.argmax(yf)], freq2)

        # Generate 1 second of 44.1KHz audio, where it is completely silent
        y = np.zeros(x.shape[0])

        xf, yf = spectrogram_timestep(y, SAMP_RATE)
        self.assertEqual(np.max(yf), 0)

    def test_spectrogram_values(self):
        
        # Generate 5 seconds of 44.1KHz audio.
        # The first half plays a 700Hz tone.
        # The second half plays a 1450Hz tone.
        SAMP_RATE = 44100
        DURATION = 5
        freq1 = 700
        freq2 = 1450

        x = np.linspace(0, 5, DURATION * SAMP_RATE)
        y = np.sin(x[:int(2.5 * 44100)] * freq1 * 2 * np.pi)
        y = np.concatenate((y, np.sin(x[int(2.5*44100):] * freq2 * 2 * np.pi)), axis=0)
        
        xf, yf = spectrogram(y, SAMP_RATE, 0.5, 0.25, False)
        yf_1 = yf[:yf.shape[0]//2]
        yf_2 = yf[yf.shape[0]//2:]
        
        # Get midpoint samples of each 'half'
        mid_1 = yf_1[yf_1.shape[0]//2]
        mid_2 = yf_2[yf_2.shape[0]//2]

        self.assertAlmostEqual(xf[np.argmax(mid_1)], 700)
        self.assertAlmostEqual(xf[np.argmax(mid_2)], 1450)

    def test_spectrogram_shape(self):
        
        # Generate ascending tone from 100Hz to 2000Hz over 10 seconds
        SAMP_RATE = 44100
        DURATION = 10
        F_START = 100
        F_END = 2000

        x = np.linspace(0, DURATION, DURATION * SAMP_RATE)
        freq_range = np.linspace(F_START, F_END, DURATION * SAMP_RATE)
        y = np.sin(x * freq_range * 2 * np.pi)

        # Test 1: Parameters that make sliding window fit perfectly in audio
        # Sliding window: 0.5 seconds wide (22050 frames)
        # Stride: 0.25 seconds (11025 frames)
        # This results in 39 time steps (DURATION * SAMP_RATE - 0.5 * SAMP_RATE)/(0.25 * SAMP_RATE) + 1
        xf, yf_1 = spectrogram(y, SAMP_RATE, 0.5, 0.25, False)
        _, yf_2 = spectrogram(y, SAMP_RATE, 0.5, 0.25, True)

        self.assertEqual(yf_1.shape[0], yf_2.shape[0]) # Expect that the padding made no difference as it was not needed
        self.assertEqual(yf_1.shape[0], 39)

        # Test 2: Parameters that make sliding window lose a small excess
        # Sliding window: 0.5 seconds wide (22050 frames)
        # Stride: 0.255 (11245.5 frames - will be floored to 11245 frames by spectrogram)
        # The expected number of timesteps is 38 without padding, and 39 with padding
        xf, yf_1 = spectrogram(y, SAMP_RATE, 0.5, 0.255, False)
        _, yf_2 = spectrogram(y, SAMP_RATE, 0.5, 0.255, True)

        self.assertEqual(yf_1.shape[0], 38)
        self.assertEqual(yf_2.shape[0], 39)


