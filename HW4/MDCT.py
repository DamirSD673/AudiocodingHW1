import numpy as np
from scipy.signal import lfilter


def DirectMDCT(x, N):
    h_n = np.sin(np.pi / (2*N) * (np.arange(2*N)+0.5)) # Window function h(n)
    filtered = np.zeros((len(x), N))

    for k in np.arange(N):
        h_k = h_n * np.sqrt(2/N) * np.cos(np.pi/N*(k+0.5) * (np.arange(2*N)+0.5-N/2)) #Impulse response of the modulated filter
        filtered[:, k] = lfilter(h_k, 1, x, axis=0) # Filtering

    Y = filtered[::N] # Downsampling the output signal
    return Y


def SyntesisMDCT (Y, N):
    g_n = np.sin(np.pi / (2*N) * (np.arange(2*N)+0.5)) # Window function for synthesis filter
    Y_up = np.zeros((len(Y)*N, N))
    Y_up[::N, :] = Y # Upsampling
    x = np.zeros((len(Y_up), N)) # Array for reconstructed signal
    for k in np. arange(N):
        g_k = g_n * np.sqrt(2 / N) * np.cos(np.pi / N * (k + 0.5) * (np.arange(2*N) + 0.5 - N / 2)) #Impulse response of the
        x[:, k] = lfilter(g_k[::-1], 1, Y_up[:, k])  # Filtering

    output = np.sum(x, axis=1)
    return output
