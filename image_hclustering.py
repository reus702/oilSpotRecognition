#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TaxonClassifier: execute agglomerative clustering on a set of molecules based on
a distance matrix and evaluate the quality of the clustering w.r.t. a known 
clusterization.

Usage: python3 ClusterMatrix.py <molecule-list-csv-file> <distances-csv-file> <classification-level>

The format of <molecule-list-csv-file> must be <"Id", "Uniprot", "Classification"> where
Id is a unique identifier in the file, Organism is a textual description of the 
Id and Taxon is the label associated to Id by a known classification

The format of <distances-csv-file> must be <"Id1", "Id2", "Distance"> where Id1 
and Id2 are two different Ids of the first file and Distance is a floating point
value corresponding to the distance from Id1 and Id2 computed by a chosen 
comparison method. 

The value of <classification-level> is between 1 and 4.

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

def clusterMatrixMain(labels_file, distances_file, distance_matrix):
    # Read the list of molecules
    molecules = pd.read_csv(labels_file, sep=";")  #TODO: camniare molecules con etichette immagini

    # Create dictionary Id -> Index
    index_of = dict()
    for i in range(len(molecules)) :
        index_of[molecules.loc[i].loc['Id']] = i

    '''# Create dictionary Id -> Label 
    label_of = dict()
    for i in range(len(molecules)):
        app = str(molecules.loc[i].loc['Classification']).strip()
        label_of[molecules.loc[i].loc['Id']] = app[:(classification_level*2-1)] #substring to classification level'''

    # Create Distance Matrix
    s= (len(molecules),len(molecules))
    distance_matrix= np.zeros(s)

    '''# Populate Distance Matrix
    for k in range(len(distances_file)) :
        i = index_of[distances_file.loc[k].loc['Image1']]
        j = index_of[distances_file.loc[k].loc['Image2']]
        value = distances_file.loc[k].loc['Distance']
        distance_matrix[i][j] = value
        distance_matrix[j][i] = value'''
    distance_matrix = pd.read_csv(distance_matrix, sep=";")

    # Determine the number of clusters as distinct labels in molecules
    n_clusters = 3

    # Read the true lables assigned to every Id 
    #labels_true = list(label_of.values())
    labels_true = list(distance_matrix[:, 0])

    # Execute clustering with single linkage and determines the predicted labels for each molecule

    model = AgglomerativeClustering(n_clusters=n_clusters, linkage ='single').fit(distance_matrix)
    
    
    labels_pred = model.fit_predict(distance_matrix)

    # Compute the metrics and print the evaluations
    print("Method: single")
    print("Rand_score", metrics.rand_score(labels_true, labels_pred))
    print("Homogeneity_score", metrics.homogeneity_score(labels_true, labels_pred))
    print("Completeness_score", metrics.completeness_score(labels_true, labels_pred))
        
    # Execute clustering with complete linkage and determines the predicted labels for each molecule

    model = AgglomerativeClustering(n_clusters=n_clusters, linkage ='complete').fit(distance_matrix)
    labels_pred = model.fit_predict(distance_matrix)

    # Compute the metrics and print the evaluations
    print("Method: complete")
    print("Rand_score", metrics.rand_score(labels_true, labels_pred))
    print("Homogeneity_score", metrics.homogeneity_score(labels_true, labels_pred))
    print("Completeness_score", metrics.completeness_score(labels_true, labels_pred))


    # Execute clustering with average linkage and determines the predicted labels for each molecule

    model = AgglomerativeClustering(n_clusters=n_clusters, linkage ='average').fit(distance_matrix)
    labels_pred = model.fit_predict(distance_matrix)

    # Compute the metrics and print the evaluations
    print("Method: average")
    print("Rand_score", metrics.rand_score(labels_true, labels_pred))
    print("Homogeneity_score", metrics.homogeneity_score(labels_true, labels_pred))
    print("Completeness_score", metrics.completeness_score(labels_true, labels_pred))
