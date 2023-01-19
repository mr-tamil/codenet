import os
from . import filemanager


# cnet configuration data folder handler
class BasicConfiguration:
    def __init__(self, parentfoldername='', mainfilename='config.json'):
        self.parent_folder_name = parentfoldername
        self.parent_folder_path = os.path.join(os.getcwd(), self.parent_folder_name)
        if not os.path.exists(self.parent_folder_path):
            os.mkdir(self.parent_folder_path)
        
        self.config_file_name = mainfilename
    
    @property
    def mainfile(self):
        return self.getfile(self.config_file_name)

    def getfile(self, filename):
        get_file_path = os.path.join(self.parent_folder_path, filename)
        if not os.path.exists(get_file_path):
            file = filemanager.FileManager(get_file_path)
            file.clear()
            return file
        else:
            return filemanager.FileManager(get_file_path)



# configuration file default data
__config_data = {
    "display" : {
        "store" : True,
        "storelength" : 10
    }
}

cnetconfig = BasicConfiguration('.cnet', 'config.json')

def reset():
    cnetconfig.mainfile.write(__config_data)

if not os.path.exists(os.path.join(cnetconfig.parent_folder_path, 'config.json')):
    reset()
