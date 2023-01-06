def Process():
    import nltk
    nltk.download('omw-1.4')  # support: nltk

    from . import process
    return process
    
def Others():
    from . import others
    return others
