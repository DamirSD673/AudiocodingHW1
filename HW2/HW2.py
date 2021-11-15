import numpy as np
import matplotlib.pyplot as plt
from MDCT import DirectMDCT, SyntesisMDCT # Task 1
import sound as snd

#  Task 2
# Ramp function
x = np.arange(44100) / 44100
# MDCT
N = 512
Y = DirectMDCT(x, N)
# Reconstruction
X_hat = SyntesisMDCT(Y, N)

# Plotting
fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(12, 5))
ax.plot(x)
ax.plot(X_hat)
ax.legend("Original", "Reconstructed")
ax.title("Original and Reconstructed signals")
ax.set_xlabel("Samples, n")
ax.set_ylabel("Amplitude")

# Task 3
[s, rate, bytes] = snd.wavread('Track16.wav')
N_s = len(s)
seconds = 8
s_hat = s[int(N_s/2):int(N_s/2)+rate*seconds] # elements from middle and 8 sec
s_hat = s_hat[:, 0]

Y_s = DirectMDCT(s_hat, N)
S_hat = SyntesisMDCT(Y_s, N)

fig, ax2 = plt.subplots(nrows=1, ncols=1, figsize=(12, 5))
ax2.plot(s_hat[0:len(s_hat) - 1023], 'r--', linewidth=2)
ax2.plot(S_hat[1023::], linewidth=0.5)
ax2.legend("Original", "Reconstructed")
ax2.title("Original and Reconstructed signals")
ax2.set_xlabel("Samples, n")
ax2.set_ylabel("Amplitude")

plt.show()