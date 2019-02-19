from edfVisualization import readEEGSignal,plotRawData,plot3D,plotLabel,temporalPlotHypnogram,plotSeparateSignal
from featureExtraction import process,spectralEntropy
from model import kmeans
import numpy as np
import pyedflib
import csv

def compare(myFeature):
    baselineFeature = np.loadtxt("resultOfBaselineModel/averageFeature.csv")
    totalError = []
    for feature in myFeature:
        error = []
        for baseFeature in baselineFeature:
            dist = np.linalg.norm(feature - baseFeature)
            error.append(dist)
        print(error)
        totalError.append(error)

    import itertools
    choices = list(itertools.permutations([0, 1, 2, 3, 4]))
    print(choices)
    final_choice = 0
    minError = 10000000
    for choice in choices:
        tempError = 0
        for i in range(5):
            if choice[i] == 2:  # S2
                tempError += 2 * totalError[i][choice[i]]
            elif choice[i] == 4:  # REM
                tempError += 2 * totalError[i][choice[i]]
            else:
                tempError += totalError[i][choice[i]]
        if tempError < minError:
            minError = tempError
            final_choice = choice
    print(final_choice)
    print(minError)
    return final_choice






def loadGroundTruth():

    data = readEEGSignal('Data/SC4001E0-PSG.edf')[:,2880000:5400000] #based on the ground truth
    dataPerEpoch = 30*100 #30 sec
    labels = np.loadtxt("resultOfMyModel/label.csv")
    stages = ['W', 'S1', 'S2', 'SWS', 'REM']
    average_signal = {}
    numOfSignal = {}
    average_feature = {}
    for stage in stages:
        average_signal[stage] = np.zeros((2,3000))
        numOfSignal[stage] = 0
        average_feature[stage] = np.zeros(22)
    for i in range(len(labels)):
        current_signal = np.array(data[:,i*3000:i*3000+3000])
        average_signal[stages[int(labels[i])]] = np.add(current_signal,average_signal[stages[int(labels[i])]])
        average_feature[stages[int(labels[i])]] = np.add(process(current_signal,3000,True,True,True,True,True,True,True),average_feature[stages[int(labels[i])]])
        numOfSignal[stages[int(labels[i])]] += 1



    for key in stages:
        # print(key)
        # print(average_signal[key])
        # print(numOfSignal[key])
        average_signal[key] = np.divide(average_signal[key],numOfSignal[key])
        average_feature[key] = np.divide(average_feature[key], numOfSignal[key])
        # print(average_feature[key])
        #plotSeparateSignal(average_signal[key],key)



    write_feature = []
    for key in ['W', 'S1', 'S2', 'SWS', 'REM']:
        write_feature.append(average_feature[key].ravel())
    write_feature = np.array(write_feature)
    # print(write_feature.shape)
    np.savetxt("resultOfMyModel/averageFeature.csv", write_feature)

loadGroundTruth()
