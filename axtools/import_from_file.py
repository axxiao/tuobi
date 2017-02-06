import importlib
import notebook_extract

import os.path

DEBUG=False
def set_DEBUG(flg):
    DEBUG=flg
    if DEBUG:
        notebook_extract.OUT_FLAG=True
    else:
        notebook_extract.OUT_FLAG=False
def load_module(path,module):
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
    return importlib.import_module(module)
