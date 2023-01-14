'''decorators: to decorate the class or function'''


# import package modules
from . import codio
from .filemanager import FileManager as fm

# import libraries
import time, datetime
from functools import wraps
import inspect


# ---------------------------------------

# selfit: function helper class
class _SELFIT_DEFAULT:
    '''set default for selfit decorator function'''

# selfit: function helper function
def _selfit_helper(func, adjust, args, kwargs, default_value=_SELFIT_DEFAULT, self=True):

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
        if s1 == -1 and s2 == -1: 'no one, no two'
        if s1 == s2 and s1 != -1 and s2 != -1: 'two'
        if s1 != s2 and s1 != -1 and s2 != -1: 'one and two'
        '''
        
        obj = args[0]

        # kwargs empty
        kk = kwargs.keys()

        note_error = []
        for i, k in enumerate(ak[1:]):
            if k not in kk:
                if adjust is False:
                    kwargs[k] = av[i+1].default

                elif self is True:
                    if k not in obj.__dict__.keys():
                        if default_value is not _SELFIT_DEFAULT:
                            kwargs[k] = default_value
                        else:
                            note_error.append(k)
                    else:
                        kwargs[k] = obj.__dict__[k]

                elif self is False:
                    if default_value is not _SELFIT_DEFAULT:
                        kwargs[k] = default_value
                    else:
                        note_error.append(k)

        if note_error:
            sent = ", ".join(note_error)
            raise Exception(f"{func.__name__} missing {len(note_error)} required positional arguments: {sent}")

        if len(args)>1 and not one:
            args = list(args)
            for i, a in enumerate(args[1:]):
                kwargs[ak[i+1]] = a
                del args[1]
                
            args = tuple(args)
        
        if obj:
            for k, v in kwargs.items():
                setattr(obj, k, v)
                
    output = func(*args, **kwargs)
    return output


# selfit: function helper function
def _selfit_adjust(self= True, default=_SELFIT_DEFAULT):
    def function(func):
        @wraps(func)
        def call(*args, **kwargs):
            output = _selfit_helper(func=func,
                                      default_value= default,
                                      self= self,
                                      adjust=True,
                                      args=args,
                                      kwargs=kwargs)
            return output
        return call
    return function


# selfit for instantiate self in class methods
def selfit(func):
    @wraps(func)
    def call(*args, **kwargs):
        output = _selfit_helper(func=func,
                                  adjust=False,
                                  args=args,
                                  kwargs=kwargs)
        return output

    return call

# instantiate adjust method
selfit.adjust = _selfit_adjust

# ---------------------------------------
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

