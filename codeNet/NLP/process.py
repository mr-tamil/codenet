"""Prcess :: Some techniques and tools for processing the NLP"""

# import modules
from .codio import install_packages, install_package


# install packages
install_packages(['re', 'nltk', 'spacy', 'pattern', 'deepmultilingualpunctuation', 'transformers'])


# import libraries
import re
import spacy
import nltk
from nltk.stem.porter import PorterStemmer
from pattern.en import lemma, lexeme
from nltk.stem import WordNetLemmatizer
from transformers import BertTokenizer, AutoTokenizer, AutoModelForTokenClassification, TokenClassificationPipeline, pipeline
from deepmultilingualpunctuation import PunctuationModel


# additional libraries for imported libraries:
install_package('sentencepiece') # support: deepmultilingualpunctuation


#: 1. Punctuation

class Punctuate:
    """
    websitelink: https://huggingface.co/oliverguhr/fullstop-punctuation-multilang-large
    """

    def __init__(self)-> None:
        # load model
        self.model = PunctuationModel()

    def __call__(self, sequence: [str, [str]]) -> str:
        punctuated_text =  self.model.predict(sequence)
        
        if isinstance(sequence, list):
            str_zero = '0'
            punctuated_text_temp = ""
            
            for word in punctuated_text:
                punctuated_text_temp += word[0]
                get_punc = word[1]
                
                if get_punc == str_zero:
                    punctuated_text_temp += " "
                else:
                    punctuated_text_temp += get_punc
                    
            punctuated_text = punctuated_text_temp

        return punctuated_text
        

#: 2. Word Split

def WordSplit():
    '''splits the word from sentence or sentences'''
    
    def call(sequence: str) -> [str]:
        sequence = re.sub(r"(?<!\d)[.,;:!?](?!\d)","",sequence)
        return sequence.split()
        
    return call



#: 3. Sentence Split

def SentenceSplit():
    '''splits the sentence from sentences'''
    
    # load model
    nlp = spacy.load("en_core_web_sm")
    
    def call(sequence: str) -> [str]:
        sentences = nlp(sequence)
        return list(sentences.sents)

    return call
    



#: 3. Stop Words

STOPWORD_BASE_NAMES = ['nltk','spacy']


class StopWords:
    '''
    remove the stopwords from the given 1d list of words
    '''
    
    def __init__(self, base: STOPWORD_BASE_NAMES='spacy')-> None:
        # Parameter Value Error Check
        assert base in STOPWORD_BASE_NAMES, f"base must be one of {STOPWORD_BASE_NAMES}."
        
        # load mentioned model
        if base == 'spacy':
            # set stopwords
            from spacy.lang.en.stop_words import STOP_WORDS
            self.stop_words = STOP_WORDS
            
        if base == 'nltk':
            # download base file
            nltk.download('stopwords')
            
            # set stopwords
            from nltk.corpus import stopwords
            self.stop_words = stopwords
    
    def __call__(self, words:list)-> list:
        get = [word for word in words if word not in self.stop_words]
        return get


#: 4. Stemming

def Stemming():
    '''returns stem word of the 1d list od words'''
    
    # initialize model
    ps = PorterStemmer()
    
    def call(sequence: list) -> list:
        return [ps.stem(word) for word in sequence]
        
    return call



#: 5. Lemmatizing

LEMMA_BASE_NAMES = ['wordnet', 'pattern']


class Lemmatizing():
    '''Lemmatize the 1d list of words and returns as the same size'''
    
    def __init__(self, base: LEMMA_BASE_NAMES= 'pattern')-> None:
        # Parameter Value Error Check
        assert base in LEMMA_BASE_NAMES, f"base must be one of the {LEMMA_BASE_NAMES}"
        
        # download the base file
        nltk.download('omw-1.4')
        
        # load mentioned model
        if base == 'pattern':
            self.bengine = lemma
            
        if base == 'wordnet':
            lem = WordNetLemmatizer()
            self.bengine = lem.lemmatize

    def __call__(self, sequence: list) -> list:
        output = [self.bengine(word) for word in sequence]
        return output


#: 6. Lexemetizing

def Lexeme():
    '''get the posiblities of the lemma of 1d list of words'''
    
    # download the base file
    nltk.download('omw-1.4')
    
    def call(sequence: list) -> list:
        return [lexeme(word) for word in sequence]
        
    return call


#: 7. Parts of Speech Tagging (POS)

def PosTaging():
    """
    count = doc.count_by(spacy.attrs.POS)
    name = doc.vocab[96].text
    Note: Bert POS Tagging has some disadvantage compared to Spacy
    """
    
    # load model
    nlp = spacy.load("en_core_web_sm")
    
    def call(sequence: str) -> list:
        doc = nlp(sequence)
        pos_tags = []
        for token in doc:
            pos_tags.append([token, (token.pos_, spacy.explain(token.pos_)), (token.tag_, spacy.explain(token.tag_))])
        return pos_tags
        
    return call


#: 8. Named Entity Recognition (NER)

NER_BASE_NAMES = ['spacy', 'bert']


class Ner:
    '''
    Named Entity Recognition of the given sentences or paragraph
    '''
    
    def __init__(self, base: NER_BASE_NAMES= 'spacy'):
        # Parameter Value Error Check
        assert base in NER_BASE_NAMES, f"base must be one of the {NER_BASE_NAMES}"
        
        self.base = base
        
        # load mentioned model
        if base == 'spacy':
            self.bengine = spacy.load("en_core_web_sm")
        
        if base == 'bert':
            self.bengine = pipeline('ner')

    def __call__(self, sequence):
        if self.base == "spacy":
            result = [({"word": word.text,
                        "entity": word.label_,
                        "char_start": word.start_char,
                        "char_end": word.end_char,
                        "word_start": word.start,
                        "word_end": word.end}) for word in self.bengine(sequence).ents]
        else:
            result = [word for word in self.bengine(sequence)]

        return result


#: 9. Tokenization

class Token:
    '''
    Token related methods;
    '''
    
    def __init__(self, cased = False) -> None:
        #:param: cased: True or False; cased tokens are considered
        
        checkpoint = "bert-base-cased" if cased else "distilbert-base-uncased-finetuned-sst-2-english"
        self.bertTokenizer = BertTokenizer.from_pretrained(checkpoint)
        self.tokenizer = AutoTokenizer.from_pretrained(checkpoint)

    def autokenize(self, batches: list) -> dict:
        # :param: batches: [['hello', 'world'], ['i', 'am']]
        # :return: dict: -
        
        output = self.bertTokenizer(batches, padding=True, truncation=True, return_tensors="pt")
        return output
    
    def tokenize(self, sequence: 'text') -> ['words']:
        tokens = self.tokenizer.tokenize(sequence)
        return tokens
    
    def tokens_to_ids(self, tokens: ['words']) -> ['ids']:
        ids = self.tokenizer.convert_tokens_to_ids(tokens)
        return ids
    
    def encode(self, sequence: 'text') -> ['ids']:
        """combination of tokenize ins and  tokens_to_ids ins (with [cls], [sep])"""
        
        ids = self.tokenizer.encode(sequence)
        return ids

    def decode(self, ids: ['ids']) -> 'text':
        text = self.tokenizer.decode(ids)
        return text
