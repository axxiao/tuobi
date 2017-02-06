import sys,os,IPython
platform=sys.platform
jupyter=IPython.get_ipython()
sys.path.append(os.path.join(jupyter.home_dir,'axtools'))
from import_from_file import load_module
from notebook_extract import JupyterNotebookExtract
