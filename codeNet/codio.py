"""codio: Code Toolkit for I/O"""


# import libraries
import os, sys, subprocess, importlib


# libraries easy access method:---
	
# dill source direct call
from dill import source

# get file source code
from dill.source import getsource

# --------------------------------


# terminal command call by subprocess
def command_call(cmd: str):
	subprocess.check_call(cmd.split())


# install single package
def install_package(name)->None:
    if importlib.util.find_spec(name) is None:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', name])


# install list of packages
def install_packages(names:['packages'])->None:
    for name in names:
        install_package(name)
	

# disable print output
def disablePrint():
    sys.stdout = open(os.devnull, 'w')


# enable print output
def enablePrint():
    sys.stdout = sys.__stdout__


# eable or disable print output on with statement
class PrintStatements:
    '''
    with PrintStatements(state=True):
    	# will print
    	
    with PrintStatements(state=True):
    	# will not print
    '''
    
    def __init__(self, state= True):
        # :param: state: True or False
        self.state = state
    	
    def __enter__(self):
        if not self.state:
            sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self.state:
            sys.stdout.close()
            sys.stdout = sys.__stdout__
