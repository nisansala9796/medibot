import pickle

import pandas as pd
from sklearn import preprocessing

file_name = './medi_bot_api/diagnose/disease_classifier.sav'


def transform_data(data):
    symptoms = pd.read_csv('./medi_bot_api/diagnose/symptoms.csv')
    symptoms.iloc[-1] = ['NaN', 1]

    le = preprocessing.LabelEncoder()
    le.fit(symptoms['Symptom'])

    return le.transform(data).reshape(1, -1)


def get_predictions(data):
    clf = pickle.load(open(file_name, 'rb'))

    data = transform_data(data).reshape(1, -1)

    preds = clf.predict(data)
    print('Diagnose: ', preds[0])
    return preds[0]

# data = ['itching', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN']
# print(get_predictions(data))
