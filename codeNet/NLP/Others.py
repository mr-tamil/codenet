print("""Others :: Others model in NLP""")


# import modules
from codeNet.codio import install_packages, install_package, command_call


# install packages
install_packages(["fasttext", "spacy", "gensim"])
command_call("!pip install -U setuptools")


# import libraries
import fasttext
import spacy
from spacy import displacy
import gensim.downloader as api


#: 1. Spacy Model

SPACY_MODELS_NAME = ['small', 'medium', 'large', 'too-large']


def Spacy(model:SPACY_MODELS_NAME= "small"):
    """
    websitelink:URL1: https://spacy.io/api/doc
    websitelink:URL2: https://spacy.io/models/en
    
    rendered = displacy.render(doc, style= 'ent')
    """
    
    # Parameter Value Error Check
    assert model in SPACY_MODELS_NAME, f"model must be in {SPACY_MODELS_NAME}"
    
    # set mentioned model name
    if model== 'small':
        install_package("en_core_web_sm")
        model_name = "en_core_web_sm"
        
    elif model== 'medium':
        install_package("en_core_web_md")
        model_name = "en_core_web_md"
        
    elif model== 'large':
        install_package("en_core_web_lg")
        model_name = "en_core_web_lg"
        
    elif model== 'too-large':  # testing version model
        install_package('spacy[transformers]')
        model_name = "en_core_web_trf"
    
    # load model
    nlp = spacy.load(model_name)

    def call(text: str):
        doc = nlp(text)
        return doc

    return call


#: 2. Gemsim Model

def gensim(model= "word2vec-google-news-300"):
    '''
    websitelink: https://github.com/RaRe-Technologies/gensim-data
    
    Examples:
        most_similar = model.most_similar(positive=positive, negative=negative)
    '''
    
    # load model
    model = api.load(model)
    
    return model


#: 3. FastText Model

def fastText(input: "dataset.txt"):
    '''
    Examples:
        nearest_neighbors = model.get_nearest_neighbors('word')
    '''

    # load model
    model = fasttext.train_unsupervised(input= input)
    
    return model
