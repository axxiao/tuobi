"""
The package of Alex's tools

Should be placed at <jupyter notebook root>/axtoools

__author__ = "Alex Xiao <http://www.alexxiao.me/>"
__date__ = "2017-02-08"
__version__ = "0.5"

"""

import sys,os
try:    
    platform=sys.platform    
    import IPython    
    jupyter=IPython.get_ipython()
    sys.path.append(os.path.join(jupyter.home_dir,'axtools'))
    HOME=jupyter.home_dir
    from notebook_extract import JupyterNotebookExtract
    from import_from_file import load_module_extract as load_module  
    #from DB import DB
except:
    JupyterNotebookExtract=None
    from import_from_file import load_module  
    HOME=(os.path.abspath('.')).replace('/axtools','')
    pass

DB=load_module('axtools','DB')
#cache=DB.im_memory_share
tools=load_module('axtools','tools')
structures=load_module('axtools','structures')
aws=load_module('axtools','aws')
Log=load_module('axtools','Log')
