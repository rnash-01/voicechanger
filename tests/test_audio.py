# Following snippet from: https://stackoverflow.com/a/1897665
import unittest
from wave import Wave_read, Wave_write
import set_test_env
from audio import *
import os

# Ensure that random operations are consistent
np.random.seed(0)

class TestAudio(unittest.TestCase):
    
    def test_frames_from_binary(self):
        # Two stereo 16-bit frames of data in binary format:
        input = '1100001100001100011111101010000100101011000111011110000110001110'
        expected = np.array([[-15604, 32417], [11037, -7794]])
        equality = np.array_equal(frames_from_binary(input, (2, 2)), expected)
        print(expected)
        print(frames_from_binary(input, (2,2)))
        self.assertTrue(equality)

        # Four stereo 16-bit frames
        input = '00100100101001110010011110010001111101100111001001010111110101110101101100111011010001001000010111011101110000110000001100001110'
        expected = np.array([[9383, 10129], [-2446, 22487], [23355, 17541], [-8765, 782]])
        equality = np.array_equal(frames_from_binary(input, (2, 2)), expected)
        self.assertTrue(equality)

        # Empty string
        input = ''
        expected = None
        equality = frames_from_binary(input, (2, 2)) == expected
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

    def test_open_write(self):

        # Make sure it can open a file, existing or not.
        TEST_FILE = 'assets/OPEN_WRITE_TEST_FILE.wav'

        # Initially, file does not exist. On second interation, it does. Both times assertions should
        # show it is not None

        for i in range(2):
            file = open_write('assets/WRITE_TEST_FILE.wav', 1, 2, 44100)
            self.assertIsNotNone(file)
            self.assertIsInstance(file, Wave_write)
            file.close()
        
        # Get rid of file
        if (os.path.exists(TEST_FILE)):
            os.remove(TEST_FILE)

    def test_read(self):
        # Make sure it can read from a valid file
        file = wave.open('assets/sine.wav')
        SAMPWIDTH = file.getsampwidth()
        CHANNELS = file.getnchannels()
        frames = read(file, 1)
        self.assertIsNotNone(frames)
        self.assertIsInstance(frames, np.ndarray)
        self.assertEqual(frames.shape, (1, CHANNELS))

    def test_write(self):

        TEST_FILE = 'assets/WRITE_TEST_FILE_SINE.wav'
        if os.path.exists(TEST_FILE):
            os.remove(TEST_FILE)
        
        DURATION = 3
        FREQ = 1000
        FRAMERATE = 44100
        SAMPWIDTH = 2
        CHANNELS = 1

        x = np.linspace(0, DURATION * FREQ * 2 * np.pi, FRAMERATE * DURATION)
        y = np.sin(x)
        
        y = np.reshape(y, (-1, 1))
        print(y.shape)

        f = open_write(TEST_FILE, CHANNELS, SAMPWIDTH, FRAMERATE)
        write(f, y)
        f.close()


if __name__ == '__main__':
    unittest.main()