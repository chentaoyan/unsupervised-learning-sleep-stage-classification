from edfVisualization import readEEGSignal,plotRawData,plot3D,plotLabel,temporalPlotHypnogram
from featureExtraction import process,spectralEntropy
from analysis import compare
from model import kmeans
import numpy as np
import pyedflib


#use two channel of data  Fz and Cp
#this two channel have same length
#all data is stored in oe ['W', 'S1', 'S2', 'SWS', 'REM']

#
# data = readEEGSignal('Data/SC4001E0-PSG.edf')[:,2880000:5400000] #based on the other paper
# print(data.shape)
# # plotRawData(data)
# dataPerEpoch = 30*100 #30 sec
# feature = process(data,dataPerEpoch,True,True,True)
# model, centroids, labels = kmeans(feature,5)
# print(centroids,labels)
# print(type(labels))
# np.savetxt("labels1.csv", labels,fmt="%d")
# plot3D(feature,centroids,labels)
# plotLabel(labels)


# data = readEEGSignal('Data/SC4001EC-Hypnogram.edf')
# f = pyedflib.EdfReader('Data/SC4001EC-Hypnogram.edf')
# print(f)
# annotations = f.readAnnotations()
# print(annotations)
# for n in np.arange(f.annotations_in_file):
#         print("annotation: onset is %f    duration is %s    description is %s" % (annotations[0][n],annotations[1][n],annotations[2][n]))

# power2 = power(data)
# print(power2)
# power0 = power(np.array(data[0]))
# power1 = power(np.array(data[1]))
#
# print(power0)
# print(power1)
#
# processedData = process(data,10,True,True)
# plot3D([[1,2,3,4],[2,23,4,5],[3,4,4,4]],[[1,2,3,4]])
# plotLabel([1,1,0,0,2,3,4,3,4,4,2])






# #0216 test frequency band
# data = readEEGSignal('Data/SC4001E0-PSG.edf')[:,3066000:5064000] #based on the ground truth
# from featureExtraction import frequencyBand
# print(data.shape)
# oneEpochData = data[0,1120000:1123000]
# print(oneEpochData)
# plotRawData(oneEpochData)
# frequencyBand(oneEpochData)


# #0216 test entropy
# data = readEEGSignal('Data/SC4001E0-PSG.edf')[:,3066000:5064000] #based on the ground truth
# from featureExtraction import frequencyBand
# print(data.shape)
# oneEpochData = data[0,1120000:1123000]
# print(oneEpochData)
# print(spectralEntropy(oneEpochData))

# #0216 test model
# data = readEEGSignal('Data/SC4001E0-PSG.edf')[:,2880000:5400000] #based on the ground truth
# dataPerEpoch = 30*100 #30 sec
# print(data.shape)
# feature = process(data,dataPerEpoch,True,True,True,True,True,True,True)
# np.savetxt("feature.csv", feature,fmt="%d")
# print(feature)
#
# feature =np.loadtxt("feature.csv")
# model, centroids, labels = kmeans(feature,5)
# print(centroids,labels)
# print(type(labels))
# # plot3D(feature,centroids,labels)
# # plotLabel(labels)
# np.savetxt("label.csv", labels,fmt="%d")
# label = np.loadtxt("label.csv")
# temporalPlotHypnogram(label)


#0219 whole process of how to generate result
data = readEEGSignal('Data/SC4001E0-PSG.edf')[:,2880000:5400000] #based on the other paper
# print(data.shape)
# plotRawData(data)
dataPerEpoch = 30*100 #30 sec
feature = process(data,dataPerEpoch,True,True,True,True,True,True,True)
model, centroids, labels = kmeans(feature,5)
choices = compare(centroids)
temporalPlotHypnogram(labels,choices)

# label = np.loadtxt("resultOfMyModel/label.csv")
# feature = np.loadtxt("resultOfMyModel/averageFeature.csv")
# choices = compare(feature)
# temporalPlotHypnogram(label,choices)