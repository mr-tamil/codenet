'''filemanager :: File Manager : as fm'''

# import package modules
from . import codio

# import libraries
import os, shutil, json

class Dencrypt():
	"""
	Encrypt and Decrypt the file with key,
	key: 44 char and ends with =
	key: not 44  char and not ends with =
	"""
		
	def __init__(self, filepath: str):
		assert isinstance(filepath, str), f"file path '{filepath}' must be str."
		self.filepath= filepath
		self.__key= None
		
		# install required library
		try:
			codio.install_package('cryptography')
		except:
			raise Exception("install cryptography using pip")
		from cryptography.fernet import Fernet
		self.Fernet = Fernet


	def encrypt(self, key: str= None, keyfilepath: str= None, savekeyfile:str= None):
		assert key== None or isinstance(key, str), f"key '{key}' must be NoneType of str."
		assert keyfilepath== None or isinstance(keyfilepath, str), f"key file '{keyfilepath}' must be NoneType of str."
		
		error= None
		status= True
		
		if not key and keyfilepath is None:
			key = self.Fernet.generate_key().decode()
		
		if key is None:
			with open(keyfilepath, 'r') as kf:
				key = kf.read()
        
		if len(key)<44:
			if '=' not in key:
				key = key.zfill(43) + '='
			else:
				raise Exception("Invalide key format")

		if savekeyfile:
			with open(savekeyfile, 'w') as source:
				source.write(key)
		
		try:
			f = self.Fernet(key.encode())
			with open(self.filepath,'rb') as source:
				file = source.read()
			
			encryption = f.encrypt(file)
			with open(self.filepath,'wb') as source:
				source.write(encryption)
				
		except Exception as e:
			status= False
			error= e
			
		self.__key= key
		return {
				'type': 'encrypt',
				'status': status,
				'key': key,
				'filename': self.filepath,
				'savekeyfile': savekeyfile,
				'keyfilename': keyfilepath,
				'error': error
				}
	
	def decrypt(self, key:str= None, keyfilepath:str= None):
		assert key== None or isinstance(key, str), f"key '{key}' must be NoneType of str."
		assert keyfilepath== None or isinstance(keyfilepath, str), f"key file '{keyfilepath}' must be NoneType of str."
		assert (key or keyfilepath) and not (key and keyfilepath), f"key or key_file any one must be given."
		
		error= None
		status= True
		
		try:
			if keyfilepath:
				with open('key.txt', 'r') as file:
					key= file.read()
			if len(key)<44:
				if '=' not in key:
					key = key.zfill(43) + '='
				else:
					raise Exception("Invalide key format")
			f = self.Fernet(key)
			with open(self.filepath, 'rb') as source:
			    file = source.read()
			
			Decryption = f.decrypt(file)
			
			with open(self.filepath, 'wb') as source:
			    source.write(Decryption)
		
		except Exception as e:
			error= e
			status= False
		
		
		return {
				'type': 'decrypt',
				'status': status,
				'key': key,
				'filename': self.filepath,
				'keyfilename': keyfilepath,
				'error': error
				}
	
	@property
	def key(self):
		pass
	
	@key.getter
	def key(self):
		key= self.__key
		self.__key= None
		return key



# File Manager Format
class Fmf:
    '''
    Fmf: File Manager Format
    '''
    
    __modes = ['t', 'b']
    
    def __init__(self, filepath: str, mode:str= 't')->None:
        # Parameter ValueError Check
        assert isinstance(filepath, str), f"file path {filepath} must be str"
        assert mode in self.__modes, f"mode must be one of {self.__modes}"
        
        #: param: filepath: str: file path or location
        #: param: mode: str: file mode -text or binary
        
        self.filepath = filepath
        self.mode = mode
        
        # set default content
        self.default_content = ''
        '''
        --This layer of objects should change--
        
        self.default_content = 
        self.read(self)
        self.write(self)
        self.append(self)
        self.create(self)
        '''
    	
    	
    # ------------------------------------------
    
    # class tools
    def modop(self, op):
    	'''combine mode and operation of the open function'''
    	return f"{op}{self.mode}"
    	
    
    
    # ------------------------------------------
    # --- This layer should change -------------
    # manage and access file content
    def read(self, n:int=-1):
        '''read content from the file'''
        file = open(self.filepath, self.modop('r'))
        red = file.read(n)
        file.close()
        return red
        
    def write(self, content):
        '''write content to the file: even overwrite'''
        file = open(self.filepath, self.modop('w'))
        file.write(content)
        file.close()
        
    def append(self, content):
        '''append content to the file'''
        file = open(self.filepath, self.modop('a'))
        file.write(content)
        file.close()
        
    def create(self, content):
        '''create file and write content to the file: if file not exists'''
        file = open(self.filepath, self.modop('a'))
        file.write(content)
        file.close()
        
        
        
    # ------------------------------------------

    # manage file content shortcuts
    def clear(self):
        '''clear file content'''
        file = open(self.filepath, self.modop('w'))
        
        # set default content to the file
        file.write(self.default_content)
        file.close()
        
        
        
    # ------------------------------------------

    # manage file on system
    def move(self, path:str):
        '''move file to destination path'''
        shutil.move(self.filepath, path)
        self.filepath = path
    
    def copy(self, path:str):
        '''copy the file to destination path'''
        shutil.copy(self.filepath, path)
        
    def copyAndWork(self, path:str):
        '''copy the file to destination path and continue the copied file'''
        shutil.copy(self.filepath, path)
        self.filepath = path
        
    def delete(self):
        '''delete the file'''
        os.remove(self.filepath)
    
    def encrypt(self, key: str= None, keyfilepath: str= None, savekeyfile:str= None):
        '''encrypt the file'''
        file = Dencrypt(self.filepath)
        response = file.encrypt(key=key, keyfilepath=keyfilepath, savekeyfile=savekeyfile)
        return response
    
    def decrypt(self, key:str= None, keyfilepath:str= None):
        '''decrypt the file'''
        file = Dencrypt(self.filepath)
        response = file.decrypt(key=key, keyfilepath=keyfilepath)
        return response
        
        
    # ------------------------------------------
    
    # file info
    def info(self):
        '''get the information of the file'''
        data = os.stat(self.filepath)
        
        info = {
                "filename": self.filename,
                "directory": self.directory,
                "mode": data.st_mode,
                "ino": data.st_ino,
                "dev": data.st_dev,
                "nlink": data.st_nlink,
                "uid": data.st_uid,
                "gid": data.st_gid,
                "size": data.st_size,
                "atime": data.st_atime,
                "mtime": data.st_mtime,
                "ctime": data.st_ctime,
            }
        return info
        
    @property
    def show_info(self):
        result = self.info()
        show = "Info:------\n"
        words_len = len(max(result.keys(), key=len))
        for i in result.items():
    	    show += f"{i[0]}".ljust(words_len)
    	    show += f": {i[1]}\n"
        return show
    	
    
    # file info shortcuts
    @property
    def size(self):
        '''get the size of the file'''
        data = os.stat('test.txt')
        size = data.st_size
        return size
    
    @property
    def directory(self):
        '''get the directory of the file'''
        directory = os.path.dirname(self.filepath)
        if directory == '':
        	directory = os.getcwd()
        return directory
        
    @property
    def name(self):
        '''get the name of the file'''
        name = os.path.splitext(self.filename)[0]
        return name
        
    @property
    def type(self):
        '''get the type of the file'''
        type = os.path.splitext(self.filename)[1].split('.')[-1]
        return type
    
    
    @property
    def filename(self):
        '''get the file name of the file'''
        filename = os.path.basename(self.filepath)
        return filename
    
    
    
    # ------------------------------------------
    # addition easy do feautures
    # todo: add more features later if required
    
    @property
    def string(self, n:int=-1):
        '''show original content of the file in string'''
        file = open(self.filepath, self.modop('r'))
        red = file.read(n)
        file.close()
        return red

    def __str__(self):
        '''show self.read() of the file in string'''
        return str(self.read())
    


class TextFe(Fmf):
    '''
    TextFe: Text File manager expert
    '''
    __modes = ['t', 'b']
    
    def __init__(self, filepath: str, mode:str= 't')->None:
        # Parameter ValueError Check
        assert isinstance(filepath, str), f"file path {filepath} must be str"
        assert mode in self.__modes, f"mode must be one of {self.__modes}"
        
        #: param: filepath: str: file path or location
        #: param: mode: str: file mode -text or binary
        
        # inherite parent class: FileManagerFormat
        super().__init__(filepath, mode)
        
        self.filepath = filepath
        self.mode = mode
        
        # set default content
        self.default_content = ''

class JsonFe(Fmf):
    '''
    JsonFe: Json File manager expert
    '''
    __modes = ['t', 'b']
    
    def __init__(self, filepath: str, mode:str= 't')->None:
        # Parameter ValueError Check
        assert isinstance(filepath, str), f"file path {filepath} must be str"
        assert mode in self.__modes, f"mode must be one of {self.__modes}"
        
        #: param: filepath: str: file path or location
        #: param: mode: str: file mode -text or binary
        
        # inherite parent class: FileManagerFormat
        super().__init__(filepath, mode)
        
        self.filepath = filepath
        self.mode = mode
        
        # set default content
        self.default_content = '{}'
    
    # ------------------------------------------
    # --- This layer should change -------------
    # manage and access file content
    def read(self, *, cls=None, object_hook=None, parse_float=None, parse_int=None, parse_constant=None, object_pairs_hook=None, **kw):
        '''read content from the file'''
        file = open(self.filepath, self.modop('r'))
        red = json.loads(file.read(), cls=cls, object_hook=object_hook, parse_float=parse_float, parse_int=parse_int, parse_constant=parse_constant, object_pairs_hook=object_pairs_hook, **kw)  # parameters changable
        file.close()
        return red
    
    def write(self, content, *, skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True, cls=None, indent=None, separators=None, default=None, sort_keys=False, **kw):
        '''write content to the file: even overwrite'''
        assert isinstance(content, dict), f"write content should be dict type."
        file = open(self.filepath, self.modop('w'))
        json_string = json.dumps(content, skipkeys=skipkeys, ensure_ascii=ensure_ascii, check_circular=check_circular, allow_nan=allow_nan, cls=cls, indent=indent, separators=separators, default=default, sort_keys=sort_keys, **kw)  # parameters changable
        file.write(json_string)
        file.close()
        
    def append(self, content, *, skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True, cls=None, indent=None, separators=None, default=None, sort_keys=False, **kw):  # parameters changable
        '''append or update content to the file'''
        read = self.read()
        read.update(content)
        self.write(read)
        
    def create(self, content, *, skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True, cls=None, indent=None, separators=None, default=None, sort_keys=False, **kw):  # parameters changable
        '''create file and write content to the file: if file not exists'''
        assert isinstance(content, dict), f"write content should be dict type."
        file = open(self.filepath, self.modop('a'))
        json_string = json.dumps(content, skipkeys=skipkeys, ensure_ascii=ensure_ascii, check_circular=check_circular, allow_nan=allow_nan, cls=cls, indent=indent, separators=separators, default=default, sort_keys=sort_keys, **kw)
        file.write(json_string)
        file.close()
    
    def __getitem__(self, key):
        '''get content from the file'''
        return self.read()[key]
    
    def __setitem__(self, key, value):
        '''set content of the file: Note: only one iteration'''
        read = self.read()
        read[key] = value
        self.write(read)


	

def FileManager(filepath: str, filetype:str= None, mode:str= 't', formated=True):
    
    __modes = ['t', 'b']
    __filetypes = ['txt', 'json']

    # Parameter ValueError Check-- Part-1
    assert isinstance(filepath, str), f"file path {filepath} must be str"
    assert filetype in __filetypes or filetype is None, f"filetype {filetype} must be one of {__filetypes} or None"
    assert mode in __modes, f"mode must be one of {__modes}"
    assert isinstance(formated, bool), f"formated {formated} must be bool"
        
    #: param: filepath: str: file path or location
    #: param: filetype: str: file type = __filetypes or None
    #: param: mode: str: file mode -text or binary
    #: param: formated: bool: mentioning whether the file is not formated correct filetype or not, used to open if not supported.
    
    # set file type if required
    if filetype is None:
        filetype = Fmf(filepath).type
        if not formated:
            if filetype == '' or filetype not in __filetypes:
            	filetype = 'txt'
            
    
    # Parameter ValueError Check-- Part-2
    assert filetype in __filetypes, f"filetype {filetype} must be one of {__filetypes}"
    
    # call specified File manager expert
    if filetype == 'txt':
    	return TextFe(filepath, mode)
    elif filetype == 'json':
    	return JsonFe(filepath, mode)
    

if __name__ =="__main__":
    # File Manager
    fm = FileManager(
                filepath= __file__,
                filetype='txt',
                format=True,
                mode='t')
    print(fm)
