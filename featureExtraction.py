import numpy as np
import pywt
import math




#input x should be an array with shape(Channel, dataPoint)
#all returned feature is in list

def power( x ):
    fea = []
    if(len(x.shape)!=1):
        for ele in x:
            F = np.fft.fft(ele)
            P = F * np.conjugate(F)
            fea.append(sum(P))
    else:
        F = np.fft.fft(x)
        P = F * np.conjugate(F)
        fea.append(sum(P))
    return fea


def mean(x):
    fea = []
    if(len(x.shape)!=1):
        for ele in x:
            fea.append(np.mean(ele))
    else:
        fea.append(np.mean(x))
    return fea

def std( x ):
    fea = []
    if (len(x.shape) != 1):
        for ele in x:
            fea.append(np.std(ele))
    else:
        fea.append(np.std(x))
    return fea




#TODO:
# def SpectralEntropy( x ):
#     fs = 128
#     band = [1,4,8,12,30]
#     b = pyeeg.bin_power(x,band,fs)
#     resp = pyeeg.spectral_entropy(x,band,fs,Power_Ratio=b)
#
#     resp = [0 if math.isnan(x) else x for x in resp]
#     return resp
#
# def DWT( x ):
#     fea = []
#     if (len(x.shape) != 1):
#         for ele in x:
#             fea.append(pywt.dwt(ele, 'db4'))
#     else:
#         fea.append(pywt.dwt(x, 'db4'))
#     return fea



def process(data, numOfFrames, usePower, useMean, useStd):
    epoch = len(data[0])//numOfFrames
    totalFeature = []
    for i in range(epoch):
        feature = []
        for channel in data:
            if usePower:
                feature.extend(power(channel[i * numOfFrames:(i + 1) * numOfFrames]))
            if useMean:
                feature.extend(mean(channel[i * numOfFrames:(i + 1) * numOfFrames]))
            if useStd:
                feature.extend(std(channel[i * numOfFrames:(i + 1) * numOfFrames]))
        totalFeature.append(feature)
    return totalFeature
