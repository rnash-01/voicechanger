import unittest
import numpy as np
from scipy.fft import rfft, rfftfreq
import set_test_env
from postprocessing import *
from preprocessing import spectrogram

class TestPostprocessing(unittest.TestCase):
    def test_reverse_spectrogram_timestep(self):
        
        # Set up np random seed
        np.random.seed(0)

        # Set up some constants
        SAMP_RATE = 44100                                               # Sample rate of 44.1KHz
        WIN_SIZE = 2 * SAMP_RATE                                        # 2 seconds of audio
        
        # Create some random data, RFFT it
        input = np.random.randn(WIN_SIZE)
        spectrogram = rfft(input)[::-1]

        output = reverse_spectrogram_timestep(spectrogram, WIN_SIZE)
        
        self.assertEqual(input.shape, output.shape)
        self.assertIsInstance(input, np.ndarray)
        self.assertIsInstance(output, np.ndarray)
        
        # Get 10 random elements
        indices = np.random.randint(0, input.shape[0], 20).tolist()
        
        for i in indices:
            self.assertAlmostEqual(input[i], output[i])

        return
    
    def test_reverse_spectrogram(self):
        SAMP_RATE = 44100
        DURATION = 2
        WINDOW_SIZE = 2047/SAMP_RATE
        STRIDE = (((DURATION - WINDOW_SIZE))/256)
        
        ws_frames = int(WINDOW_SIZE * SAMP_RATE)
        st_frames = int(STRIDE * SAMP_RATE)
        d_frames = int(DURATION * SAMP_RATE)

        print((d_frames - ws_frames)//st_frames)

        FREQ = 100

        x = np.linspace(0, FREQ * DURATION * 2 * np.pi, DURATION * SAMP_RATE)
        y = np.sin(x)
        _, input = spectrogram(y, SAMP_RATE, WINDOW_SIZE, STRIDE, pad=True)
        output = reverse_spectrogram(input, SAMP_RATE, WINDOW_SIZE, STRIDE)

        self.assertLessEqual((np.abs(y.shape[0] - output.shape[0]))/y.shape[0], 0.01)
        self.assertAlmostEqual(y[0], output[0])

