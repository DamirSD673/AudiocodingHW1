from scipy.io import wavfile
import pickle


rate, s = wavfile.read('Track16.wav')
binaryfile = pickle.dump(s, open('encoded.bin', 'wb'), protocol=1)
