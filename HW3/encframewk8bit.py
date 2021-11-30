import os
from scipy.io import wavfile
import pickle
import numpy as np

def encframewk8bit(file):
    rate, s = wavfile.read(file)
    step = (float(np.max(s)) - float(np.min(s))) / 2**8
    s8bit = (s/step).astype(np.int8)
    pickle.dump([s8bit, step],
                open('encoded8bit.bin', 'wb'))
    print('Wav-file size is', os.path.getsize('Track16.wav'), '\n',
          '8bit Bin-file size is', os.path.getsize('encoded8bit.bin'),'\n',
          'Initial bin-file size is', os.path.getsize('encoded.bin'))
