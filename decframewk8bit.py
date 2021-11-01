import pickle
from scipy.io import wavfile

def decframewk8bit(file, fs):
    s = pickle.load(open(file, 'rb'), encoding='int8')
    wavfile.write('decoded_8bit.wav', fs, s)
