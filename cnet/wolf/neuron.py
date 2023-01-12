import numpy as np
import inspect
import imp
import os
import site
import dill
import importlib as implib
from warnings import filterwarnings
import json
import pandas as pd

project_work_flow_folder = "" # "ProjectWorkFlow"

class NeuronsWarning(Warning):
	def __init__(self, message):
		self.message = message
	def __str__(self):
		return repr(self.message)

	
def __related_files_one_generation(file_name: str):
	site_path = os.path.split(site.getsitepackages()[0])[0]
	mod = implib.import_module(file_name)
	get = []
	for i in inspect.getmembers(mod, inspect.ismodule):
		get.append(i)
	for i in inspect.getmembers(mod, inspect.isclass):
		get.append(i)
	for i in inspect.getmembers(mod, inspect.isfunction):
		get.append(i)

	connected = []
	cname_temp = []
	for i, j in get:
		try:	
			j.__file__
			source= dill.source.getimport(j)
			if i != j.__name__:
				source = source[:-1]
		except:
			source= dill.source.getimport(j)
			if not source.startswith(f"from {file_name}."):
				if i != j.__name__:
					source = source[:-1]
		
		if not source.startswith(f"from {file_name}."):
			model = source.strip('\n ').split(" ")[1]
			# .split(".")[0]
			try:
				f, path, desc = imp.find_module(model)
				condition = desc[2] != imp.C_BUILTIN
			except:
				try:
					condition = True
					path = dill.source.getfile(j)
				except TypeError:
					condition = False
			if path is None:
				continue
				
				
			fi = os.path.splitext(os.path.split(str(path))[-1])[0]
			
			if model != fi:
				model = model + '.' + fi
			
			
			if condition:
				if not path.startswith(site_path) and model not in cname_temp:
					connected.append((model, path))
					cname_temp.append(model)

	return connected


def files_relation_importion(file_name: ['str', '__main__', 'global()'], connected_files= True, importlib= True):
	site_path = os.path.split(site.getsitepackages()[0])[0]
	if not isinstance(file_name, str):
		globals_ = file_name
		file_name= os.path.splitext(os.path.split(globals_["__file__"])[-1])[0]
		all = [(k, v) for k,v in globals_.items() if inspect.isfunction(v) or inspect.isclass(v) or inspect.ismodule(v)][1:]
	else:
		mod = implib.import_module(file_name)
		all = []
		for i in inspect.getmembers(mod, inspect.ismodule):
			all.append(i)
		for i in inspect.getmembers(mod, inspect.isclass):
			all.append(i)
		for i in inspect.getmembers(mod, inspect.isfunction):
			all.append(i)

	packages = []
	modules = []
	connected = []
	cname_temp = []
	for i, j in all:
		try:	
			j.__file__
			source= dill.source.getimport(j)
			if not source.startswith(f"from {file_name}."): # line no need
				if "__main__" == source.strip('\n ').split(" ")[1].split(".")[0]:
					continue
				if i != j.__name__:
					source = source[:-1] + f" as {i}"
			packages.append(source.strip("\n "))
		except:
			source= dill.source.getimport(j)
			
			if not source.startswith(f"from {file_name}."):
				if "__main__" == source.strip('\n ').split(" ")[1].split(".")[0]:
					continue

				if i != j.__name__:
					source = source[:-1] + f" as {i}"
				modules.append(source.strip("\n "))
				
		if not source.startswith(f"from {file_name}."):
			model= source.strip('\n').split(" ")[1]
			#model = model.replace(".", divider)
			#model = model.split(".")[0]

			if model == "__main__":
				continue
			try:
				f, path, desc = imp.find_module(model)
				condition = desc[2] != imp.C_BUILTIN
			except:
				condition = True
				path = dill.source.getfile(j)
				
			if path is None:
				continue
				
			fi = os.path.splitext(os.path.split(str(path))[-1])[0]
			
			if model != fi:
				model = model + '.' + fi
			
			if condition:
				
				if not path.startswith(site_path) and model not in cname_temp:
					connected.append((model, path))
					cname_temp.append(model)
					start = __related_files_one_generation(model)
					if start:
						pending = [x[0] for x in start]
					else:
						pending= False
					while pending:
						checking = __related_files_one_generation(pending[0])
						if checking:
							for y in checking:
								if y[0] not in pending:
									pending.append(y[0])
								if y[0] not in cname_temp:
									cname_temp.append(y[0])
									connected.append((y[0], y[1]))
						elif pending[0] not in cname_temp:
							try:
								f, path, desc = imp.find_module(model)
								cname_temp.append(pending[0])
								connected.append((pending[0], path))
							except:
								pass
						pending.remove(pending[0])
						
	packages= "# Site Packages:\n" + "\n".join(packages)
	modules= "\n\n# Built-in & Modules:\n" + "\n".join(modules)

	result = []
	if connected_files:
		result = connected
	if importlib:
		result.append(packages + modules)
	
	return result


def get_importlib(file_name):
	return files_relation_importion(file_name, connected_files=False, importlib=True)[0]


def get_connected_files(file_name):
	return files_relation_importion(file_name, connected_files=True, importlib=False)


def get_class_family(ins, cwd_globals_= None):
	"""    global_ is used to avoid double execution of the current file
	usage: useful while taking the current file class as a instances
	"""
	file = inspect.getfile(ins)
	file_name = os.path.splitext(os.path.split(file)[-1])[0] if cwd_globals_ is None else cwd_globals_
		
	must = get_connected_files(file_name)
	must_in_list = [l[1] for l in must]
	must_in_list.append(file)
	shortlist_class = []
	places = []
	for i in inspect.getmro(ins)[:-1]:
		get = inspect.getfile(i)
		if get in must_in_list:
			if get not in places:
				places.append(get)
			shortlist_class.append([i, get])
			
	return shortlist_class, places


class Extract():
    def __init__(self):
    	pass
		
    def __getting(self, dtype):
    	neu= self.neurons
    	ret = []
    	for n in np.where(neu[:,2]== dtype):
    		ret.append(neu[n])
    	
    	return ret[0]

    @property
    def get_classes(self):
    	new_list= []
    	for c in self.__getting('class'):
    		new = []
    		for mem in c[4]():
    			if inspect.isfunction(mem[1]):
    				new.append(mem)
    		insert = [c[0], c[1], c[2], c[3], new, c[5]]
    		new_list.append(insert)
    			
    	return np.array(new_list)
    	
    @property
    def get_functions(self):
    	new_list= []
    	for c in self.__getting('function'):
    		insert = [c[0], c[1], c[2], c[3], [], c[5]]
    		new_list.append(insert)
    			
    	return np.array(new_list)
    
    
    def show(self, name, methods= True, variables= True, doc= False, source= False, family= False, deep= False, counts= True):
    	layer = 1
    	get_index= np.where(self.neurons[:, layer]== name)
    	ret = ''
    	result= ["temp", "name", 'type', "original_namd"]
    	if not len(get_index[0]):
    		layer = 3
    		get_index= np.where(self.neurons[:, layer]== name)
    	if not len(get_index[0]):
    		ret = None
    	else:
    		result = self.neurons[get_index][0]

    	if ret is not None:
    		ret = f"{result[1]}: '{result[2]}' | {result[3]}"
	    	new_ret= ''
	    	if methods:
	    		new_ret = '\n\nmethods:'
	    		count = 0
	    		lc = [i[0] for i in result[-2]() if inspect.isfunction(i[1]) or inspect.isdatadescriptor(i[1])]
	    		method_deep_remove = ["__weakref__"]
	    		if not deep:
	    			for mdr in method_deep_remove:
	    				if mdr in lc:
	    					lc.remove(mdr)
	    		if lc:
		    		len_cal = len(max(lc, key= len))
		    		
		    		here = result[-2]()
		    		new_here = []
		    		for no, h in enumerate(here):
		    			if h[0] in ["__init__", "__call__"]:
		    				new_here.append(h)
		    				del here[no]

		    		new_here.sort(reverse=True)
		    		get_here = new_here + here

			    	for i in get_here:
			    		if inspect.isfunction(i[1]) or inspect.isdatadescriptor(i[1]):
			    			if not deep and i[0] in method_deep_remove:
			    				continue
			    				
			    			count += 1
			    			mem= ""
			    			if not inspect.isdatadescriptor(i[1]):
				    			mem= inspect.signature(i[1])
				    		new_ret_new = f"\n  --> {i[0]}".ljust(len_cal+7, " ")
			    			new_ret += new_ret_new + f' : {mem}'
	    		if not count:
			    	new_ret = new_ret[:11] + f" <{count} /{len(result[-2]())}>" + new_ret[11:] + "\n  None"
	    		else:
			    	new_ret = new_ret[:10] + f" <{count} /{len(result[-2]())}>" + new_ret[10:] + "\n"
	    		ret = ret + new_ret

	    	if variables:
	    		new_ret = "\n\nvariables:"
	    		count = 0
	    		dictionary = result[0].__dict__
	    		olc = list(dictionary.keys())
	    		lc = olc.copy()
	    		variables_deep_remove = ["__module__", "__dict__", "__weakref__", "__doc__"]
	    		if not deep:
	    			for mdr in variables_deep_remove:
	    				if mdr in lc:
	    					lc.remove(mdr)
	    		if lc:
		    		len_cal = len(max(lc, key= len))
		    		for var in dictionary.items():
		    			if not deep and var[0] in variables_deep_remove:
		    				continue
		    			count += 1
		    			new_ret_new = f"\n  {var[0]}".ljust(len_cal + 3, " ")
		    			
		    			new_ret += new_ret_new + f" : {var[1]}"
		    		ret += new_ret[:12] + f" <{count} /{len(olc)}>" + new_ret[12:] + "\n"
		    	else:
		    		ret += new_ret[:12] + f" <{count} /{len(olc)}>" + new_ret[12:] + "\n  None"
		    
	    	if family:
	    		new_ret = "\n\nFamily:"
	    		count = 0
	    		add_count = ""
	    		if result[2] == "class":
	    			cwd_globals = self.cwd_globals if inspect.getfile(result[0]) == self.cwd_globals['__file__'] else None
	    			try:
	    				dictionary = get_class_family(result[0], cwd_globals)[0]
	    				lc = [s[0].__name__ for s in dictionary]
	    			except ModuleNotFoundError: # No idea, its not showing all classes or not
	    				lc = 0
	    				print(f"Model '{result[0]}' not found.")
	    			except:
	    				lc = 0

	    			
		    		if lc:
			    		len_cal = len(max(lc, key= len))
			    		for var in dictionary:
			    			new_ret_new = f"\n  {var[0].__name__}".ljust(len_cal + 3, " ")
			    			
			    			new_ret += new_ret_new + f" : {var[1]}"
			    			count += 1
			    		if counts:
			    			add_count = f" <{count} /{len(inspect.getmro(result[0]))- 1}"
			    		ret += new_ret[:9] + add_count + new_ret[9:]
			    	else:
			    		if counts:
			    			add_count = f" <{count} /{len(inspect.getmro(result[0]))- 1}"
			    		ret += new_ret[:9] + add_count + "\n  None" + new_ret[9:]
	    		else:
	    			if counts:
	    				add_count = " <0 /0>"
			    	ret += new_ret + f"{add_count}\n  Function has no family."
			    
			
	    	if doc:
	    		new_ret = "\n\nDoc String: "
	    		query= result[0].__doc__
	    		
	    		if query is not None:
	    			
	    			
	    			new_ret += "-" * (len(max(query.splitlines(), key= len))- len(new_ret) + 2)
	    			new_ret += "\n" + query
	    			ret += new_ret
	    		else:
	    			ret += new_ret+ "\n  None"

	    	if source:
	    		new_ret = "\n\nSource: "
	    		query = None
	    		if deep and result[2] == 'class':
	    			try:
	    				classes = reversed(get_class_family(result[0])[0])
	    				query = ""
		    			for cins, d in classes:
		    				query += dill.source.getsource(cins) + "\n"
	    			except ModuleNotFoundError:
	    				pass
	    				
	    		else:
	    			query = result[-1]()
	    			
	    		
	    		if query is not None:
	    			
	    			
	    			new_ret += "-" * (len(max(query.splitlines(), key= len))- len(new_ret) + 2)
	    			new_ret += "\n" + query
	    			ret += new_ret
	    		else:
	    			ret += new_ret+ "\n  None"
    	ret = ret.splitlines(True)
    	ret.insert(1, "parameters: " + str(inspect.signature(result[0])) + "\n")
    	ret = "".join(ret)
    	return ret
    	
    def show_classes(self, real_name= False, root= False, root_num= False, call= False, head_count= False):
    	return self.__show_cls_func(dtype="class", real_name=real_name,head_count=head_count, call=call, root=root, root_num=root_num)
    	
    def show_functions(self, real_name= False, head_count= False, call= False):
    	return self.__show_cls_func(dtype="function", real_name=real_name,head_count=head_count, call=call)
    	
    def __show_cls_func(self, dtype, real_name= False, root= False, root_num= False, head_count= True, call= False):
    	get_func= self.__getting(dtype)
    	ret= "functions:" if dtype == "function" else "classes:"
    	spacer = "  --> "
    	subspacer = "        + "
    	call_fill = "  :"
    	cfill = ' | '
    	length= len(get_func)
    	sss_len= len((spacer + subspacer))
    	if length and head_count: # do
    		ret += f' <{length}>'
    	top_length = 0
    	try:
    		if get_func[:, 1]:
    			top_length= len(max(get_func[:, 1],key=len))
    	except:
    		pass
    	if real_name:
    		
    		if call:
    			signa = [str(inspect.signature(sig)) for sig in get_func[:, 0]]
    			len_call = len(max(signa, key= len)) + len(call_fill)
    		
    		mem_atr = True
    		if not root:
    			mem_atr = False
    		for e, i in enumerate(get_func):
    			ret += f"\n{spacer}"
    			ret1 = f'{i[1]}'.ljust(top_length, " ")
    			if dtype== 'function' and call:
    				spac1 = " "
    				ret1 += f'{call_fill}{signa[e]}{spac1}'
    				ret1 = ret1.ljust(top_length + len_call + len(spac1), ' ')
    			
    			ret1 += cfill+ f'{i[3]}'

    			ret += ret1.ljust(len(max(get_func[:, 3],key=len)) + top_length + len(cfill)+ 1, " ")
    			
    			
    			if dtype== 'class' and mem_atr:
    				
    				total = 0
    				new_ret = ""
    				lis = [mem[0] for mem in i[-2]() if inspect.isfunction(mem[1]) or inspect.isdatadescriptor(mem[1])]
    				if len(lis):
	    				mem_len= len(max(lis, key= len))
	    				
	    				for mem in i[-2]():
		    				is_datadesc = inspect.isdatadescriptor(mem[1])
			    			if inspect.isfunction(mem[1]) or is_datadesc:
			    				total+= 1
			    				new_ret += f"\n{subspacer}"
			    				new = f'{mem[0]}' 
			    				new_ret += new.ljust(mem_len, " ")
			    					
			    				try:
					    			if call:
					    				new_ret += f'{call_fill}{inspect.signature(mem[1])}'
					    		except:
					    			new_ret += f'{call_fill}'
    				
    				if root_num:
    					new_ret = new_ret.ljust(sss_len, " ")
    					ret += f'<{total} /{len(i[4]())}>'
    				ret += new_ret
    			
    	else:
    		
    		if call:
    			signa = [str(inspect.signature(sig)) for sig in get_func[:, 0]]
    			len_call = len(max(signa, key= len)) + len(call_fill) # if add after
    		
    			
    		for e, i in enumerate(get_func):
    			ret += f"\n{spacer}"
    			ret += f'{i[1]}'.ljust(top_length, " ")
    			if dtype== 'function' and call:
    				spac1 = " "
    				ret += f'{call_fill}{signa[e]}{spac1}'
    				ret = ret.ljust(top_length + len_call + len(spac1), ' ')
    				
    			mem_atr = True
    			if not root:
    				mem_atr = False
    				
    			if dtype== 'class' and mem_atr:
    				total = 0
    				new_ret = ""
    				lis = [mem[0] for mem in i[4]() if inspect.isfunction(mem[1])]
    				if len(lis):
	    				for mem in i[4]():
		    				mem_len= len(max(lis, key= len))
		    			
			    			if inspect.isfunction(mem[1]):
			    				total+= 1
			    				new_ret += f"\n{subspacer}"
			    				new = f'{mem[0]}' 
			    				new_ret += new.ljust(mem_len, " ")
			    					
			    				try:
					    			if call:
					    				new_ret += f'{call_fill}{inspect.signature(mem[1])}'
					    		except:
					    			pass
			    			
    				if root_num:
    					ret += f' <{total} /{len(i[4]())}>'
    				ret += new_ret
    			
    	return ret

    def __get_ins_source(self, name: str):
    	ins, source = None, None
    	if "." not in name:
    	    find_id = np.where(self.neurons[:, 1]== name)
    	    assert len(find_id[0]), f"'{name}' is not defined or inserted."
    	    ins = self.neurons[find_id][0][0]
    	    source= dill.source.getsource(ins)
				
    	else:
    	    clean= name.strip("\n ").split('.')
    	    code= [c.strip() for c in clean if c]
		    
    	    find_id = np.where(self.neurons[:, 1]== code[0])
    	    assert len(find_id[0]), f"'{name}' is not defined or inserted."
		    
    	    source = self.neurons[find_id][0][-2]()
    	    for i in source:
    	    	if code[1] == i[0]:
    	    		ins= i[1]
    	    		source = dill.source.getsource(ins)
    	    		break
    	return ins, source

    def getins(self, name: str):
    	ins = self.__get_ins_source(name)[0]
    	return ins

    def getsource(self, name: str):
    	return self.__get_ins_source(name)[1]


class Neurons(Extract):
    '''
        used
    '''
    def __init__(self, globals_)-> None:
        self.neurons = None
        self.model = None
        self.cwd_globals = globals_
    
    def globalize(self, modules=False, append= True):
        if append is not True:
            self.neurons = None

        for name, obj in self.cwd_globals.items():
            if modules is True:
                if inspect.ismodule(obj):
                    continue
            if inspect.isfunction(obj) or inspect.isclass(obj):
                self.add(obj)

    def source(self, val):
    	def call():
    		return val
    	return call
    	
    def add(self, neuron, name=None):
        if inspect.isfunction(neuron):
        	type_= 'function'
        	original_name= neuron.__name__
        	name = original_name if name is None else name
        	members = inspect.getmembers(neuron)
        	
        elif inspect.isclass(neuron):
        	type_= 'class'
        	# original_name= str(neuron).strip("'>").split('.')[-1]
        	original_name = neuron.__name__
        	name= original_name if name is None else name
        	members = inspect.getmembers(neuron)
        else:
        	raise Exception(f"function or classes should be add, not '{neuron}' as type {type(neuron)}")
        	
        source= dill.source.getsource(neuron)
        
        if self.neurons is None:
            self.neurons= np.array([neuron, name, type_, original_name, self.source(members), self.source(source)], ndmin=2)
            
        else:
            if original_name in self.neurons[:, 3]:
            	self.remove(original_name)
            
            self.neurons= np.vstack((self.neurons,[neuron, name, type_, original_name, self.source(members), self.source(source)]))
        
    def remove(self, neuron_name):
        cond1= neuron_name in self.neurons[:, 3]
        cond2= len(self.neurons)
        dim = 0
        if cond1 and cond2:
            del_rowid= np.where(self.neurons[:, 3]== neuron_name)
            self.neurons= np.delete(self.neurons, del_rowid , dim)
            
            if len(self.neurons)==0:
                self.neurons= None
                
        else:
            print(f"nothing found named {neuron_name}")
    
    def get_list(self, complete= False):
        """[neuron instance, name, type, original name, members, source]"""
        neu= self.neurons
        get= len(neu[0])
        if not complete:
        	get -= 2
        return np.array([list(n[:get]) for n in neu])
    
    def saving(self, _loop= False): # ToDo: add saving and restoring options
        self.file_saving = dict()
        
        import_ = get_importlib(self.cwd_globals)
        import_ = import_ + "\n\n" if import_ else import_

        function_ = ""
        for i in self.get_functions:
        	function_ += i[5]() + "\n\n"
        
        class_ = ""
        for i in self.get_classes:
            
            if not _loop: # useful or not: sometime will help.
            	person = self.cwd_globals if inspect.getfile(i[0]) == self.cwd_globals['__file__'] else None
            else:
            	person = self.cwd_globals
            
            family = get_class_family(i[0], person)[0]
            for member in family:
            	condition1 = inspect.getfile(member[0])
            	condition2 = self.cwd_globals['__file__']
            	if condition1 == condition2:
	            	get_source = dill.source.getsource(member[0])
	            	class_ += get_source + "\n\n"
	            
            		
        connected_files = get_connected_files(self.cwd_globals)
        files = dict()
        cwd_f = os.path.join(os.getcwd(), project_work_flow_folder)
        for f in connected_files:
        	# m1 --
        	# ff = f[0].split('.')
        	# if len(ff) >= 2 and ff[0] == project_work_flow_folder:
        	# 	continue
        	
        	# m2 --
        	if f[1][:len(cwd_f)] == cwd_f:
        		continue
        	red = open(f[1]).read()
        	if isinstance(red, bytes):
        		red = red.decode()

        	files[f[0]] = [f[1], red]
        	
        self.file_saving.update({"codes":{"libraries:": import_,
        							"functions:": function_,
        							"classes:": class_},
        					"files": files})
        	
    def save(self, save_path= None):
        import json
        json_obj = json.dumps(file_saving, indent= 4)
        if save_path is None:
            file = self.cwd_globals['__file__']
            file_name = os.path.splitext(os.path.split(file)[-1])[0]
            save_path = os.path.join(os.path.dirname(file), file_name + '.wf')

        	
        with open(save_path, 'w') as file:
        	file.write(json_obj)

    def __add__(self, neuron, name= None):
        self.add(neuron, name)
    
    def __str__(self):
        try:
            s = "".join([f'{n[:2]}\n' for n in self.neurons])
        except:
            s = ''
		
        return s

    def display(self):
        '''"Name", "Type", "Original_Name", "Object"'''
        try:
            # pandas dataframe
            new = self.neurons[:, 0:4].copy()
            new[:, 0:3] = self.neurons[:, 1:4]
            new[:, 3] = self.neurons[:, 0]
            pdf = pd.DataFrame(new, columns=["Name", "Type", "Original_Name", "Objects"])
            # pdf = pd.DataFrame(self.neurons[:,1:4], columns=["Name", "Type", "Original_Name"])
        except:
            pdf = []
            pdf = pd.DataFrame([], columns=["Name", "Type", "Original_Name"])
		
        return pdf
