from HW2 import sound as snd
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft, fftshift


def normalisation(signal):
    max_value = float(np.max(np.abs(signal)))
    normalized_signal = signal/max_value
    return normalized_signal

def FFT(signal, channel, N_FFT, N_blocks):
    fig, ax = plt.subplots()
    for i in range(N_blocks):
        x = signal[i*N_FFT:(i+1)*N_FFT - 1, channel] # block-wise FFT
        x_hat = fftshift(fft(x))
        X = 20*np.log10(np.abs(x_hat)) # logarithmic scale
        ax.plot((np.linspace(-np.pi, np.pi, N_FFT - 1, endpoint=True)), X)

    ax.legend(range(N_blocks))
    ax.set_xlabel('Normalized frequency')
    ax.set_ylabel('Magnitude, dB')
    ax.set_title('Spectrum of 4 blocks')


# Task 1

[s, rate, bytes] = snd.wavread('Track16.wav')

#snd.sound(s, rate)
N = len(s)

print('Number of bits of the signal:', N*bytes*8)

s_hat = s[int(N/2):int(N/2)+rate*8] # elements from middle and 8 sec
s_normalized = normalisation(s_hat)  # normalisation process


fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(12, 6)) # creating plots
ax1.plot(s_normalized[:, 0])
ax2.plot(s_normalized[:, 1])
ax1.set_title('First channel')
ax2.set_title('Second channel')

# Task 2
FFT(s_hat, 0, 1024, 4)

plt.show()