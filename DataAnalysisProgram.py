# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 14:48:49 2020

@author: AdamDiamond
"""
import mysql.connector
import pandas as pd
from sklearn.preprocessing import OrdinalEncoder, LabelEncoder
from sklearn.svm import SVR
from mysql.connector import errorcode
from sklearn.neighbors import KNeighborsClassifier

try:
    cnx = mysql.connector.connect(user='user', password='password', host='your_host', database="your_database")
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("ERROR: Wrong Credentials")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("ERROR: Database does not exist")
    else:
        print("Unknown ERROR: ")
        print(err)
else:
    cursor = cnx.cursor(buffered=True)
    select_feature = "SELECT feature_one, feature_two, feature_three, feature_four, feature_five, feature_six, feature_seven, feature_eight, feature_nine, feature_ten FROM your_table"
    select_feature_w_setup = "SELECT setup_hours, feature_one, feature_two, feature_three, feature_four, feature_five, feature_six, feature_seven, feature_eight, feature_nine, feature_ten FROM your_table"

    select_setup = "SELECT setup_hours FROM your_table"
    select_labor = "SELECT labor_hours FROM your_table"

    featureData = pd.read_sql(select_feature, con=cnx)
    setupData = pd.read_sql(select_setup, con=cnx)
    laborData = pd.read_sql(select_labor, con=cnx)
    setup_with_features = pd.read_sql(select_feature_w_setup, con=cnx)
    
    print(featureData)
    print(setupData)
    print(laborData)

    featureData['feature_one'] = LabelEncoder().fit_transform(featureData.feature_one)
    featureData['feature_two'] = LabelEncoder().fit_transform(featureData.feature_two)
    featureData['feature_three'] = LabelEncoder().fit_transform(featureData.feature_three)
    featureData['feature_four'] = LabelEncoder().fit_transform(featureData.feature_four)
    featureData['feature_five'] = LabelEncoder().fit_transform(featureData.feature_five)
    featureData['feature_six'] = LabelEncoder().fit_transform(featureData.feature_six)
    featureData['feature_seven'] = LabelEncoder().fit_transform(featureData.feature_seven)
    featureData['feature_eight'] = LabelEncoder().fit_transform(featureData.feature_eight)
    featureData['feature_nine'] = LabelEncoder().fit_transform(featureData.feature_nine)
    featureData['feature_ten'] = LabelEncoder().fit_transform(featureData.feature_ten)

    setup_train = setupData[int(len(setupData) * 0.0): int(len(setupData) * .75)]

    labor_train = laborData[int(len(laborData) * 0.0): int(len(laborData) * .75)]

    feature_train = featureData[int(len(featureData) * 0.0): int(len(featureData) * .75)]

    setup_test = setupData[int(len(setupData) * .75): int(len(setupData) * 1.0)]

    labor_test = laborData[int(len(laborData) * .75): int(len(laborData) * 1.0)]

    feature_test = featureData[int(len(featureData) * .75): int(len(featureData) * 1.0)]

    print(featureData.head())
    print(setupData.head())
    print(laborData.head())

    knn = KNeighborsClassifier(n_neighbors=5, metric='euclidean')
    print("feature_train: ")
    print(feature_train)
    print("setup_train: ")
    print(setup_train)
    print("feature_test: ")
    print(feature_test)
    knn.fit(feature_train, setup_train.values.ravel())
    y_pred = knn.predict(feature_test)
    print(y_pred)

