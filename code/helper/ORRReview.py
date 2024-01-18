import csv
import openreview

from helper.constants import *

class Review:
    def __init__(self, fileprocessor) -> None:
        print('ORRREVIEW: Instantiated.')
        self.client = openreview.Client(
            baseurl='https://api.openreview.net', 
            username=USERNAME, 
            password=PASSWORD
        )
        self.fileprocessor = fileprocessor
        self.all_reviews = {}
    
    def get_venues(self, filter=''):
        venues = []
        for venue in self.client.get_group(id='venues').members:
            if filter in venue:
                venues.append(venue)
        return venues
    
    def scrape_all_reviews(self):
        reviews = {}
        titles = {}

        venues = self.get_venues(filter='Conference')

        for venue in venues:
            sub_reviews, sub_titles = self.scrape_reviews(venue)

            reviews.update(sub_reviews)
            titles.update(sub_titles)

        return reviews, titles
    
    def scrape_reviews(self, venue='ICLR.cc/2019/Conference'):
        reviews = {}
        titles = {}

        invitation = venue+'/-/Blind_Submission'
        notes = openreview.tools.iterget_notes(self.client, invitation=invitation, details='directReplies')

        for note in notes:
            content = note.content
            title = content['title']
            reviews[title] = []

            replies = note.details['directReplies']
            for reply in replies:
                reviews[title].append(reply['content'])
                titles[title] = content

        return reviews, titles
    
    def get_reviews(self):
        return self.all_reviews
    
    def word_processor(self, text):
        return text

    def get_data(self):
        print('ORRREVIEW: Getting data.')
        review_to_sentence = {}
        
        with open(PROCESSED_DATA, 'r', encoding='latin') as processed_data:
            csvreader = csv.reader(processed_data)

            # Go through reader and save every sentence to its appropriate review
            for line in csvreader:
                try:
                    review_id, sentence_id, text, label1, label2, _ = self.word_processor(line)
                    review = {
                        'text': text,
                        'label1': label1,
                        'label2': label2
                    }
                    review_to_sentence[(review_id, sentence_id)] = review
                except:
                    print('ORRREVIEW: Error at ', line)
                    pass

        return review_to_sentence

if __name__ == '__main__':
    pass