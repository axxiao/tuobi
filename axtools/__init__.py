"""
The package of Alex's tools

Should be placed at <jupyter notebook root>/axtoools

__author__ = "Alex Xiao <http://www.alexxiao.me/>"
__date__ = "2016-02-08"
__version__ = "0.5"

"""
import sys,os,IPython
platform=sys.platform
jupyter=IPython.get_ipython()
sys.path.append(os.path.join(jupyter.home_dir,'axtools'))
#from DB import DB

from import_from_file import load_module
DB=load_module('axtools','DB')

from notebook_extract import JupyterNotebookExtract
