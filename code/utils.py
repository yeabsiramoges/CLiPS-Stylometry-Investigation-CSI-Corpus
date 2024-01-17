import os
import csv
import json
import nltk

from tqdm import tqdm
from constants import *
from deep_translator import GoogleTranslator

class Translator():
    def __init__(self, source, target) -> None:
        print(f'Translator Instance Instantiated.')
        print(f'Source: {source}')
        print(f'Target: {target}')

        self.translator = GoogleTranslator(source=source, target=target)

    def get_translation(self, text):
        try:
            translation = []
            for sentence in nltk.tokenize.sent_tokenize(text):
                translation.append(self.translator.translate(sentence))
            return ''.join(translation)
        except:
            print('Empty sequence.')
            return ""

class FileProcessor():
    def __init__(self) -> None:
        print('Instantiating File Processor')
        pass

    def get_text(self, input_file, as_list=False, delimiter=','):
        with open(input_file, 'r+', encoding='latin1') as csv_file:
            reader = csv.reader(csv_file, delimiter=delimiter)
            text_list = [str(line) for line in reader]
            return text_list if as_list else ' '.join(text_list)
        
    def dump_json(self, dictionary, output_file):
        json_object = json.dumps(dictionary)
        with open(output_file, 'w', encoding='latin1') as json_file:
            json_file.write(json_object)

    def load_json(self, json_file):
        return json.load(json_file)

class DataLoader():
    def __init__(self) -> None:
        print('Instantiating Data Loader')

        # Processor Helper Classes
        self.fileprocessor = FileProcessor()
        self.translator = Translator(DANISH_CODE, ENGLISH_CODE)

        # Data Setup
        self.reviews = self.generate_reviews() if not os.path.isfile(NEW_REVIEWS) else self.fileprocessor.load_json(NEW_REVIEWS)
        self.essays = self.generate_essays() if not os.path.isfile(NEW_ESSAYS) else self.fileprocessor.load_json(NEW_ESSAYS)

        self.author_data = self.generate_author_data() if not os.path.isfile(NEW_AUTHOR_DATA) else self.fileprocessor.load_json(NEW_AUTHOR_DATA)
        self.document_data = self.generate_document_data() if not os.path.isfile(NEW_DOCUMENT_DATA) else self.fileprocessor.load_json(NEW_DOCUMENT_DATA)

    def generate_reviews(self):
        print('Generating Reviews')
        reviews = {}
        review_file_list = os.listdir(OLD_REVIEWS)
        for index in tqdm(range(len(review_file_list))):
            filename = review_file_list[index]
            # Metadata
            author_ID, genre, timestamp, veracity, sentiment = filename.split("_")
            sentiment = sentiment.split('.')[0]

            # Text
            text = self.fileprocessor.get_text(OLD_REVIEWS + "/" + filename)

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
        print('Generating Essays.')
        essays = {}
        essay_file_list = os.listdir(OLD_ESSAYS)
        for index in tqdm(range(len(essay_file_list))):
            filename = essay_file_list[index]
            # Metadata
            author_ID, genre, timestamp, = filename.split("_")
            sentiment = sentiment.split('.')[0]

            # Text
            text = self.fileprocessor.get_text(OLD_ESSAYS + "/" + filename)

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
    def generate_author_data(self):
        author_data = {}
        author_data_list = self.fileprocessor.get_text(OLD_AUTHOR_DATA, True)
        for line in author_data_list:
            author_id, dob, gender, sexual_perference, region, country, big_five, mbti = line.split(OLD_DATA_DELIMITER)
            author_data[author_id] = {
                'DOB':dob,
                'Gender':gender,
                'Sexual Perference': sexual_perference,
                'Region': region,
                'Country': country,
                'Big Five': big_five,
                'MBTI': mbti
            }
        return author_data

    def generate_document_data(self):
        document_data = {}
        document_data_list = self.fileprocessor.get_text(OLD_DOCUMENT_DATA, True)
        for line in document_data_list:
            filename, author_id, timestamp, genre, grade, sentiment, veracity, category, product, subject = line.split(OLD_DATA_DELIMITER)
            document_data[author_id] = {
               'filename': filename,
               'timestamp': timestamp,
               'genre': genre,
               'grade': grade,
               'sentiment': sentiment,
               'veracity': veracity,
               'category': category,
               'product': product,
               'subject': subject
            }
        return document_data