"""
The common tools
"""
import re
def mysearch(orig_str,begin,end=None,strip=False):
    """
    The generator function to return all information that in between start/end key words
    
    Input:
        orig_str: the string to be searched
        begin: the keyword for begining (exclusive)
        end [Optional]: the keyword for the end (exclusive), if not defined, get all the info before next begin
        strip [Optional]: default to False, which will not strip info if empty
    
    Output:
        List of all result (yield)
    """
    first=orig_str.find(begin)
    for patt in orig_str[first:].split(begin):
        if strip:
            patt=patt.strip()
        if end==None:
            if len(patt)>0:
                yield patt
        else:
            end_pos=patt.find(end)
            if end_pos>0 or (strip==False and end_pos==0):
                yield patt[:end_pos]
def nvl_dict(in_dict,key_name,default):
    """
    Try to get a value from dict, if not return the default value
    
    input:
        in_dict: the dict to be looked up
        name: the name of item
        default: default value
    """
    rtn=default
    if key_name in in_dict:
        rtn=in_dict[key_name]
    return rtn
def get_name(obj):
    if hasattr(obj,'name'):
        nm=obj.name
    else:
        nm=str(obj)
    return nm

def has_functions(obj,methods,raise_error_flag=True):
    """
    To check if object has method as a function
    Inputs:
        obj: the object
        methods: the list of functions to check
        raise_error_flag: [default to True], if True, raise ValueError if not found the function
    Output:
        return the result True/ False
    
    """
    #'status' in dir(services[service_name])
    lkp=dir(obj)
    rtn=False
    missed_list=set(methods)-set(lkp)
    if len(missed_list)>0:
        err_msg='Object '+get_name(obj)+'['+str(type(obj))+'] does not have expected function '+str(missed_list)
    else:
        rtn=True
        invlid_list=[]
        for mth in methods:
            if not callable(getattr(obj,mth)):
                #find a not callable
                rtn=False
                invlid_list.append(mth)
        err_msg='Object '+get_name(obj)+'['+str(type(obj))+'] has attribute '+str(invlid_list)+' NOT callable!'
        #if all are included
        
    
    if rtn==False and raise_error_flag:
        #Raise error
        raise ValueError(err_msg)
    return rtn

def has_function(obj,method,raise_error_flag=True):
    """
    To check if object has method as a function
    Inputs:
        obj: the object
        method: the function to check
        raise_error_flag: [default to True], if True, raise ValueError if not found the function
    Output:
        return the result True/ False
    
    """
    #'status' in dir(services[service_name])
    print(obj,method)
    rtn=hasattr(obj,method) and callable(getattr(obj,method))
    if rtn==False and raise_error_flag:
        #Raise error
        raise ValueError('Object '+get_name(obj)+'['+str(type(obj))+'] does not have expected function '+method)
    return rtn
def tryrun(function,*args,**kwargs):
    """
        try to run the function in standard try cacth block, to reduce coding
        
        Input:
          1. The function to be run
          2. Arguments (if any)
          3. Key word arguments (if any)
        
        Output:
            True/ False: True= Succeeded, False=Failed with error
            The return the original function
        
    """
    try:
        return True,function(*args,**kwargs)
    except Exception as e:
        return False,e


    
# This example requires the requests library be installed.  You can learn more
# about the Requests library here: http://docs.python-requests.org/en/latest/

from requests import get
def get_pulic_ip():
    """
        Return the public ip of the requested machine
        
        Input: N/A
        
        Output: IP V4 string xxx.xxx.xxx.xxx
    """
    ip = get('https://api.ipify.org').text
    return ip

