import os
import numpy as np
import sound as snd
from scipy.io import wavfile
import matplotlib.pyplot as plt
from MDCT import DirectMDCT, SyntesisMDCT
import pickle


class HeapNode:
    def __init__(self, value, word):
        self.value = value
        self.symbols = word
        self.left = None
        self.right = None
        self.par_left = None
        self.par_right = None

        def __repr__(self):
            return str(self.value)


class Huffman:
    def __init__(self, file, n=32, seconds=3):
        self.file = file
        self.n = n
        self.seconds = seconds


    def tree(self):
        from bitarray import bitarray
        [dictionaryy, sig8bit, stepsize] = self.frequency_dict()
        # codebooks = [] if necessary
        decodbooks = []
        whole_signal = bitarray()
        lengths = []
        for ii in range(self.n):
            nodes = [[]]
            for f in dictionaryy[ii]:
                nodes[-1].append(HeapNode(dictionaryy[ii][f], f))

            key = lambda x: x.value
            nodes[-1] = sorted(nodes[-1], key=key)
            k = 0
            while (len(nodes[-1]) > 1) and (k < 256):
                k += 1
                # print(self.nodes)
                new_value = nodes[-1][0].value + nodes[-1][1].value
                # print((self.nodes[-1][0].symbols))
                new_symbols = [nodes[-1][0].symbols] + [
                    nodes[-1][1].symbols]
                new_node = HeapNode(new_value, new_symbols)
                new_node.left = nodes[-1][0]
                new_node.right = nodes[-1][1]
                nodes[-1][0].par_left = new_node
                nodes[-1][1].par_right = new_node
                new_nodes = [new_node] + nodes[-1][2:]
                nodes.append(sorted(new_nodes, key=key))

            cod_dict = dict.fromkeys(dictionaryy[ii])
            for i, s in enumerate(dictionaryy[ii]):
                x = nodes[0][i]
                cod = ''
                # print('len_dict:', len(self.sorted_dict))
                for k in range(len(dictionaryy[ii])):
                    if x.par_left:
                        x = x.par_left
                        if x is None:
                            break
                        cod += '0'
                    else:
                        x = x.par_right
                        if x is None:
                            break
                        cod += '1'
                cod_dict[s] = cod[::-1]

            [coded_signal, decod_dict] = encode(sig8bit[:, ii], cod_dict)
            lengths.append(len(coded_signal))
            decodbooks.append(decod_dict)
            whole_signal.extend(coded_signal)

        return whole_signal, decodbooks, stepsize, lengths



    def frequency_dict(self):
        [sig8bit, stepsize] = self.quantizer8it()

        frequency_array = []
        for i in range(self.n):
            frequency = {}
            for sample in sig8bit[:, i]:
                if not sample in frequency:
                    frequency[sample] = 0
                frequency[sample] += 1

            frequency_array.append(dict(
                sorted(frequency.items(), key=lambda item: item[1],
                       reverse=False)))

        return frequency_array, sig8bit, stepsize


    def merge_and_MDCT(self):
        rate, s = wavfile.read(self.file)
        N_s = len(s)
        s_hat = s[int(N_s / 2):int(N_s / 2) + rate * self.seconds]  # elements from middle and 8 sec
        s_merged = np.reshape(np.transpose(s_hat), 2*s_hat.shape[0], order='F')
        s_MDCT = DirectMDCT(np.transpose(s_merged), self.n)
        return s_MDCT


    def quantizer8it(self):
        signal = self.merge_and_MDCT()
        step = (np.amax(signal, axis=0) - np.amin(signal, axis=0))/2 ** 8
        s8bit = (signal / step[None, :]).astype(np.int8)
        return s8bit, step

def encode(signal ,cod_dict):
    from bitarray import bitarray
    decod_dict = {v: np.int8(k) for k, v in cod_dict.items()}
    output = ''
    for s in signal:
        coded_s = cod_dict[s]
        output += coded_s

    coded_signal = bitarray(output)
    return coded_signal, decod_dict


def quantize8it(signal):
    step = (np.amax(signal, axis=0) - np.amin(signal, axis=0))/2 ** 8
    s8bit = (signal / step[None, :]).astype(np.int8)
    return s8bit, step

# Activate coder
seconds = 3
N = 32 # Subbands
coder = Huffman('Track16.wav', N, seconds)
[whole_signal, decodbooks, stepsizes, lengths] = coder.tree()

# Preapare binary files
binary_mdct = 'binary_mdct.bin'
binary_huffman = 'binary_huffman.bin'

# Original signal
[s, rate, bytes] = snd.wavread('Track16.wav')
N_s = len(s)
s_hat = s[int(N_s/2):int(N_s/2)+rate*seconds] # elements from middle and 8 sec
s_hat_1 = s_hat[:, 0]
s_hat_2 = s_hat[:, 1]

# MDCT of original signal (two channels)
Y_s_1 = DirectMDCT(s_hat_1, N)
Y_s_2 = DirectMDCT(s_hat_2, N)

# Quantizing originalMDCT signal
[Y_s_1_quant, stepsizes_Y_1] = quantize8it(Y_s_1)
[Y_s_2_quant, stepsizes_Y_2] = quantize8it(Y_s_2)

# Writing in files
pickle.dump([stepsizes_Y_1, Y_s_1_quant, stepsizes_Y_2, Y_s_2_quant], open(binary_mdct, "wb"), 1)
pickle.dump([stepsizes, decodbooks, whole_signal, lengths], open(binary_huffman, "wb"), 1)

print(os.path.getsize(binary_mdct) / 1024)
print(os.path.getsize(binary_huffman) / 1024)
