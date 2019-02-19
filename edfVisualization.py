import pyedflib
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.decomposition import PCA
import matplotlib
import time


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
    if (len(multiChannel.shape) == 1):
        plt.plot(np.array(multiChannel))
    else:
        for i in range(len(multiChannel)):
            plt.plot(multiChannel[i])
    plt.show()

def plotSeparateSignal(signal,title):
    plt.title(title)
    for i in range(len(signal)):
        plt.plot(signal[i])
    plt.show()


def plot3D(processedData,centerOfCluster,labels):
    colors = ['r', 'g', 'b', 'y', 'c', 'm']
    copy = np.array(processedData)
    pca = PCA(n_components=3)
    fig = plt.figure().add_subplot(111, projection='3d')
    pcaData = pca.fit_transform(copy)
    tem1, tem2, tem3 = zip(*pcaData)
    for i in range(len(tem1)):
        fig.scatter(tem1[i], tem2[i], tem3[i], marker='o', c=colors[labels[i]])
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


def plotHypnogram(stages, labels=None, title='', ax1=None, **kwargs):
    if labels is None:
        if np.max(stages) == 4:
            print('assuming 0=W, 1=S1, 2=S2, 3=SWS, 4=REM')
            labels = ['W', 'S1', 'S2', 'SWS', 'REM']
        if np.max(stages) == 5:
            print('assuming 0=W, 1=S1, 2=S2, 3=S3, 4=S4, 5=SWS')
            labels = ['W', 'S1', 'S2', 'S3', 'S4', 'REM']
        if np.max(stages) == 8:
            print('assuming 0=W, 1=S1, 2=S2, 3=S3, 4=S4, 5=SWS')
            labels = ['W', 'S1', 'S2', 'S3', 'S4', 'REM', 'Movement']
    labels_dict = dict(zip(np.arange(len(labels)), labels))

    x = []
    y = []
    for i in np.arange(len(stages)):
        s = stages[i]
        if labels_dict[s] == 'W':   p = -0
        if labels_dict[s] == 'REM': p = -1
        if labels_dict[s] == 'S1':  p = -2
        if labels_dict[s] == 'S2':  p = -3
        if labels_dict[s] == 'SWS': p = -4
        if labels_dict[s] == 'S3': p = -4
        if labels_dict[s] == 'S4': p = -5
        if i != 0:
            y.append(p)
            x.append(i - 1)
        y.append(p)
        x.append(i)

    x = np.array(x) * 30
    y = np.array(y)
    if ax1 is None:
        fig = plt.figure(figsize=[8, 2])
        ax1 = fig.add_subplot(111)
    formatter = matplotlib.ticker.FuncFormatter(lambda s, x: time.strftime('%H:%M', time.gmtime(s)))
    ax1.xaxis.set_major_formatter(formatter)
    ax1.plot(x, y, **kwargs)
    plt.yticks([0, -1, -2, -3, -4, -5], ['W', 'REM', 'S1', 'S2', 'SWS'])
    plt.xticks(np.arange(0, x[-1], 3600))
    plt.xlabel('Time after recording start')
    plt.ylabel('Sleep Stage')
    plt.title(title)
    plt.tight_layout()
    plt.show()





def temporalPlotHypnogram(stages, choices=None, title='', ax1=None, **kwargs):

    print('assuming 0=W, 1=S1, 2=S2, 3=SWS, 4=REM')
    defaultLabels = ['W', 'S1', 'S2', 'SWS', 'REM']
    labels = []
    for choice in choices:
        labels.append(defaultLabels[choice])

    labels_dict = dict(zip(np.arange(len(labels)), labels))
    print(labels_dict)

    x = []
    y = []
    for i in np.arange(len(stages)):
        s = stages[i]
        if labels_dict[s] == 'W':   p = -0
        if labels_dict[s] == 'REM': p = -1
        if labels_dict[s] == 'S1':  p = -2
        if labels_dict[s] == 'S2':  p = -3
        if labels_dict[s] == 'SWS': p = -4
        if labels_dict[s] == 'S3': p = -4
        if labels_dict[s] == 'S4': p = -5
        if i != 0:
            y.append(p)
            x.append(i - 1)
        y.append(p)
        x.append(i)

    x = np.array(x) * 30
    y = np.array(y)
    if ax1 is None:
        fig = plt.figure(figsize=[8, 2])
        ax1 = fig.add_subplot(111)
    formatter = matplotlib.ticker.FuncFormatter(lambda s, x: time.strftime('%H:%M', time.gmtime(s)))
    ax1.xaxis.set_major_formatter(formatter)
    ax1.plot(x, y, **kwargs)
    plt.yticks([0, -1, -2, -3, -4, -5], ['W', 'REM', 'S1', 'S2', 'SWS'])
    plt.xticks(np.arange(0, x[-1], 3600))
    plt.xlabel('Time after recording start')
    plt.ylabel('Sleep Stage')
    plt.title(title)
    plt.tight_layout()
    plt.show()




