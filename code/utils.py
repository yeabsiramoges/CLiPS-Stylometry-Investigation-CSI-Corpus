import os
import csv
import json
import nltk

from constants import *
from deep_translator import GoogleTranslator

class Translator():
    def __init__(self, source, target) -> None:
        nltk.download('popular')
        self.translator = GoogleTranslator(source=source, target=target)

    def get_translation(self, text):
        translation = []
        for sentence in nltk.tokenize.sent_tokenize(text):
            translation.append(self.translator.translate(sentence))
        return ''.join(translation)

class FileProcessor():
    def __init__(self) -> None:
        pass
    def get_reader(self, input_file):
        with open(input_file, 'r+', encoding='latin1') as csv_file:
            return csv.reader(csv_file)
    def dump_json(self, dictionary, output_file):
        json_object = json.dumps(dictionary)
        with open(output_file, 'w', encoding='latin1') as json_file:
            json_file.write(json_object)
    def load_json(self, json_file):
        return json.load(json_file)

class DataLoader():
    def __init__(self) -> None:
        # Processor Helper Classes
        self.fileprocessor = FileProcessor()
        self.translator = Translator(DANISH_CODE, ENGLISH_CODE)

        # Data Setup
        self.reviews = self.generate_reviews() if not os.path.isfile(NEW_REVIEWS) else self.fileprocessor.load_json(NEW_REVIEWS)
        self.essays = self.generate_essays() if not os.path.isfile(NEW_ESSAYS) else self.fileprocessor.load_json(NEW_ESSAYS)

    def generate_reviews(self):
        reviews = {}
        review_file_list = os.listdir(OLD_REVIEWS)
        for filename in review_file_list:
            # Metadata
            author_ID, genre, timestamp, veracity, sentiment = filename.split("_")
            sentiment = sentiment.split('.')[0]

            # Text
            text = self.fileprocessor.get_reader(OLD_REVIEWS + "/" + filename)

            # Bundling
            new_review = {
                'genre': genre,
                'timestamp': timestamp,
                'veracity': veracity,
                'sentiment': sentiment,
                'text': self.translator.get_translation(text)
            }

            # Storage
            if author_ID in reviews:
                reviews[author_ID].append(new_review)
            else:
                reviews[author_ID] = [new_review]
        
        self.fileprocessor.dump_json(reviews, NEW_REVIEWS)
        return reviews
    
    def generate_essays(self):
        essays = {}
        essay_file_list = os.listdir(OLD_ESSAYS)
        for filename in essay_file_list:
            # Metadata
            author_ID, genre, timestamp, = filename.split("_")
            sentiment = sentiment.split('.')[0]

            # Text
            text = self.fileprocessor.get_reader(OLD_ESSAYS + "/" + filename)

            # Bundling
            new_review = {
                'genre': genre,
                'timestamp': timestamp,
                'text': self.translator.get_translation(text)
            }

            # Storage
            if author_ID in essays:
                essays[author_ID].append(new_review)
            else:
                essays[author_ID] = [new_review]
        
        self.fileprocessor(essays, NEW_ESSAYS)
        return essays

if __name__ == "__main__":
    dataloader = DataLoader()