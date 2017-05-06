"""
To load module dynamitically

__author__ = "Alex Xiao <http://www.alexxiao.me/>"
__date__ = "2017-02-08"
__version__ = "0.5"

"""

DEBUG=True
import importlib,sys

import os.path
try:
    import notebook_extract
except:
    if DEBUG:
        print("working in none-Jupyter environment")
    pass
import sys
def set_DEBUG(flg):
    DEBUG=flg
    if DEBUG:
        notebook_extract.OUT_FLAG=True
    else:
        notebook_extract.OUT_FLAG=False
def load_module_extract(path,module):
    extr=notebook_extract.JupyterNotebookExtract()
    if os.path.isabs(path):
        module_file_name=os.path.join(path,module)
    else:
        module_file_name=os.path.join(extr.base_dir,path,module)
    nbTS=-1.0
    nbfname=module_file_name+'.ipynb'
    if os.path.isfile(nbfname):
        #found the time
        nbTS=os.path.getmtime(nbfname) 
    pyTS=-1.0
    pyfname=module_file_name+'.py'
    if os.path.isfile(pyfname):
        #found the time
        pyTS=os.path.getmtime(pyfname) 
    if nbTS>pyTS:
        #.ipynb is later than .py
        if DEBUG:
            print('Found change, converting latest',nbfname,'to',pyfname)
        extr.extract(nbfname,pyfname,True)
    print('Loading',pyfname)
    return load_module(path,module)
            
def load_module(path,module):
    if not path in sys.path:
        sys.path.insert(0, path)
    if module in sys.modules:
        if DEBUG:
            print('Existing module, reloading')
        return importlib.reload(sys.modules[module])
    return importlib.import_module(module)
#def load_module(path,module):
#    extract_py(path,module)
#    return importlib.import_module(module)
#load_module_extract('axtools','import_from_file')
