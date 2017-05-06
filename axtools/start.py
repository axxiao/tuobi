
# coding: utf-8

# In[1]:

import inspect, os
curdir=os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) 
#curdir=os.getcwd()


# In[4]:

import sys
sys.path.append(curdir)
print('working in ',curdir)
from import_from_file import load_module_extract as load_module

