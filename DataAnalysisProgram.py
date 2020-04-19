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
    cnx = mysql.connector.connect(user='adam', password='grinding', host='10.0.0.27', database="machdata")
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
    select_feature = "SELECT feature_one, feature_two, feature_three, feature_four, feature_five, feature_six, feature_seven, feature_eight, feature_nine, feature_ten FROM customToolData"
    select_feature_w_setup = "SELECT setup_hours, feature_one, feature_two, feature_three, feature_four, feature_five, feature_six, feature_seven, feature_eight, feature_nine, feature_ten FROM customToolData"

    select_setup = "SELECT setup_hours FROM customToolData"
    select_labor = "SELECT labor_hours FROM customToolData"

    featureData = pd.read_sql(select_feature, con=cnx)
    setupData = pd.read_sql(select_setup, con=cnx)
    laborData = pd.read_sql(select_labor, con=cnx)
    setup_with_features = pd.read_sql(select_feature_w_setup, con=cnx)
    print(featureData)
    print(setupData)
    print(laborData)
    # Encode all of the features as integers using LabelEncoder
    setup_with_features['feature_one'] = LabelEncoder().fit_transform(setup_with_features.feature_one)
    setup_with_features['feature_two'] = LabelEncoder().fit_transform(setup_with_features.feature_two)
    setup_with_features['feature_three'] = LabelEncoder().fit_transform(setup_with_features.feature_three)
    setup_with_features['feature_four'] = LabelEncoder().fit_transform(setup_with_features.feature_four)
    setup_with_features['feature_five'] = LabelEncoder().fit_transform(setup_with_features.feature_five)
    setup_with_features['feature_six'] = LabelEncoder().fit_transform(setup_with_features.feature_six)
    setup_with_features['feature_seven'] = LabelEncoder().fit_transform(setup_with_features.feature_seven)
    setup_with_features['feature_eight'] = LabelEncoder().fit_transform(setup_with_features.feature_eight)
    setup_with_features['feature_nine'] = LabelEncoder().fit_transform(setup_with_features.feature_nine)
    setup_with_features['feature_ten'] = LabelEncoder().fit_transform(setup_with_features.feature_ten)

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

    setup_with_features_train = setup_with_features[
                                int(len(setup_with_features) * 0.0): int(len(setup_with_features) * .75)]
    setup_with_features_test = setup_with_features[
                               int(len(setup_with_features) * .75): int(len(setup_with_features) * 1.0)]
    print(featureData.head())
    print(setupData.head())
    print(laborData.head())

    print(setup_with_features.head())

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

    svr = SVR()

    encoder = OrdinalEncoder()
    encoder.fit(feature_train)
    feature_train = encoder.transform(feature_train)
    encoder.fit(feature_test)

    feature_test = encoder.transform(feature_test)

    svr.fit(feature_train, setup_train.values.ravel())

    svr.fit(feature_train, labor_train.values.ravel())

    #print("Accuracy Setup: {:.2f}".format(svr.score(feature_test, setup_test)))
    #print("Accuracy Labor: {:.2f}".format(svr.score(feature_test, labor_test)))
