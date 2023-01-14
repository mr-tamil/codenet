"""codio: Code Toolkit for I/O"""
__version__ = "0.1.1"

# import libraries assist
import os, sys, subprocess, importlib, io, imp, types, time, inspect
from collections import namedtuple
from functools import wraps


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

# get members
from inspect import getmembers

# filter warnings
from warnings import filterwarnings
# --------------------------------


# setattr method to set attrs
def setattrs(obj, *args, **kwargs):
    '''Usage:--
obj_dict = setattrs(object, locals())
obj_dict = setattrs(object, name= name, age= age)


Example:--
class Person: pass
p = Person()
d = {'name':'Dinesh', 'age':22}
    

get = setattrs(p, name='Dinesh',age=22)
get = setattrs(p, d)

print(p.name)
print(p.age)
    
----or ----------------------------
class Person:
    def __init__(self, name, age):
        get_dict = setattrs(self, name=name, age=age)
	del get_dict['self']
   '''
    
    if args:
        assert len(args)==1, f"args must not more than one."
        for k, v in args[0].items():
            setattr(obj, k, v)
            
    elif kwargs:
        for k, v in kwargs.items():
            setattr(obj, k, v)
            
    return obj.__dict__

# Objectise: Objectise the list, dict
class Objectise:
    '''Usage:
    l = Objectise.list(['name'], ['Tamil'])
    d = Objectise.dict({'name':'Dinesh'})
    
    print(l.name)
    print(d.name)
    '''

    def list(keys, values, name='id'):
        class objectise: pass
    
        obj = objectise()
        obj.__class__.__name__ = name
        objdict = obj.__dict__
        for i, key in enumerate(keys):
            objdict[key] = values[i]
        return obj

    def dict(dict_, name='id'):
        class objectise: pass
    
        obj = objectise()
        obj.__class__.__name__ = name
        objdict = obj.__dict__
        for key, value in dict_.items():
            objdict[key] = value
        return obj



# TupleInstantiate: Instantiate the list, dict
class TupleInstantiate:
    '''
    # Usage:

    # instance = TupleInstantiate.list(['name', 'age'], ["name", 0])
    instance = TupleInstantiate.dict({'name': 'age', "name": 0})

    # Access using index
    print(instance[0])

    # Access using name
    print(instance.name)

    # Access using getattr()
    print(getattr(instance, 'name'))
    '''


    def list(keys, values, identifier="id"):
        nt = namedtuple(identifier, keys)
        n = nt(*values)
        return n

    def dict(dict_, identifier="id"):
        keys, values = list(dict_.keys()), list(dict_.values())
        nt = namedtuple(identifier, keys)
        n = nt(*values)
        return n


# create new module on running code and access it
def create_modula(script:str, name:str=None, delete=True):
    """
    Note: don't use variables: __start__, __end__
    """

    script = f"""__start__ = 'Future use variable'\n{script}\n__end__ = globals()"""
    
    if name is None:
        name = str(time.time())

    module_path = name
    with open(module_path, "w") as file:
        file.write(script)

    with io.open(module_path) as scriptfile:
        code = compile(scriptfile.read(),module_path,'exec')
        module = imp.new_module(name)
        exec(code, module.__dict__)

    if delete is True:
        os.remove(module_path)

    return module


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

def mkdirz(directory, lis):
	for f in lis:
		path = directory
		for d in f[:-1]:
			path = os.path.join(path, d)
			os.mkdir(path)
