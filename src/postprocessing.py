from scipy.fft import irfft
import numpy as np
def reverse_spectrogram_timestep(data, win_size):
    return irfft(data[::-1], int(win_size))

def reverse_spectrogram(data, samp_rate, window_size, stride):
    
    ws_frames = int(window_size * samp_rate)
    st_frames = int(stride * samp_rate)
    # First, get individual windows of audio
    audio_windows = []
    for i in range(data.shape[0]):
        spec = data[i, :]
        audio = reverse_spectrogram_timestep(spec, window_size * samp_rate)
        audio_windows.append(audio)
    
    # Now merge
    frames = []
    frames += audio_windows[0].tolist()
    for ind, snippet in enumerate(audio_windows[1:]):
        # Before any appending, merge the overlapping segment with where we are in frames
        
        # Get start and end, relative to the frames array
        i = ind + 1
        start = i * st_frames
        end = ws_frames + (ind * st_frames)
        overlay_size = end - start

        if (overlay_size < 0):

            # Get the data to merge with the main frames array
            merge_snippet = snippet[:overlay_size]
            
            # Weight should start near 0 and end near 1 - sigmoid_offset achieves this for us
            sigmoid_offset = overlay_size//2

            # Now merge!
            for j in range(overlay_size):
                w = 1/(1 + np.exp(-(j - sigmoid_offset)))
                d0 = frames[start + j]
                d1 = merge_snippet[j]
                merge = (1. - w) * d0 + w * d1
                frames[start + j] = merge

            overlay_size = 0
        # Now append whatever is left to the end of frames
        remaining_snippet = snippet[overlay_size:]
        frames += remaining_snippet.tolist()

    return np.array(frames)
