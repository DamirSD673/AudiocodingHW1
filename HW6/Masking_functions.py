import numpy as np
from scipy.signal import stft

width = 0.5

def hz2brk(hz):
    return 6 * np.arcsinh(hz/600)

def map2brk_mat(fs, nfft):
    # Constructing matrix W which has 1’s for each Bark subband, and 0’s else
    max_brk = hz2brk(fs/2)
    nfilts = np.round(max_brk/width).astype(np.int64)
    step_barks = max_brk/(nfilts-1)
    
    binbarks = hz2brk(np.linspace(0,(nfft//2),(nfft//2)+1)*fs//nfft)
    W = np.zeros((nfilts, nfft))
    for i in range(nfilts):
        W[i,0:(nfft//2)+1] = (np.round(binbarks/step_barks)== i)
    return W, nfilts, max_brk

def map2brk(x, W, nfft):
    nfreqs = int(nfft/2)
    mXbark = (np.dot(np.abs(x[:nfreqs]).T**2.0, W[:, :nfreqs].T))**(0.5)
    return mXbark

def SF_mat(max_brk, nfilts, alpha):
    fadB = 14.5 + 12 # Simultaneous masking for tones at Bark band 12
    fbdb = 7.5 # Upper slope of spreading function
    fbbdb = 26.0 # Lower slope of spreading function
    sf_brk_dB = np.zeros(2*nfilts)
    sf_brk_dB[0:nfilts] = np.linspace(-max_brk*fbdb, -2.5, nfilts) - fadB
    sf_brk_dB[nfilts:2*nfilts] = np.linspace(0, -max_brk*fbbdb, nfilts) - fadB
    sf_brk = 10**(sf_brk_dB*alpha / 20)
    sf_mat = np.zeros((nfilts, nfilts))
    for k in range(nfilts):
        sf_mat[:,k] = sf_brk[(nfilts - k):(2*nfilts - k)]
    return sf_mat

def SF(max_brk, nfilts):
    sf_db = np.zeros(2*nfilts)
    sf_db[0:nfilts] = np.linspace(-max_brk*27,-8,nfilts)-23.5
    sf_db[nfilts:2*nfilts] = np.linspace(0,-max_brk*12.0,nfilts)-23.5
    return sf_db

def MT(x,sf_mat, alpha):
    mt = np.dot(x**alpha, sf_mat)
    return mt**(1.0/alpha)

def brk2hz(bark):
    return 600 * np.sinh(bark/6)

def MT_bark(x,sf_mat, max_brk, alpha):
    mt = np.dot(x**alpha, sf_mat**alpha)
  
    #apply the inverse exponent to the result:
    return mt**(1.0/alpha)

def MTQ_bark(x,sf_mat, max_brk, nfilts, alpha): 
    mt = np.dot(x**alpha, sf_mat**alpha)
    mt = mt**(1.0/alpha)
    step_bark = max_brk/(nfilts-1)
    barks = np.arange(0,nfilts)*step_bark
  
    f = brk2hz(barks) + 1e-6
    LTQ = np.clip((3.64*(f/1000.)**-0.8 -6.5*np.exp(-0.6*(f/1000.-3.3)**2.)+1e-3*((f/1000.)**4.)),-20,160)
    mt1 = np.max((mt, 10.0**((LTQ-60)/20)),0)
    return mt1

def map2hz_mat(W, nfft):
    nfreqs = int(nfft/2)
    W_inv = np.dot(np.diag((1.0/np.sum(W,1))**0.5), W[:,0:nfreqs + 1]).T
    return W_inv

def map2hz(mt_bark, W_inv, nfft):
    nfreqs = int(nfft/2)
    mt = W_inv @ mt_bark
    return mt
