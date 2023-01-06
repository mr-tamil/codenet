import importlib


def Process():
    process = importlib.import_module('process')
    return process

def Others():
    others = importlib.import_moduls('others')
    return others
