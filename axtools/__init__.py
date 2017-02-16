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
    
    from notebook_extract import JupyterNotebookExtract
    from import_from_file import load_module_extract as load_module  
    #from DB import DB
except:
    JupyterNotebookExtract=None
    from import_from_file import load_module  
    pass

DB=load_module('axtools','DB')
import aws
cache=DB.im_memory_share
import tools
