'''decorators: to decorate the class or function'''


# import package modules
from . import codio
from .filemanager import FileManager as fm

# import libraries
import time, datetime
from functools import wraps

# import decorators from other modules
# setattr method to set attrs
from cnet.codio import setattrs


# runtime decorator
def timed(function):
    
    @wraps(function)
    def wrapper(*args, **kwargs):
        
        # runtime count
	    before = time.time()
	    
	    # run main function
	    value = function(*args, **kwargs)
	    after = time.time()
	    
	    print(f"{function.__name__} runs: {after-before} seconds")
	    return value
    
    return wrapper


# log decorator
def logged(function):  # beta version
    fileObj = fm('file.log')
    
    @wraps(function)
    def wrapper(*args, **kwargs):
        
        # run time count
        before = time.time()
        
        # eun main function
        value = function(*args, **kwargs)
        after = time.time()
        
        # get file details for log
        dtype = codio.typesof(function)
        dtype = dtype[0] if len(dtype) else type(function)
        name = codio.cfpname(function)
        
        content = f"{datetime.datetime.now()} :: {after-before} || <{dtype}> {name} :returns ;{value}\n"
        
        # append log
        fileObj.append(content)
        return value
    
    return wrapper

