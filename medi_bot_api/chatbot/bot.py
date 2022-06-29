import nltk
import random
import numpy as np
import json
import pickle
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model


class ChatBot():
    """
        Responsible on handling the chat bot(Intent classification generating responses)
    """
    def __init__(self):
        self.base_dir = './medi_bot_api/chatbot/'
        self.lemmatizer = WordNetLemmatizer()
        self.words = pickle.load(open(self.base_dir + 'words.pkl', 'rb'))
        self.classes = pickle.load(open(self.base_dir + 'classes.pkl', 'rb'))
        self.json_file = open(self.base_dir + 'intents.json')
        self.intents = json.load(self.json_file)
        self.model = None

    def clean_up_sentence(self, sentence):
        """
            :param sentence: str - sentence/pattern from the user
            :rtype: list -  returns Summarized sentence
        """
        sentence_words = nltk.word_tokenize(sentence)
        sentence_words = [self.lemmatizer.lemmatize(word) for word in sentence_words]
        return sentence_words

    def bag_of_words(self, sentence):
        """
            :param sentence: str sentence/pattern from the user
            :rtype: np array - returns bag of words
        """
        sentence_words = self.clean_up_sentence(sentence)
        bag = [0] * len(self.words)
        for w in sentence_words:
            for i, word in enumerate(self.words):
                if word == w:
                    bag[i] = 1
        return np.array(bag)

    def predict_class(self, sentence):
        """
            :param sentence: str sentence/pattern from the user
            :rtype: list - returns processed dataset list of dict[{intent, probability}), ...]
        """
        bow = self.bag_of_words(sentence)

        # load model
        self.model = load_model('./medi_bot_api/chatbot/chatbotmodel.h5')

        res = self.model.predict(np.array([bow]))[0]
        ERROR_THRESHOLD = 0.25
        results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

        results.sort(key=lambda x: x[1], reverse=True)
        return_list = []

        for r in results:
            return_list.append({'intent': self.classes[r[0]], 'probability': str(r[1])})
        return return_list

    def get_response(self, intents_list, intents_json):
        """

            :param intents_list: list -  list of intents
            :param intents_json: json load
            :rtype: string - random response
        """
        tag = intents_list[0]['intent']
        list_of_intents = intents_json['intents']

        # print(tag)

        result = 'N/A'

        for i in list_of_intents:
            if i['tag'] == tag:
                result = random.choice(i['responses'])
                break
        return result

