import numpy as np
import pywt
import math
import matplotlib.pyplot as plt
from scipy import stats, signal



#input x should be an array with shape(Channel, dataPoint)
#all returned feature is in list

# all feature extraction function is for one channel of signal
# 5 frequency bands
def frequencyBand(data):
    fea = []
    fs = 100                                # Sampling rate (512 Hz)
    # data = np.random.uniform(0, 100, 1024)  # 2 sec of data b/w 0.0-100.0
    
    # Get real amplitudes of FFT (only in postive frequencies)
    fft_vals = np.absolute(np.fft.rfft(data))
    
    # Get frequencies for amplitudes in Hz
    fft_freq = np.fft.rfftfreq(len(data), 1.0/fs)
    
    # Define EEG bands
    eeg_bands = {'Delta': (0.5, 4),
                 'Theta': (4, 8),
                 'Alpha': (8, 13),
                 'Beta': (13, 20),
                 'Gamma': (20, 50),
                 'Sleep_Spindle': (12, 14)}
    
    # Take the mean of the fft amplitude for each EEG band
    eeg_band_fft = dict()
    for band in eeg_bands:  
        freq_ix = np.where((fft_freq >= eeg_bands[band][0]) & 
                           (fft_freq <= eeg_bands[band][1]))[0]
        eeg_band_fft[band] = np.mean(fft_vals[freq_ix])
    
    # # Plot the data (using pandas here cause it's easy)
    # import pandas as pd
    # df = pd.DataFrame(columns=['band', 'val'])
    # df['band'] = eeg_bands.keys()
    # df['val'] = [eeg_band_fft[band] for band in eeg_bands]
    # ax = df.plot.bar(x='band', y='val', legend=False)
    # ax.set_xlabel("EEG band")
    # ax.set_ylabel("Mean band Amplitude")
    # # plt.show()
    for band in eeg_bands:
        fea.append(eeg_band_fft[band])
        
    return fea

#
# def power( data ):
#     fea = []
#     F = np.fft.fft(data)
#     P = F * np.conjugate(F)
#     fea.append(sum(P))
#     return fea


def mean(data):
    fea = []
    fea.append(np.mean(data))
    return fea


def std(data):
    fea = []
    fea.append(np.std(data))
    return fea


def variance(data):
    fea = []
    fea.append(np.var(data))
    return fea


def kurtosis(data):
    fea = []
    fea.append(stats.kurtosis(data))
    return fea


def spectralEntropy(data):
    fea = []
    _, psd = signal.periodogram(data, 100) #frequency = 100
    psd_norm = np.divide(psd, psd.sum())
    se = -np.multiply(psd_norm, np.log2(psd_norm)).sum()

    #TODO:how to handle NaN case

    if math.isnan(se):
        se = 0
    fea.append(se)
    return fea




#TODO:
#
# def DWT( x ):
#     fea = []
#     if (len(x.shape) != 1):
#         for ele in x:
#             fea.append(pywt.dwt(ele, 'db4'))
#     else:
#         fea.append(pywt.dwt(x, 'db4'))
#     return fea


def process(data, dataPerEpoch, usePower, useMean, useStd, useVariance, useFreqBand, useKurtosis, useSpectralEntropy):
    numOfEpoch = len(data[0])//dataPerEpoch
    totalFeature = []
    for i in range(numOfEpoch):
        feature = []
        for channel in data:
            # if usePower:
            #     feature.extend(power(channel[i * dataPerEpoch:(i + 1) * dataPerEpoch]))
            if useMean:
                feature.extend(mean(channel[i * dataPerEpoch:(i + 1) * dataPerEpoch]))
            if useStd:
                feature.extend(std(channel[i * dataPerEpoch:(i + 1) * dataPerEpoch]))
            if useVariance:
                feature.extend(variance(channel[i * dataPerEpoch:(i + 1) * dataPerEpoch]))
            if useFreqBand:
                feature.extend(frequencyBand(channel[i * dataPerEpoch:(i + 1) * dataPerEpoch]))
            if useKurtosis:
                feature.extend(kurtosis(channel[i * dataPerEpoch:(i + 1) * dataPerEpoch]))
            if useSpectralEntropy:
                feature.extend(spectralEntropy(channel[i * dataPerEpoch:(i + 1) * dataPerEpoch]))
        totalFeature.append(feature)
    totalFeature = np.array(totalFeature)
    # print(totalFeature.shape)
    return totalFeature
