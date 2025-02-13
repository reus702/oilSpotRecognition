#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TaxonClassifier: execute agglomerative clustering on a set of molecules based on
a pair of features and evaluate the quality of the clustering w.r.t. a known 
clusterization.

Usage: python3 ClusterFeatures.py <molecule-list-csv-file> <eigenvalues-csv-file>

The format of <molecule-list-csv-file> must be <"Id", "Organism", "Taxon"> where
Id is a unique identifier in the file, Organism is a textual description of the 
Id and Taxon is the label associated to Id by a known classification

The format of <eigenvalues-csv-file> must be <"Id", "valueS", "valueS"> where Id
is one Id of the first file and valueS/valueE are features computed for each Id.
The features are used to 

The output is given textually as the values of "Rand_score", "Homogeneity_score" 
and "Completeness_score" metrics computed for each executed clustering and for 
each linkage parameter of the clustering algorithm: single, complete and 
average.


@author: Michela Quadrini and Luca Tesei
"""
import sys
import pandas as pd
import numpy as np
from sklearn.metrics import *
from sklearn.cluster import *
from sklearn import metrics

def clusterFeatures(features_path):
    # Read the list of molecules
    features_file = pd.read_csv(features_path, sep=",",skiprows=0 )
    features = features_file[["Histogram_Distance", "SSIM"]]

    # Determine the number of clusters as distinct labels in molecules
    n_clusters = 3

    # Read the true lables assigned to every Id 
    labels_true = features_file["Label"]

    model = AgglomerativeClustering(n_clusters=n_clusters, metric='euclidean', linkage ='single').fit(features)
    labels_pred = model.fit_predict(features)

    # Compute the metrics and print the evaluations
    print("Method: single")
    print("Rand_score", metrics.rand_score(labels_true, labels_pred))
    print("Homogeneity_score", metrics.homogeneity_score(labels_true, labels_pred))
    print("completeness_score", metrics.completeness_score(labels_true, labels_pred))

    model = AgglomerativeClustering(n_clusters=n_clusters, metric='euclidean', linkage ='complete').fit(features)
    labels_pred = model.fit_predict(features)

    # Compute the metrics and print the evaluations
    print("Method: complete")
    print("Rand_score", metrics.rand_score(labels_true, labels_pred))
    print("Homogeneity_score", metrics.homogeneity_score(labels_true, labels_pred))
    print("completeness_score", metrics.completeness_score(labels_true, labels_pred))

    model = AgglomerativeClustering(n_clusters=n_clusters, metric='euclidean', linkage ='average').fit(features)
    labels_pred = model.fit_predict(features)
    
    '''print ("LABELS TRUE ")
    for label in labels_true:
        print(label)

    print ("LABELS PRED ")
    for label in labels_pred:
        print(label)'''

    # Compute the metrics and print the evaluations
    print("Method: average")
    print("Rand_score", metrics.rand_score(labels_true, labels_pred))
    print("Homogeneity_score", metrics.homogeneity_score(labels_true, labels_pred))
    print("completeness_score", metrics.completeness_score(labels_true, labels_pred))

if len(sys.argv) != 2 :
    print("Usage: python ClusterFeatures.py <features-csv-file>")
    sys.exit(1)

features_path = sys.argv[1]
clusterFeatures(features_path)