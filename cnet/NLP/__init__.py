from cnet import codio


def Process():
    # imported library error support: nltk
    import nltk
    nltk.download('omw-1.4')

    from . import process
    return process


def Others():
    from . import others
    return others
