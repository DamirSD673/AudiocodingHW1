import os
from scipy.io import wavfile
import pickle
import numpy as np

def encframewk8bit(file):
    rate, s = wavfile.read(file)
    new_data = (s / (2 ** 8) + 127).astype(np.uint8)
    pickle.dump(np.int8(new_data),
                open('encoded8bit.bin', 'wb'), protocol=1)
    print('Wav-file size is', os.path.getsize('Track16.wav'), '\n',
          '8bit Bin-file size is', os.path.getsize('encoded8bit.bin'),'\n',
          'Initial bin-file size is', os.path.getsize('encoded.bin'))
