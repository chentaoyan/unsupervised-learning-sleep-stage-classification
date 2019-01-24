import pyedflib
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.decomposition import PCA


# source of data: https://physionet.org/pn4/sleep-edfx/
# choice of data: first two signal ['EEG Fpz-Cz', 'EEG Pz-Oz'] 100Hz not sure
def readEEGSignal(name):
    f = pyedflib.EdfReader(name)
    signal_labels = f.getSignalLabels()
    print(signal_labels[0:2])
    sigbufs = np.zeros((2, f.getNSamples()[0]))
    print(sigbufs.shape)
    for i in np.arange(2):
        sigbufs[i, :] = f.readSignal(i)
    return sigbufs


def plotRawData(multiChannel):
    for i in range(len(multiChannel)):
        plt.plot(multiChannel[i])
    plt.show()


def plot3D(processedData,centerOfCluster):
    copy = np.array(processedData)
    pca = PCA(n_components=3)
    fig = plt.figure().add_subplot(111, projection='3d')
    pcaData = pca.fit_transform(copy)
    tem1, tem2, tem3 = zip(*pcaData)
    fig.scatter(tem1, tem2, tem3, marker='o', c='b')
    if centerOfCluster is not None:
        pcaLabel = pca.transform(centerOfCluster)
        print(pcaLabel)
        tem1,tem2,tem3 = zip(*pcaLabel)
        fig.scatter(tem1,tem2,tem3, marker='^',s=100)#????why the c='b' above has no error, here AttributeError

    plt.show()


def plotLabel(labels):
    colors = ['r', 'g', 'b', 'y', 'c', 'm']
    distinctLabel = list(set(labels))
    df = pd.DataFrame({'a': labels})
    for i in range(len(distinctLabel)):
        type_ = df[df['a']==distinctLabel[i]]
        plt.bar(type_.index.values, 1, color=colors[i])
    plt.show()






