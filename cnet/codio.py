"""codio: Code Toolkit for I/O"""

# import libraries assist
import os, sys, subprocess, importlib, io, imp, types, time, inspect, json, datetime
from collections import namedtuple
from functools import wraps
from json import JSONDecodeError

# import package modules
from cnet.config import cnetconfig, cnet_basic_config_data


# install single package
def install_package(name)->None:
    if importlib.util.find_spec(name) is None:
        try:
            import pip 
            pip.main(['install', name])
        except:
            # subprocess.check_call([sys.executable, '-m', 'pip', 'install', name])
            os.system(f"python -m pip install {name}")


# install list of packages
def install_packages(names:['packages'])->None:
    for name in names:
        install_package(name)


# install libraries
install_packages(['dill', 'pandas'])

# import installable libraries
# pandas will be imported, if need


# libraries easy access method:---

# pprint: preaty print
from pprint import pprint

# dill source direct call
from dill import source

# get file source code
from dill.source import getsource

# get members
from inspect import getmembers

# filter warnings
from warnings import filterwarnings
# --------------------------------


# jprint: json print
def _jprint(func):
    '''
    from cnet.codio import jprint

    # json print
    jprint({'name': 'Thamizh'})
    '''
    @wraps(func)
    def call(*args, **kwargs):
        if 'indent' not in kwargs.keys():
            kwargs['indent'] = 4
        try:
            result = func(*args, **kwargs)
            print(result)
        except:
            del kwargs['indent']
            print(*args, **kwargs)
        
    
    return call

jprint = _jprint(json.dumps)






def import_module(globals_, module, install=True):
    '''Usage:
from cnet.codio import import_module


# :param : install: default; True  # if module not exists, install it

import_module(globals(), 'inspect.signature')
import_module(globals(), ('pandas', 'pd'))
import_module(globals(), ['numpy', 'np'])
import_module(globals(), 'dill')

    '''

    assert isinstance(module, list) or isinstance(module, tuple) or isinstance(module, set) or isinstance(module, str), f"only str, tuple, list, set of module list is allowed"
    if isinstance(module, str):
        module = module.strip()
        if install is True:
            install_package(module.split('.')[0])

        try:
            globals_[module.split('.')[-1]] = importlib.import_module(module)
        except ModuleNotFoundError:
            get, getcf = module.rsplit('.', 1)
            globals_[module.split('.')[-1]] = getattr(importlib.import_module(get), getcf)

    else:
        if isinstance(module, tuple) or isinstance(module, set):
            module = list(module)

        module[0] = module[0].strip()
        module[1] = module[1].strip()

        if install is True:
            install_package(module[0].split('.')[0])
        try:
            globals_[module[1]] = importlib.import_module(module[0])
        except ModuleNotFoundError:
            get, getcf = module[0].rsplit('.', 1)
            globals_[module[1]] = getattr(importlib.import_module(get), getcf)




def import_modules(globals_, modules:list, install=True):
    '''Usage:
from cnet.codio import import_modules

import_modules(globals(), 
         [
	 'inspect.signature',
         ('pandas', 'pd'),
	 ('numpy', 'np'),
	 'dill'
	  ], install= True  # if module not exists, install it
)
    '''

    for module in modules:
        import_module(globals_, module, install)


# import libraries from file
def impfilelib(globals_, filepath):
    '''Usage:
from  cnet.codio import impfilelib

# use modules that have been import
impfilelib(globals(), 'file.tx')

Note: format
'------
os
sys
numpy, np
pandas, pd
'------
    '''
    lines = open(filepath).readlines()
    modules = []
    for line in lines:
        if line.count(',') == 1:
            get = line.split(',')
            get[0], get[1] = get[0].strip(), get[1].strip()
            if get[0] and get[1]:
                modules.append((get[0], get[1]))
            if get[0] and not get[1]:
                modules.append(get[0])
        else:
            get = line.strip()
            if get:
                modules.append(get)

    import_modules(globals_, modules)


def onelib(globals_, project='default'):
    '''Usage:
from  cnet.codio import onelib

# use modules that have been import
onelib(globals(), 'default')
    -----------
add project in (:project:json) variable:: developer mode only now:: codenet/cnet/_project_libraries.py
	'''

    from cnet._project_libraries import project as P

    if project in P.keys():
        import_modules(globals_, P[project])
    else:
        raise Exception(f"project must be in {', '.join(P.keys())}")

# -----------------------------------------------------

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

# Objectize: Objectize the list, dict
class Objectize:
    '''Usage:
    l = Objectize.list(['name'], ['Tamil'])
    d = Objectize.dict({'name':'Dinesh'})
    
    print(l.name)
    print(d.name)
    '''

    def list(keys, values):
        class objectize: pass
    
        obj = objectize()
        objdict = obj.__dict__
        for i, key in enumerate(keys):
            objdict[key] = values[i]
        return obj

    def dict(dict_):
        class objectize: pass
    
        obj = objectize()
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
    try:
        with io.open(module_path) as scriptfile:
            code = compile(scriptfile.read(),module_path,'exec')
            module = imp.new_module(name)
            exec(code, module.__dict__)
            
    except Exception as e:
        module = None
        print(e)
        
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
        v = str_list[index-1]
        while '<' in v:
            v1 = v.split('<')[0]
            v2 = v.split('>')[-1]
            v= v1 + v2[1:]
        return v

    else:
        get = str_list[1].split("'")[1]
        if get.startswith('__main__.'):
            get = get[9:]

        while '<' in get:
            get1 = get.split('<')[0]
            get2 = get.split('>')[-1]
            get = get1 + get2[1:]

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


# display helper function
class _wprint:
    # enable or disable print output using with-statement
    def __init__(self, state:bool=True):
        self.state = state
    	
    def __enter__(self):
        if not self.state:
            self.__stdout__ = sys.stdout
            sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self.state:
            sys.stdout.close()
            sys.stdout = self.__stdout__

    # disable print output
    def disable():
        sys.stdout = open(os.devnull, 'w')

    # enable print output
    def enable():
        sys.stdout = sys.__stdout__


# display class helper
class __displaycls:
    """Usage:
    display.store = True
    display.storelength = 2
    display(display.memory('%M %Y %D'))

    display()  # same as IPython.display.display
    display.enable()  # will print
    display.disable()  # won't print
    
    with display.print(state=True):
        '''will print'''
        
    with display.print(state=False):
        '''will not print'''
    
    Note:
    if disabled in Hupiter NoteBook, need to restart runtime to print normally else won't print after enabled or not
    """

    def __init__(self) -> None:
        global  _wprint
        # display function helper: only disable or enable the print function
        self.print = _wprint

        self.__dle = False  # display_library_enabled

        # set default or take from config file
        try:
            self.__store = cnetconfig.mainfile['display']['store']
            self.__storelength = cnetconfig.mainfile['display']['storelength']
        except KeyError:
            self.__store = cnet_basic_config_data['display']['store']
            self.__storelength = cnet_basic_config_data['display']['storelength']
            cnetconfig.mainfile.append({'display': cnet_basic_config_data['display']}, indent=4)


    def __call__(self, *objs, name=None, include=None, exclude=None, metadata=None, transient=None, display_id=None, **kwargs):  # parameters changable:

        if self.__dle is False:
            global _display
            from IPython.display import display as _display
            self.__dle = True
        

        # run display here
        time_start = time.time()
        output = _display(*objs, include=include, exclude=exclude, metadata=metadata, transient=transient, display_id=display_id, **kwargs)

        if self.__store is True:
            file = cnetconfig.getfile('display-storage.json')
            try:
                file_data = file.read()
            except JSONDecodeError:
                file.clear()
                file_data = file.read()

            length = len(file_data)
            keys = list(file_data.keys())
            if not length < self.__storelength:
                if self.__storelength != length:
                    file_data_new = {}
                    for k in keys[length-self.__storelength+1:]:
                        file_data_new[k] = file_data[k]
                    file_data = file_data_new
                else:
                    key_d = keys[0]
                    del file_data[key_d]
						

            store_content = {
                    'time': time_start,
                    'name': name,
                    'value': objs,
            }
            try:
                n = int(keys[-1])+1
                file_data[n] = store_content
            except:
                n = 0
                file_data[n] = store_content
            
            try:
                file.write(file_data, indent=4)
            except:
                store_content['value'] = str(objs)
                file_data[n] = store_content
                file.write(file_data, indent=4)


        return output
    
    @property
    def store(self):
        return self.__store

    @store.setter
    def store(self, value:bool):
        assert isinstance(value, bool), f"value {value} must be True or False"
        self.__store = value
        read_display = cnetconfig.mainfile.read()
        read_display['display']['store'] = value
        cnetconfig.mainfile.write(read_display, indent=4)
    
    @property
    def storelength(self):
        return self.__storelength
        
    @storelength.setter
    def storelength(self, value:int):
        assert isinstance(value, int), f"value {value} must be int type"
        self.__storelength = value
        read_display = cnetconfig.mainfile.read()
        read_display['display']['storelength'] = value
        cnetconfig.mainfile.write(read_display, indent=4)
        
    def change(self, store:bool=None, storelength:int=None):
        '''change default values'''
        if store is not None:
            self.store = store
        if store is not None:
            self.storelength = storelength
    
    def memories(self, dtformat:str=None):
        # :param :dtformat: date time string of view
        if globals().get('pd') is None:
            global pd
            import pandas as pd
        
        file = cnetconfig.getfile('display-storage.json')
        try:
            red = file.read()
        except JSONDecodeError:
            file.clear()
            red = file.read()


        keys = red.keys()
        if dtformat is not None:
            for k in keys:
                red[k]['time'] = datetime.datetime.fromtimestamp(int(red[k]['time'])).strftime(dtformat)

        pdf = pd.DataFrame(red.values(), index=keys)
        return pdf

# display as alternative to print and IPython.display.display
display = __displaycls()
        

def mkdirz(directory, lis:[['folder', 'file']], osfilesplit=True):
		
	for f in lis:
		if osfilesplit is True:
			f = f[:-1]
		path = directory
		for d in f:
			path = os.path.join(path, d)
			os.mkdir(path)
