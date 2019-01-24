from sklearn.cluster import KMeans


def kmeans(processedData,numOfCluster):

    kmeans = KMeans(n_clusters=numOfCluster).fit(processedData)
    labels = kmeans.predict(processedData)
    centroids = kmeans.cluster_centers_
    return kmeans, centroids, labels