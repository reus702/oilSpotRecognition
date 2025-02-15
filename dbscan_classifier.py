import sys
import pandas as pd
import numpy as np
from sklearn.metrics import *
from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
import matplotlib.pyplot as plt

def clusterFeatures(features_path):
    features_file = pd.read_csv(features_path, sep=",", skiprows=0)
    features = features_file[["Histogram_Distance", "SSIM", "White_pixels_diff", "Image_difference_mean"]]
    
    # Standardize features to improve clustering
    features = StandardScaler().fit_transform(features)
    
    # Read the true labels assigned to every Id 
    labels_true = features_file["Label"]

    # Apply DBSCAN
    eps_value = 0.5  # Adjust based on your data
    min_samples_value = 2  # Adjust based on your data
    model = DBSCAN(eps=eps_value, min_samples=min_samples_value, metric='euclidean')
    labels_pred = model.fit_predict(features)
    
    # Compute the metrics and print the evaluations
    print("Method: DBSCAN")
    print("Rand_score", metrics.rand_score(labels_true, labels_pred))
    print("Homogeneity_score", metrics.homogeneity_score(labels_true, labels_pred))
    print("Completeness_score", metrics.completeness_score(labels_true, labels_pred))

if len(sys.argv) != 2:
    print("Usage: python ClusterFeatures.py <features-csv-file>")
    sys.exit(1)

features_path = sys.argv[1]
clusterFeatures(features_path)
