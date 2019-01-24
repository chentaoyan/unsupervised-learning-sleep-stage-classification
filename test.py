from edfVisualization import readEEGSignal,plotRawData,plot3D,plotLabel
from featureExtraction import process
from model import kmeans
import numpy as np
import pyedflib

data = readEEGSignal('Data/SC4001E0-PSG.edf')[:,(1080000//2):(1080000//2*3)] #3 hours (100HZ) 100*60*60*3 data points
print(data.shape)
plotRawData(data)
dataPerEpoch = 2*60*100 #2min
feature = process(data,dataPerEpoch,True,True,True)
model, centroids, labels = kmeans(feature,3)
print(centroids,labels)
plot3D(feature,centroids)
plotLabel(labels)


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