import os
import re

from tqdm import tqdm
from helper.constants import *

class DataLoader():
    '''
    Load data from old files and save for future use.
    '''
    def __init__(self, fileprocessor, translator) -> None:
        '''
        Process review, essay, and author data.
        '''

        print('DATALOADER: Instantiated.')

        # Processor Helper Classes
        self.fileprocessor = fileprocessor
        self.translator = translator

        # Data Setup
        self.reviews = self.generate_reviews()
        self.essays = self.generate_essays()

        self.author_data = self.generate_author_data()
        self.document_data = self.generate_document_data()

    def generate_reviews(self):
        '''
        Generate reviews from old data store.
        '''
        print('DATALOADER: Generating Reviews')

        reviews = {}
        file_exists = os.path.isfile(NEW_REVIEWS)
        if file_exists:
             reviews = self.fileprocessor.load_json(NEW_REVIEWS)
        else:
            review_file_list = os.listdir(OLD_REVIEWS)
            for index in tqdm(range(len(review_file_list))):
                try:
                    filename = review_file_list[index]
                    # Metadata
                    author_ID, genre, timestamp, veracity, sentiment = filename.split("_")
                    sentiment = sentiment.split('.')[0]
                    author_ID = self.extract(author_ID)

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
                     print('DATALOADER: Invalid Review of ', review_file_list[index])

            self.fileprocessor.dump_json(reviews, NEW_REVIEWS)
        return reviews
    
    def generate_essays(self):
        '''
        Generate essays from old data store.
        '''

        print('DATALOADER: Generating Essays')
        essays = {}
        file_exists = os.path.isfile(NEW_ESSAYS)
        essay_file_list = os.listdir(OLD_ESSAYS)

        if file_exists:
             essays = self.fileprocessor.load_json(NEW_ESSAYS)
        else:
            for index in tqdm(range(len(essay_file_list))):
                try:
                    filename = essay_file_list[index]
                    # Metadata
                    author_ID, genre, timestamp, = filename.split("_")
                    author_ID = self.extract(author_ID)

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
                     print('DATALOADER: Invalid Essay of ', essay_file_list[index])
            self.fileprocessor.dump_json(essays, NEW_ESSAYS)
        return essays
    
    def generate_author_data(self):
        '''
        Generate author data from old data store.
        '''
        print('DATALOADER: Generating Author Data')
        author_data = {}
        author_data_list = self.fileprocessor.get_text(OLD_AUTHOR_DATA, True)
        file_exists = os.path.isfile(NEW_AUTHOR_DATA)

        if file_exists:
             author_data = self.fileprocessor.load_json(NEW_AUTHOR_DATA)
        else:
            for index in tqdm(range(len(author_data_list))):
                line = author_data_list[index]
                try:
                    author_id, dob, gender, sexual_perference, region, country, big_five, mbti = line.split('\\t')
                    author_id = self.extract(author_id)
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
                    print('DATALOADER: Invalid Author of ', line)
            self.fileprocessor.dump_json(author_data, NEW_AUTHOR_DATA)
        return author_data

    def generate_document_data(self):
        '''
        Generate document data from old data store.
        '''
        print('DATALOADER: Generating Document Data')
        document_data = {}
        document_data_list = self.fileprocessor.get_text(OLD_DOCUMENT_DATA, True)
        file_exists = os.path.isfile(NEW_DOCUMENT_DATA)
        
        if file_exists:
             document_data = self.fileprocessor.load_json(NEW_DOCUMENT_DATA)
        else:
            for index in tqdm(range(len(document_data_list))):
                line = document_data_list[index]
                try:
                    filename, author_id, timestamp, genre, grade, sentiment, veracity, category, subject = line.split('\\t')
                    author_id = self.extract(author_id)
                    document_data[author_id] = {
                        'filename': filename,
                        'timestamp': timestamp,
                        'genre': genre,
                        'grade': grade,
                        'sentiment': sentiment,
                        'veracity': veracity,
                        'category': category,
                        'subject': subject
                    }
                except:
                    print('DATALOADER: Invalid Document of ', line)
            self.fileprocessor.dump_json(document_data, NEW_DOCUMENT_DATA)
        return document_data
    
    def get_data(self):
         '''
         Get processed data in dict.
         '''
         print('DATALOADER: Data Loaded.')
         return {
              'reviews': self.reviews,
              'essays': self.essays,
              'author': self.author_data,
              'document': self.document_data
         }
    
    def extract(self, text):
         '''
         Extract digit from string.
         '''
         return ''.join(num for num in text if num.isdigit())