__version__ = "0.1.0"
__author__ = "Thamizharasu S"

from . import codio
from . import NLP
from . import filemanager
from . import decorators
from . import wolf



# configuration file default data
config_data = {

}

# cnet configuration data folder handler
class CnetConfiguration:
    def __init__(self):
        self.parent_folder_name = '.cnet'
        self.parent_folder_path = codio.os.path.join(codio.os.getcwd(), self.parent_folder_name)
        if not codio.os.path.exists(self.parent_folder_path):
            codio.os.mkdir(self.parent_folder_path)
        
        self.config_file_name = 'config.json'
    
    @property
    def mainfile(self):
        return self.getfile(self.config_file_name)

    def getfile(self, filename):
        get_file_path = codio.os.path.join(self.parent_folder_path, filename)
        if not codio.os.path.exists(get_file_path):
            file = FileManager(get_file_path)
            file.clear()
            return file
        else:
            return filemanager.FileManager(get_file_path)


__ccfile = CnetConfiguration()
__ccfile.mainfile.append(config_data)

    
