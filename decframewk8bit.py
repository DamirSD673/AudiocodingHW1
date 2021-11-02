import pickle
from scipy.io import wavfile
import matplotlib.pyplot as plt
import numpy as np

def normalisation(signal):
    max_value = float(np.max(np.abs(signal)))
    normalized_signal = signal/max_value
    return normalized_signal

def decframewk8bit(file, fs):
    s = pickle.load(open(file, 'rb'), encoding='int8')
    s8bit_inds, step_size = s[0], s[1]
    s8bit = s8bit_inds * step_size
    return s8bit

    #wavfile.write('decoded_8bit.wav', fs, s)
