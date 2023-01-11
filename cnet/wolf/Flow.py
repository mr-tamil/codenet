import numpy as np
from . import codio
import inspect

class Flow():
    def __init__(self, neuron):        
        self.Neurons = neuron
        self.methods_to_add = ['getsource', 'getins', 'get_classes', 'get_functions', 'show', 'show_functions', 'show_classes', 'get_list', "add", "__add__", "remove"]
        for n, m in inspect.getmembers(self.Neurons):
        	if n in self.methods_to_add:
        		self.__dict__[n] = m

        # set default values
        self.show_logs = False
    
    @staticmethod
    def func_call(func):
        def inner_model(*args):
            return func(*args)
        return inner_model
        
    def __call__(self, code):
    	clean= code.strip("\n ").split('>')
    	getnames = [c.strip() for c in clean if c not in ['', ' ']]
    	
    	self.result = []
    	for name in getnames:
    		layer = 1
    		get_index= np.where(self.Neurons.neurons[:, layer]== name)
	    	if not len(get_index[0]):
	    		layer = 3
	    		get_index= np.where(self.Neurons.neurons[:, layer]== name)
	    	if len(get_index[0]):
	    		self.result.append(self.Neurons.neurons[get_index][0])
	    	else:
	    		raise Exception(f"There is no such a function or class called '{name}'")
    	
    	return self.result

    def fit(self):
        self.model = []
        self.names_alone =[]
        for neuron in self.result:
        	if neuron[2] == 'class':
        		if neuron[1] in self.names_alone:
        			for i in self.model:
        				if i[0] == neuron[1]:
        					self.model.append((neuron[1], i[1]))
        					break
        		else:
        			self.model.append((neuron[1], neuron[0]()))
        			self.names_alone.append(neuron[1])
        	else:
        		self.model.append((neuron[1], self.func_call(neuron[0])))
        return self.__exec
    
    def __exec(self, values):
        with codio.PrintStatement(self.show_logs):
            for i, name_neuron in enumerate(self.model):
                try:
                    values = name_neuron[1](values)
                except:
                    raise Exception(f"Failed to execute the {name_neuron[0]} in location {i}: {name_neuron}")
  
        return values
