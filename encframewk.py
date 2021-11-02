import os
from scipy.io import wavfile
import pickle

rate, s = wavfile.read('Track16.wav')
pickle.dump(s, open('encoded.bin', 'wb'), 1)
print('Wav-file size is', os.path.getsize('Track16.wav'), '\n',
      'Bin-file size is', os.path.getsize('encoded.bin'))
