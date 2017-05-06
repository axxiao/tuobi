
# coding: utf-8

# In[1]:

import inspect, os
working_dir=os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) 
#curdir=os.getcwd()


# In[4]:

import sys
sys.path.append(working_dir)
print('working in ',working_dir)
from import_from_file import load_module_extract
def load_ax_module(module):
    return load_module_extract(working_dir,module)
