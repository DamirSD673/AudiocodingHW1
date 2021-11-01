import sound as snd
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft


def normalisation(signal):
    max_value = float(np.max(signal))
    min_value = float(np.min(signal))
    normalized_signal = (signal - min_value) / (max_value - min_value)
    return normalized_signal

def FFT(signal, channel, N_FFT, N_blocks):
    fig, ax = plt.subplots()
    for i in range(N_blocks):
        x = signal[i*N_FFT:(i+1)*N_FFT - 1, channel] # block-wise FFT
        X = 20*np.log10(np.abs(fft(x))) # logarithmic scale
        ax.plot((np.linspace(0, np.pi, N_FFT - 1, endpoint=True)), X)

    ax.legend(range(N_blocks))
    ax.set_xlabel('Normalized frequency')
    ax.set_ylabel('Magnitude, dB')
    ax.set_title('Spectrum of 4 blocks')


# Task 1
[s, rate] = snd.wavread('Track16.wav')
snd.sound(s, 16000)
N = len(s)

s_hat = s[int(N/2):int(N/2)+16000*8] # elements from middle and 8 sec
s_normalized = normalisation(s_hat)  # normalisation process


fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1) # creating plots
ax1.plot(s_normalized[:, 0])
ax2.plot(s_normalized[:, 1])
ax1.set_title('First channel')
ax2.set_title('Second channel')

# Task 2
FFT(s_normalized, 0, 1024, 4)

plt.show()