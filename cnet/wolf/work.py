import inspect
import os
import importlib as implib
import json
import sys,io,imp,types
import shutil
from . import neurons

class Objects(): pass


class WorkModule():
	works = []
	def __init__(self, name, neuron= None):
		self.methods_to_add = ['getsource', 'getins', 'get_classes', 'get_functions', 'show', 'show_functions', 'show_classes', 'get_list']
		if neuron is None:
			self.pname = name
			self.project_path = name

		else:
			self.module_path = None
			self.Neuron = neuron
			self.project_path = None
			self.__name__ = name
			self.works.append(self)
			
			for n, m in inspect.getmembers(self.Neuron):
				if n in self.methods_to_add:
					self.__dict__[n] = m
			
			
	def __call__(self, work, delete= True):
		# main file
		self.__name__ = work
		with open(self.pname) as file_read:
			self.read = json.load(file_read)
		
		work_path = os.getcwd()
		# restore files
		add_del_path = []
		for name, path_source in self.read['works'][work]['files'].items():
			path = work_path
			f = name.split('.')
			for d in f[:-1]:
				path = os.path.join(path, d)
			path = os.path.join(path, f[-1]) + '.py'
			add_del_path.append(path)
			with open(path, 'w') as file:
				file.write(path_source[1])

		# saving main file
		r = self.read['works'][work]['codes']
		module_path = os.path.join(work_path, work) + ".py"
		self.module_path = module_path
		fs = ""
		for div, stri in r.items():
			fs += f"# {div}\n{stri}"
		with open(module_path, 'w') as file:
			done = False
			count = 0
			variable = "pwfgetglobals"
			while not done:
				finalvar = f"{variable}{count}"
				if finalvar not in fs:
					fs += f"\n{finalvar} = globals()"
					file.write(fs)
					done = True
				else:
					count += 1
		
			
		add_del_path.append(module_path)
		with io.open(module_path) as scriptfile:
		    code = compile(scriptfile.read(),module_path,'exec')

		self.module = imp.new_module('__main__')
		exec(code,self.module.__dict__)
		
		if delete:
			# del cashe files:
			for pa in add_del_path:
				os.remove(pa)
				del_dir = os.path.split(pa)[0]
				del_dir_in = os.listdir(del_dir)
				ddil = len(del_dir_in)
				if del_dir != work_path and ddil in [0, 1]:
					if ddil == 1:
						if del_dir_in[0] == '__pycache__' and os.path.isdir(os.path.join(del_dir, del_dir_in[0])):
							shutil.rmtree(del_dir)
					else:
						shutil.rmtree(del_dir)
		
		
		getmembers = inspect.getmembers(self.module)
		globals_ = [i[1] for i in getmembers if i[0] == finalvar][0]
		
		
		globals_['__file__'] = module_path
		neu = self.read['works'][work]['neurons']
		
		neurons_ = neurons(globals_)
		for n in neu:
			neurons_.add(globals_[n[1]], n[0])
		
		self.Neuron = neurons_
		self.works.append(self)
		
		
		for n, m in inspect.getmembers(self.Neuron):
			if n in self.methods_to_add:
				self.__dict__[n] = m
		return self
		
		
	
	def objects(self):
		self.inside_class = Objects()
		for neuron in self.Neuron.neurons:
			self.inside_class.__dict__[neuron[1]] = neuron[0]
		
		return self.inside_class
		
	def remove(self, name):
		try:
			del self.inside_class.__dict__[name]
		except:
			pass
		finally:
			self.Neuron.remove(name)
			
	def __add__(self, neuron, name= None):
		self.add(neuron, name)
		
	def add(self, neuron, name= None):
		if name is None:
			name = neuron.__name__
		try:
			self.inside_class.__dict__[name] = neuron
		except:
			pass
		finally:
			self.Neuron.add(neuron, name)
		

	def save(self, save_path= None):
	    if self.project_path is not None and save_path is None:
	    	save_path = self.project_path

	    self.Neuron.saving(_loop= True)
	    self.project_path = save_path if save_path is not None else self.project_path

	    work_file_saving = self.Neuron.file_saving.copy()
	    
	    work_dict = {}
	    work_dict['neurons'] = [(name[1], name[3]) for name in self.Neuron.neurons]
	    
	    work_dict["codes"] = work_file_saving['codes']
	    work_dict["files"] = work_file_saving["files"]
	    
	    if save_path is None:
	    	file = self.Neuron.cwd_globals['__file__']
	    	file_name = os.path.splitext(os.path.split(file)[-1])[0]
	    	save_path = os.path.join(os.path.dirname(file), file_name + '.pwf')
	    	
	    if os.path.exists(save_path):
	        try:
	        	with open(save_path, 'r') as rfile:
	        		read = json.load(rfile)
	        		with open(save_path, 'w') as wfile:
	        			read["works"][self.__name__] = work_dict
	        			json_obj = json.dumps(read, indent= 4)
	        			wfile.write(json_obj)
	        except:
	        	raise Exception("Project file is already there and is not supported. Just remove it or save project as new name.")
	    else:
	        with open(save_path, 'w') as file:
	        	json_obj = json.dumps({"works": {self.__name__: work_dict}}, indent= 4)
	        	file.write(json_obj)
	
	@classmethod
	def save_all(cls, save_path= None):
		if save_path is None:
		    file = cls.works[0].Neuron.cwd_globals['__file__']
		    file_name = os.path.splitext(os.path.split(file)[-1])[0]
		    save_path = os.path.join(os.path.dirname(file), file_name + '.pwf')
		
		workings = {"works": {}}
		for w in cls.works:
		    w.Neuron.saving(_loop= True)
		    work_file_saving = w.Neuron.file_saving.copy()
		    work_dict = {}
		    work_dict['neurons'] = [(name[1], name[3]) for name in w.Neuron.neurons]
		    work_dict["codes"] = work_file_saving['codes']
		    work_dict["files"] = work_file_saving["files"]
		    workings["works"][w.__name__] = work_dict

		    if os.path.exists(save_path):
		        try:
		        	with open(save_path, 'r') as rfile:
		        		read = json.load(rfile)
		        		with open(save_path, 'w') as wfile:
		        			read["works"].update(workings["works"])
		        			json_obj = json.dumps(read, indent= 4)
		        			wfile.write(json_obj)
		        except:
		        	raise Exception("Project file is already there and is not supported. Just remove it or save as new name.")
		    else:
			    with open(save_path, 'w') as file:
			    	json_obj = json.dumps(workings, indent= 4)
			    	file.write(json_obj)
			    	
	def ediload(self, path= None):
		""" Edit by download and save as usual by Works class"""
		pass
		
	
class SavedWorks:
	def __init__(self, name):
		self.name = name
	
	def __call__(self, work, delete= True):
		wm = WorkModule(self.name)
		w = wm(work, delete=delete)
		
		return w

def Works(name, neuron= None):
	protype = 'work' if neuron is not None else 'project'
	output_class = None
	if protype == "project":
		output = SavedWorks(name)
	else:
		output = WorkModule(name, neuron)
		
	return output
