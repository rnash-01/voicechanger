import numpy as np
import unittest
import set_test_env
from dataset import *
from hyperparams import *
from audio import *

class TestDataset(unittest.TestCase):

    def setUp(self):

        # Get duration and sampling rate of "test_dataset.wav"
        self.FNAME = "../src/audio/test_dataset.wav"
        f = open_file(self.FNAME)
        self.SAMP_RATE = f.getframerate()
        self.NFRAMES = f.getnframes()
        f.close()

    def test_create_dataset_normal(self):
        
        # Test to see if a normal file (whose length is longer than the 
        # specified file window size)

        dataset = create_dataset(self.FNAME, FILE_WINDOW_SIZE, FILE_STRIDE_SIZE)
        
        # Calculate number of expected examples
        f_win_size_frames = FILE_WINDOW_SIZE * self.SAMP_RATE
        f_stride_frames = FILE_STRIDE_SIZE * self.SAMP_RATE
        expected_examples = (self.NFRAMES - f_win_size_frames) // f_stride_frames + 1

        self.assertEqual(dataset[1].shape[0], expected_examples)
    
    def test_create_dataset_short(self):
        
        # Test to see if a file whose length is shorter than the specified file
        # window size

        dataset = create_dataset(self.FNAME, 6, 6/4)

        expected_examples = 1
        self.assertEqual(dataset[1].shape[0], expected_examples)
