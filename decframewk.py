import pickle
from scipy.io import wavfile


fs = 16000

s = pickle.loads('encoded.bin')

wavfile.write('decoded.bin', fs, s)
