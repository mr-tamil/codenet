from . import codio
from . import filemanager

# configuration file default data
__config_data = {
    "display" : {
        "store" : True,
        "storelength" : 10
    }
}

__ccfile = codio.CnetConfiguration()
__ccfile.mainfile.append(__config_data)

    
