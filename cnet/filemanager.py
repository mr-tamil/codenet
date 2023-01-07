'''filemanager :: File Manager : as fm'''

# import libraries
import os, shutil


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
        self.path = path
    
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
        type = os.path.splitext(self.filename)[1]
        return type
    
    
    @property
    def filename(self):
        '''get the file name of the file'''
        filename = os.path.basename(self.filepath)
        return filename
    
    
    
    # ------------------------------------------
    # addition easy do feautures
    # todo: add more features later if required
    
    def __str__(self):
    	'''show self.read content of the file'''
    	return self.read()
    


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


def FileManager(filepath: str, filetype:str= None, mode:str= 't', format=False):
    
    __modes = ['t', 'b']
    __filetypes = ['txt']

    # Parameter ValueError Check-- Part-1
    assert isinstance(filepath, str), f"file path {filepath} must be str"
    assert filetype in __filetypes or filetype is None, f"filetype {filetype} must be one of {__filetypes} or None"
    assert mode in __modes, f"mode must be one of {__modes}"
    assert isinstance(format, bool), f"format {format} must be bool"
        
    #: param: filepath: str: file path or location
    #: param: filetype: str: file type = __filetypes or None
    #: param: mode: str: file mode -text or binary
    #: param: format: bool: format counts exact file format and filetype
    
    # set file type if required
    if filetype is None:
        filetype = Fmf(filepath).type
        if not format:
            if filetype == '' or filetype not in __filetypes:
            	filetype = 'txt'
            
    
    # Parameter ValueError Check-- Part-2
    assert filetype in __filetypes, f"filetype {filetype} must be one of {__filetypes}"
    
    # call specified File manager expert
    if filetype == 'txt':
    	return TextFe(filepath, mode)
    

if __name__ =="__main__":
    # File Manager
    fm = FileManager(
                filepath=__file__,
                filetype='txt',
                format=True,
                mode='t')
    print(fm)