import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

import pickle
import os
from bitarray import bitarray

class Filter_banks():
    def __init__(self, x, N=512):
        self.x = x
        self.N = N
        self.n = np.arange(2*N)
        self.h_k = np.zeros((N, 2*N))
        self.g_k = np.zeros((N, 2*N))
        self.y1 = np.zeros((N, len(x)))
        self.y2 = np.zeros((N, len(x)//N))
        self.s = 0  # (N-1) is identical to mode="same"
        self.h_n = np.sin(np.pi*(self.n + 0.5) /2 /self.N) * np.sqrt(2/self.N)

    def analysis(self):
        # filter and downsample
        for k in range(self.N):
            self.g_k[k, :] = self.h_n * np.cos(np.pi*(k+0.5)*(self.n+0.5-0.5*self.N) /self.N)
            self.h_k[k, :] = self.g_k[k, ::-1]
            self.y1[k, :] = signal.convolve(self.x, self.h_k[k, :], mode="full")[self.s:len(self.x)+self.s]  # filtering
            self.y2[k, :] = self.y1[k, k::self.N]   # downsampling

    def synthesis(self, new_y2=None):
        # restore
        if new_y2 is not None:
            self.new_y2 = np.array(new_y2)
        else:
            self.new_y2 = np.array(self.y2)
        self.y3 = np.zeros((self.N, len(self.x)))
        self.y4 = np.zeros((self.N, len(self.x)))
        for k in range(self.N):
            self.y3[k, k::self.N] = self.new_y2[k, :]  # upsampling
            self.y4[k, :] = signal.convolve(self.y3[k, :], self.g_k[k, :], mode="full")[self.s:len(self.x)+self.s] # filtering
        self.x_hat = self.y4.sum(0)
        return self.x_hat


class TreeNode:
    def __init__(self, value, symbols):
        self.value = value
        self.symbols = symbols
        self.left = None
        self.right = None
        self.parent_from_left = None
        self.parent_from_right = None
    
    def __repr__(self):
        return str(self.value)



key = lambda x: x.value

class Huffman:
    # only encoding here
    def __init__(self, string):
        self.string = string
        self.symbols_dict = {}
        for s in self.string:
            if s in self.symbols_dict:
                self.symbols_dict[s] += 1
            else:
                self.symbols_dict[s] = 1
        self.routines()
                
    def routines(self):
        self.__tree()
        self.__backward()
        
    def __tree(self):
        self.sorted_dict = dict(sorted(self.symbols_dict.items(), key=lambda item: item[1]))
      
        self.cod_dict = dict.fromkeys(self.symbols_dict.keys())
        self.nodes = [[]]
        for s in self.sorted_dict:
            self.nodes[-1].append(TreeNode(self.symbols_dict[s], s))
        self.nodes[-1] = sorted(self.nodes[-1], key=key)
        k = 0
        while (len(self.nodes[-1]) > 1) and (k < 10240):
            k += 1
            #print(self.nodes)
            new_value = self.nodes[-1][0].value + self.nodes[-1][1].value
            #print((self.nodes[-1][0].symbols))
            new_symbols = [self.nodes[-1][0].symbols] + [self.nodes[-1][1].symbols]
            new_node = TreeNode(new_value, new_symbols)
            new_node.left = self.nodes[-1][0]
            new_node.right = self.nodes[-1][1]
            self.nodes[-1][0].parent_from_left = new_node
            self.nodes[-1][1].parent_from_right = new_node
            new_nodes = [new_node] + self.nodes[-1][2:]
            self.nodes.append(sorted(new_nodes, key=key))
            
    def __backward(self):
        #print('sorted_dict:', self.sorted_dict)
        for i, s in enumerate(self.sorted_dict):
            x = self.nodes[0][i]
            cod = ''
            #print('len_dict:', len(self.sorted_dict))
            for k in range(len(self.sorted_dict)):
                if x.parent_from_left:
                    x = x.parent_from_left
                    if x is None:
                        break
                    cod += '0'
                else:
                    x = x.parent_from_right
                    if x is None:
                        break
                    cod += '1'
            self.cod_dict[s] = cod[::-1]
        
    def encode(self):
        from bitarray import bitarray
        
        self.decod_dict = {v: np.int32(k) for k, v in self.cod_dict.items()}
        output = ''
        #print('len:', len(self.string))
        for s in self.string:
            coded_s = self.cod_dict[s]
            output += coded_s
        #print('output:', output)
        self.coded_string = bitarray(output)
        return self.decod_dict, self.coded_string

def decode_h(decod_dict, data):
    #ba = bitarray()
    #ba.frombytes(data)
    #print('ba:', ba)
    ba = data
    #print(len(ba))

    restored = []
    buffer = ''
    #b
    for i, s in enumerate(ba):
        buffer += str(s)
        #print(buffer)
        #if decod_dict.get(buffer):
        if buffer in decod_dict:
            restored.append(decod_dict[buffer])
            buffer = ''
    return np.array(restored)
