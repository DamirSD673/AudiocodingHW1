from encframewk8bit import encframewk8bit
from decframewk8bit import decframewk8bit
import sound as snd
import matplotlib.pyplot as plt
import numpy as np

def normalisation(signal):
    max_value = float(np.max(signal))
    print("max", max_value)
    min_value = float(np.min(signal))
    print("min", min_value)
    normalized_signal = (signal - min_value) / (max_value - min_value)
    return normalized_signal

fs = 16000
encframewk8bit('Track16.wav')
decframewk8bit('encoded8bit.bin', fs)
[s, rate] = snd.wavread('decoded_8bit.wav')
[original, rate] = snd.wavread('Track16.wav')
snd.sound(s, 16000)

fig, ax = plt.subplots()

ax.plot(normalisation(original[:, 0]))
ax.plot(normalisation(s[:, 0]))

plt.show()