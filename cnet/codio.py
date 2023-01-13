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
class setattrs:
	'''Usage:
	setattrs(object, locals())
	setattrs(object, name= name, age= age)
		
	# delete and unself the inserted variables
	__dict__ = setattrs(object, locals())(remove=['age'])
		
------------------------------
# Decorator:
 - testing version:
Error:
 - unassigned parameters are just shows as name=None as a string

Example:---

class Person:
	@setattrs.selfit
	def __init__(self, name=None):
		paes
p = Person("person")
print(p.name)
>>> person
		'''
		
	def __init__(self, obj=None, *args, **kwargs):
		self.do(obj, *args, **kwargs)
	
	def do(self, obj, *args, **kwargs):
		if args:
			assert len(args)==1, f"args must not more than one."
			for k, v in args[0].items():
				setattr(obj, k, v)
				
		elif kwargs:
			for k, v in kwargs.items():
				setattr(obj, k, v)
				
		self.obj = obj
	
	def __call__(self, remove:list=None):
		if remove is not None:
			for r in remove:
				if r in self.obj.__dict__.keys():
					self.obj.__dict__.pop(r)
					
		return self.obj.__dict__
	

	def selfit(func):
		
		@wraps(func)
		def call(*args, **kwargs):
			
			if args:
				get = inspect.signature(func)
				ak = list(get.parameters.keys())
				av = list(get.parameters.values())
				s1, s2= str(get).find("*"), str(get).rfind("**")
				one, two = False, False
				
				if s1 != -1 and s2 == -1:
					'one'
					one = True
					
				'''
				if s1 == -1 and s2 == -1:
					'no one, no two'
				
				if s1 == s2 and s1 != -1 and s2 != -1:
					'two'
					two = True
				if s1 != s2 and s1 != -1 and s2 != -1:
					'one and two'
					one, two = True, True
				'''
				
				obj = args[0]
				
				# kwargs empty
				kk = kwargs.keys()
				for i, a in enumerate(ak[1:]):
					if a not in kk:
						kwargs[a] = av[i+1]
						
							
				if len(args)>1 and not one:
					args = list(args)
					for i, a in enumerate(args[1:]):
						kwargs[ak[i+1]]= a
						del args[1]
						
					args = tuple(args)
				
				if obj:
					for k, v in kwargs.items():
						setattr(obj, k, v)
						
			output = func(*args, **kwargs)
			return output
			
		return call
		






# Objectize the list, dict
class Objectize:
    '''
    # Usage:

    # object = Objectize.list(['name', 'age'], ["name", 0])
    object = Objectize.dict({'name': 'age', "name": 0})

    # Access using index
    print(object[0])

    # Access using name
    print(object.name)

    # Access using getattr()
    print(getattr(object, 'name'))
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
