def Process():
    import nltk
    nltk.download('omw-1.4')  #  imported library error support: nltk

    from . import process
    return process
    
def Others():
    from . import others
    return others
