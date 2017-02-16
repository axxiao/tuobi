"""
The common tools
"""
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
