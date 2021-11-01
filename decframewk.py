import pickle
from scipy.io import wavfile


fs = int(16e3)

s = pickle.loads('encoded.bin')

wavfile.write('decoded.bin', fs, s)
