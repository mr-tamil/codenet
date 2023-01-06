"""codio: Code Toolkit for I/O"""


import os, sys, subprocess, importlib

def command_call(cmd: str):
	subprocess.check_call(cmd)


# Install Packag
def install_package(name)->None:
    if importlib.util.find_spec(name) is None:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', name])

def install_packages(names:['packages'])->None:
    for name in names:
        install_package(name)
	

# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore
def enablePrint():
    sys.stdout = sys.__stdout__

# Enable or Disable Print output 
class PrintStatements:
    def __init__(self, state= True):
        self.state = state
    	
    def __enter__(self):
        if not self.state:
            sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self.state:
            sys.stdout.close()
            sys.stdout = sys.__stdout__

