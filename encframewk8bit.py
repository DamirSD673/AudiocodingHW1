from scipy.io import wavfile
import pickle
import numpy as np

def encframewk8bit(file):
    rate, s = wavfile.read(file)
    new_data = (s / (2 ** 8) + 127).astype(np.uint8)
    pickle.dump(np.int8(new_data),
                open('encoded8bit.bin', 'wb'), protocol=1)
