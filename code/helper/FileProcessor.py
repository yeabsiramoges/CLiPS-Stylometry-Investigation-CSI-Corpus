import csv
import json
import functools

class FileProcessor():
    '''
    Supplying needed csv and json processing methods.
    '''
    def __init__(self) -> None:
        '''
        Instantiate file processor.
        '''
        print('FILE-PROCESSOR: Instantiated.')

    @functools.lru_cache
    def get_text(self, input_file, as_list=False):
        '''
        Take a given file by its directory name and return the text as either a list of strings or a string.
        '''
        with open(input_file, 'r+', encoding='latin1') as csv_file:
            reader = csv.reader(csv_file)
            text_list = [str(line) for line in reader]
            return text_list if as_list else ' '.join(text_list)
        
    def dump_json(self, dictionary, output_file):
        '''
        Save an instance of a dictionary object to a given output file.
        '''
        with open(output_file, 'x', encoding='latin1') as json_file:
            json.dump(dictionary, json_file)

    @functools.lru_cache
    def load_json(self, json_file_name):
        '''
        Load json file found at parameters json_file.
        '''
        json_file = open(json_file_name)
        return json.load(json_file)