import nltk

from deep_translator import GoogleTranslator

class Translator():
    '''
    Using the GoogleTranslator deep_translator module to quickly generate translation from a given source language to a target one.
    '''
    def __init__(self, source, target) -> None:
        '''
        Instantiate deep translator.
        '''
        print(f'TRANSLATOR: Instantiated ({source}, {target}).')

        self.translator = GoogleTranslator(source=source, target=target)
        self.auto = GoogleTranslator(source='auto', target=target)

    def get_translation(self, text):
        '''
        Process translation of text passed in.
        '''
        try:
            translations = []
            for sentence in nltk.tokenize.sent_tokenize(text):
                translation = self.translator.translate(sentence)
                re_translation = self.auto.translate(translation)
                translations.append(re_translation)
            return ''.join(translations)
        except:
            print('TRANSLATOR: Error at ', text)