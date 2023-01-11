"""
CodeFlow.py :: shows the running code flow in order
status: completed

"""


# import libraries
import pandas as pd
from IPython.display import display


class CodeFlow:
    '''
    -------------------------------------
    
    Example:
    --------
    from wolf import CodeFlow, display

    # initialize
    cf = CodeFLow(globals())

    # access variables
    get = cf()[0]

    # show table and columns in beautify
    display(cf())
    -------------------------------------

    Note:
    -----
    - don't use cf() alone in line, use with print, display, (call with variable)
       - print(cf())
       - display(cf())
       - code_flow = cf()

    '''
    
    def __init__(self, globals_, take= [], neglect= []):
        self.globals_= globals_
        self.take = take
        self.neglect = neglect
        
        self.additional_backlogs_contents = ['In', 'Out', 'get_ipython', 'exit', 'quit', '__name__', '__file__', '__builtins__', '__warningregistry__']
        
        # set pandas display : IPython.display.display
        self.display = pd.options.display
        
        # set pandas default display values
        self.display.max_rows = 30
        self.display.max_columns = 4

    def __call__(self, take= None, neglete= None, r= True, sp=False, vo= True, abl=False):
        """
        r  : reverse
        sp : show_private
        vo : variables_only
        abl: aditional_backlogs
        
        """
        # assign codes to real names
        reverse = r
        show_private = sp
        variables_only = vo
        additional_backlogs = abl
        
        new_arr = []
        
        taking = take if take is not None else self.take
        neglete = neglete if neglete is not None else self.neglect
        
        for i in list(self.globals_.items()):
            # get name, value
            name = i[0]
            value = i[1]
            
            # show private objects
            if not show_private:
                if name.startswith("_"):
                    continue
            
            # get type
            type_ = type(value).__name__
            if type_ == "type":
                type_ = 'class'
            if type_ not in taking and taking:
                continue
            if type_ in neglete and neglete:
                continue
            
            # show variables only
            if variables_only:
                if type_ in ["class", "function", 'module']:
                    continue
            
            # remove additional backlogs
            if additional_backlogs is False:
                if name in self.additional_backlogs_contents:
                    continue
                        
            # get length
            try:
                shape = len(value)
                if type_ in ["ndarray", "DataFrame"]:
                    shape = value.shape
                if type_ in ['list', 'str']:
                    type_shape = type_
                    if type_ == "str":
                        type_shape = "chars"
                    shape = f"{shape} {type_shape}"
            except:
                shape = ''
            
            # add to the list
            new_arr.append([name, type_, shape, value])

        # variables priority order: list reverse
        if reverse:
            new_arr.reverse()
        
        # create dataframe
        df = pd.DataFrame(new_arr, columns= ["Name", "Type", "Shape", "Value"])
        df[:2] = df[:2].astype('string')
        return df
