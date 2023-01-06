def Process():
    import nltk
    nltk.download('all')  # support: nltk

    from . import process
    return process
    
def Others():
    from . import others
    return others
