from . import codio

NLP_CREATED = None
def NLP():
    nlp = NLP_CREATED
    if NLP_CREATED is None:
        from . import NLP as nlp
        NLP_CREATED = nlp
    return nlp


