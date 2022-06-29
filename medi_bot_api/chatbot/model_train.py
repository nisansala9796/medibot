import random
import json
import pickle
import numpy as np

import nltk

# nltk.download('punkt')
# nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.optimizers import SGD


class ChatBotModel:
    """
        Responsible in training intent classification model
    """

    def __init__(self):
        self.words = []
        self.classes = []
        self.documents = []
        self.ignore_letters = ['?', '!', '.', ',']
        self.json_file = open('./medi_bot_api/chatbot/intents.json')
        self.intents = json.load(self.json_file)
        self.lemmatizer = WordNetLemmatizer()

    def preprosess(self):
        """
            Preprocess the dataset
            :rtype: None
        """
        for intent in self.intents['intents']:
            for pattern in intent['patterns']:
                word_list = nltk.word_tokenize(pattern)
                self.words.extend(word_list)
                self.documents.append((word_list, intent['tag']))
                if intent['tag'] not in self.classes:
                    self.classes.append(intent['tag'])

        self.words = [self.lemmatizer.lemmatize(word) for word in self.words if word not in self.ignore_letters]

        self.words = sorted(set(self.words))
        self.classes = sorted(set(self.classes))

        # create pickle files
        pickle.dump(self.words, open('./medi_bot_api/chatbot/words.pkl', 'wb'))
        pickle.dump(self.classes, open('./medi_bot_api/chatbot/classes.pkl', 'wb'))

    def get_trainingset(self):
        """
            Creates the training set for the model
            :return: np array - Preprocessed dataset
        """
        training = []
        output_empty = [0] * len(self.classes)

        for document in self.documents:
            bag = []
            word_patterns = document[0]
            words = [self.lemmatizer.lemmatize(word) for word in self.words if word and word not in self.ignore_letters]
            for word in words:
                bag.append(1) if word in word_patterns else bag.append(0)

            output_row = list(output_empty)
            output_row[self.classes.index(document[1])] = 1
            training.append([bag, output_row])

        random.shuffle(training)

        return np.array(training)

    def xy_split(self, training_set):
        """
            Independent dependent variable splitting
            :param training_set: np array - preprocessed complete dataset
            :rtype: object
        """
        train_x = list(training_set[:, 0])
        train_y = list(training_set[:, 1])

        return train_x, train_y

    def create_model(self, input_shape, output_shape):
        """
            Intent classification model.
            :param input_shape: tuple - size of input data
            "param output_shape: tuple - size of output data
            :rtype: sequential
        """
        model = Sequential()
        model.add(Dense(128, input_shape=input_shape, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(64, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(output_shape, activation='softmax'))

        sgd = SGD(learning_rate=0.01, decay=1e-6, momentum=0.9, nesterov=True)
        model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

        return model

    def train(self, epochs=200):
        """
            Training
            :param epochs: int -  number of epochs
            :rtype: model object
        """
        self.preprosess()
        training_set = self.get_trainingset()

        train_x, train_y = self.xy_split(training_set)
        input_shape = (len(train_x[0]), )
        output_shape = len(train_y[0])

        model = self.create_model(input_shape, output_shape)

        hist = model.fit(
            x=train_x,
            y=train_y,
            epochs=epochs,
            batch_size=5,
            verbose=1
        )

        model.save('./medi_bot_api/chatbot/chatbotmodel.h5', hist)
        print('Training Done')

#
# if __name__ == '__main__':
#     model = ChatBotModel()
#     model.train()