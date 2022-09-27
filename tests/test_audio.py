# Following snippet from: https://stackoverflow.com/a/1897665
import unittest
from wave import Wave_read
import set_test_env
from audio import *

# Ensure that random operations are consistent
np.random.seed(0)

class TestAudio(unittest.TestCase):
    
    def test_frames_from_binary(self):
        # Two stereo 16-bit frames of data in binary format:
        input = '1100001100001100011111101010000100101011000111011110000110001110'
        expected = np.array([[12483, -31362], [-18220, 29063]])
        equality = np.array_equal(frames_from_binary(input, (2, 2)), expected)
        print(equality)
        self.assertTrue(equality)

        # Four stereo 16-bit frames
        input = '00100100101001110010011110010001111101100111001001010111110101110101101100111011010001001000010111011101110000110000001100001110'
        expected = np.array([[-6876, -30236], [20079, -5142], [-8998, -24286], [-15429, 28864]])
        equality = np.array_equal(frames_from_binary(input, (2, 2)), expected)
        print(equality)
        self.assertTrue(equality)

        # Empty string
        input = ''
        expected = None
        equality = frames_from_binary(input, (2, 2)) == expected
        print(equality)
        self.assertTrue(equality)

        # Alphanumeric characters
        input = 'Hello, this is a pretty bad string, 99!'
        self.assertRaises(Exception, frames_from_binary, (input, (2, 2)))

        # Uneven parameters
        input = '1100001100001100011111101010000100101011000111011110000110001110'
        self.assertRaises(Exception, frames_from_binary, (input, (2, 3)))


    def test_open_file(self):
        
        # Make sure that it CAN open an existing file
        file = open_file('assets/sine.wav')
        self.assertIsNotNone(file)
        self.assertIsInstance(file, Wave_read)
        file.close()

        # Make sure it returns None if file does not exist
        file = open_file('i_don\'t_exist.wav')
        self.assertIsNone(file)

    def test_read(self):
        # Make sure it can read from a valid file
        file = wave.open('assets/sine.wav')
        SAMPWIDTH = file.getsampwidth()
        CHANNELS = file.getnchannels()
        frames = read(file, 1)
        self.assertIsNotNone(frames)
        self.assertIsInstance(frames, np.ndarray)
        self.assertEqual(frames.shape, (1, CHANNELS))


if __name__ == '__main__':
    unittest.main()