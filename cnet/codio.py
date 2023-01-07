"""codio: Code Toolkit for I/O"""


# import libraries assist
import os, sys, subprocess, importlib


# install single package
def install_package(name)->None:
    if importlib.util.find_spec(name) is None:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', name])


# install list of packages
def install_packages(names:['packages'])->None:
    for name in names:
        install_package(name)


# install libraries
install_packages(['dill'])


# libraries easy access method:---
	
# dill source direct call
from dill import source

# get file source code
from dill.source import getsource

# --------------------------------


def cfpname(func):
    '''
    cfpname = class function parent name
    
    Explanation:
    	class Files:
    		def delete(self):
    			pass
    	
    	>> cfpname(Files.delete)
    	<< Files.delete
    	
    	
    '''
    
    str_list = str(func).split()
    
    if 'of' in str_list:
        index= str_list.index('of')
    elif 'at' in str_list:
        index = str_list.index('at')
    else:
    	index = None
    
    if index is not None:
    	return str_list[index-1]
    else:
    	get = str_list[1].split("'")[1]
    	if get.startswith('__main__.'):
    		get = get[9:]
    	return get
    	

def typesof(obj):
    '''type(obj) in all ways'''
    
    checker = {
         "method": source.ismethod,
         "def": source.isfunction,
         "class": source.isclass,
    }
    
    total_chances = []
    for check in checker.items():
        ans = check[1](obj)
        if ans:
            total_chances.append(check[0])
	
    return total_chances



# terminal command call by subprocess
def command_call(cmd: str):
	subprocess.check_call(cmd.split())


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
            self.__stdout__ = sys.stdout
            sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self.state:
            sys.stdout.close()
            sys.stdout = self.__stdout__
