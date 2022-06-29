# import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import pickle


class HeartDiseaseClassifier:
    """
        Responsible for preprocessing, training and predicting Heart Disease
    """

    def __init__(self, dataset='dataset.csv'):
        self.base_dir = './medi_bot_api/heart_disease/'
        self.datasource = self.base_dir + dataset
        self.x = ''
        self.y = ''
        self.file_name = self.base_dir + 'heart_disease_classifier.sav'
        self.classifier = None

    # def preprocess(self):
    #     """
    #         Removes rows containing null fields
    #         :param dataset: str path tocsv file
    #         :rtype: pandas dataframe
    #     """
    #     # drop rows containing null fields
    #     df = pd.read_csv(self.datasource).dropna()
    #
    #     return df

    # def xy_split(self, df):
    #     """
    #         Dependent independent var split
    #         :param df: pd dataframe
    #         :rtype: None
    #     """
    #     self.x = df.drop('target', axis=1).values
    #     self.y = df['target'].values

    # def train(self):
    #     """
    #         Trains the model
    #         :rtype: None
    #     """
    #     # classifier with tuned params
    #     rf = RandomForestClassifier(
    #         bootstrap=True, ccp_alpha=0.0,
    #         class_weight=None, criterion='entropy',
    #         max_depth=None, max_features='auto',
    #         max_leaf_nodes=None, max_samples=None,
    #         min_impurity_decrease=0.0,
    #         min_samples_leaf=2, min_samples_split=10,
    #         min_weight_fraction_leaf=0.0, n_estimators=100,
    #         n_jobs=None, oob_score=False, random_state=None,
    #         verbose=0, warm_start=False
    #     )
    #
    #     # remove null containing rows
    #     # independent dependant var split
    #     self.xy_split(self.preprocess())
    #
    #     # train
    #     # print(type(self.x), type(self.y))
    #     rf.fit(self.x, self.y)
    #
    #     # save model
    #     pickle.dump(rf, open(self.file_name, 'wb'))
    #     print('Model trained!')

    def get_predictions(self, data):
        """
            Returns predictions for feature array
                :param data: list of features used to train model
                >>> data = [ 63., 1., 3., 145., 233., 1., 0., 150., 0., 2.3, 0., 0., 1.]
                :return: bool True if has a heart disease else false
        """
        data = np.array(data).reshape(1, -1)

        # load model
        self.classifier = rf = pickle.load(open(self.file_name, 'rb'))

        # get prediction
        prediction = self.classifier.predict(data)

        if prediction[0] == 1:
            return True
        return False

# !!! Comment when deploying - TESTING PURPOSES ONLY !!!
# if __name__ == '__main__':
#     clf = HeartDiseaseClassifier()
#     clf.train()
#
#     data = [63., 1., 3., 145., 233., 1., 0., 150., 0., 2.3, 0., 0., 1.]
#     print(clf.get_predictions(data))