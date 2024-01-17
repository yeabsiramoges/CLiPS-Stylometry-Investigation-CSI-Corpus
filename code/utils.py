import os
import csv
import json
import nltk
import functools

from tqdm import tqdm
from constants import *
from deep_translator import GoogleTranslator

class Translator():
    '''
    Using the GoogleTranslator deep_translator module to quickly generate translation from a given source language to a target one.
    '''
    def __init__(self, source, target) -> None:
        '''
        Instantiate deep translator.
        '''
        print(f'Instantiating Translator')
        print(f'Source: {source}')
        print(f'Target: {target}')

        self.translator = GoogleTranslator(source=source, target=target)

    def get_translation(self, text):
        '''
        Process translation of text passed in.
        '''
        try:
            translation = []
            for sentence in nltk.tokenize.sent_tokenize(text):
                translation.append(self.translator.translate(sentence))
            return ''.join(translation)
        except:
            print('Empty sequence.')
            return ""

class FileProcessor():
    '''
    Supplying needed csv and json processing methods.
    '''
    def __init__(self) -> None:
        '''
        Instantiate file processor.
        '''
        print('Instantiating File Processor')

    @functools.lru_cache
    def get_text(self, input_file, as_list=False, delimiter=','):
        '''
        Take a given file by its directory name and return the text as either a list of strings or a string.
        '''
        with open(input_file, 'r+', encoding='latin1') as csv_file:
            reader = csv.reader(csv_file, delimiter=delimiter)
            text_list = [str(line) for line in reader]
            return text_list if as_list else ' '.join(text_list)
        
    @functools.lru_cache
    def dump_json(self, dictionary, output_file):
        '''
        Save an instance of a dictionary object to a given output file.
        '''
        json_object = json.dumps(dictionary)
        with open(output_file, 'w', encoding='latin1') as json_file:
            json_file.write(json_object)

    def load_json(self, json_file):
        '''
        Load json file found at parameters json_file.
        '''
        return json.load(json_file)

class DataLoader():
    '''
    Load data from old files and save for future use.
    '''
    def __init__(self) -> None:
        '''
        Process review, essay, and author data.
        '''

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
        '''
        Generate reviews from old data store.
        '''
        print('Generating Reviews')
        reviews = {}
        review_file_list = os.listdir(OLD_REVIEWS)
        for index in tqdm(range(len(review_file_list))):
            try:
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
            except:
                print('Unpacking issue at: ', index)
        
        self.fileprocessor.dump_json(reviews, NEW_REVIEWS)
        return reviews
    
    def generate_essays(self):
        '''
        Generate essays from old data store.
        '''

        print('Generating Essays.')
        essays = {}
        essay_file_list = os.listdir(OLD_ESSAYS)
        for index in tqdm(range(len(essay_file_list))):
            try:
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
            except:
                print('Unpacking issue at: ', index)
        
        self.fileprocessor(essays, NEW_ESSAYS)
        return essays
    
    def generate_author_data(self):
        '''
        Generate author data from old data store.
        '''
        author_data = {}
        author_data_list = self.fileprocessor.get_text(OLD_AUTHOR_DATA, True)
        for line in author_data_list:
            try:
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
            except:
                print('Unpacking issue at: ', line)
        return author_data

    def generate_document_data(self):
        '''
        Generate document data from old data store.
        '''

        document_data = {}
        document_data_list = self.fileprocessor.get_text(OLD_DOCUMENT_DATA, True)
        for line in document_data_list:
            try:
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
            except:
                print('Unpacking issue at: ', line)
        return document_data