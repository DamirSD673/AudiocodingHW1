from encframewk8bit import encframewk8bit
from decframewk8bit import decframewk8bit
import sound as snd
import matplotlib.pyplot as plt
import numpy as np

def normalisation(signal):
    max_value = float(np.max(np.abs(signal)))
    normalized_signal = signal/max_value
    return normalized_signal


fs = 16000
encframewk8bit('Track16.wav')
s = decframewk8bit('encoded8bit.bin', fs)
[original, rate, bytes] = snd.wavread('Track16.wav')  # Original wave signal
#snd.sound(s, rate_r)

fig, ax = plt.subplots(figsize=(12, 6))
# Plotting
ax.plot(normalisation(original[:, 0]), 'r--', linewidth=2)
ax.plot(normalisation(s[:, 0]), linewidth=0.5)
ax.legend(['16-bit', '8-bit'])
ax.set_title('Original and reconstructed signals')
ax.set_xlabel('samples')
ax.set_ylabel('Amplitude')

plt.show()