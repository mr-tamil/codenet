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

__ccfile = codio.CnetConfiguration()
__ccfile.mainfile.append(config_data)

    
