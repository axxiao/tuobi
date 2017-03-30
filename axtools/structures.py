"""
This is the common data stucture objects which may be usable
Part of the package of Alex's tools

Should be placed at <jupyter notebook root>/axtoools

__author__ = "Alex Xiao <http://www.alexxiao.me/>"
__date__ = "2017-02-08"
__version__ = "0.5"

"""
class Tree(object):
    """
        Return the object the code carry
    """
    def __call__(self):
        return self.obj
    """
        The Node of tree object
        
        name: the name of the root
        obj: the object assigned to the node
        parent: the parent of the node, default to None for root        
        *NOTE: to add a child, please use add function rather than define parent here!
    """
    def __init__(self,name,obj,parent=None):
        self.name=name
        self.obj=obj
        self.parent = parent
        if parent!=None and  not parent.has(name):
            #in case of the node has not been addded to parent
            parent.children[name]=self       
        self.children=dict()
        if parent==None:
            self.level=0
        else:
            self.level=parent.level+1
    """
        Return the list of the children
        
        output:
            [list] of all children
    """
    def list(self):
        if len(self.children)>0:
            return list(self.children.keys())
    """
        If the current node the root of the tree
    """
    def is_root(self):
        return self.parent==None
    
    """
        If the current node the leaf of the tree (no child)
    """
    def is_leaf(self):
        rtn=True
        if len(self.children)>0:
            rtn=False
        return rtn
    
    """
        Remove one child
    """
    def remove(self,name):
        self.children.remove(name)
    """
        Add one child
        
        Input:
            name: the name of the child
            obj: the child, if the object is a tree, it all be hooked to current tree as a node
    """
    def add(self,name,obj):
        if type(obj)==type(self):
            #adding a tree as object
            obj.name=name
            obj.hook(self)
        else:
            #self.children[name]=
            Tree(name,obj,self)
    """
        If the node has given child
    """    
    def has(self,name):
        return name in self.children
    """
        Get the child by name, None if not exist
    """    
    def child(self,name):
        if name in self.children:
            return self.children[name]
    """
        The max depth from current node
    """    
    def depth(self):
        dep=0
        if len(self.children)>0:
            for child in self.children:
                cdep=self.children[child].depth()
                if cdep>dep:
                    dep=cdep 
            dep+=1    
        return dep
    
    """
        Cascade the level change to all children
    """
    def __update_level(self,parentlevel):
        self.level=parentlevel+1
        if len(self.children)>0:
            for child in self.children:
                self.children[child].__update_level(self.level)
        
        
    """
        Hook the current root node to a parent node of the other tree
    """
    def hook(self, parent):
        if self.parent==None and parent!=None and  not parent.has(self.name):
            #ok to hook            
            self.parent=parent
            #in case of the node has not been addded to parent
            parent.children[self.name]=self 
            self.__update_level(parent.level)
        else:
            if self.parent!=None:
                raise ValueError('[Error] This is not root node, can not be hooked to the other parent!')
            if parent==None:
                raise ValueError('[Error] Cannot hook to the None parent!')
            if parent.has(self.name) and parent.child(self.name)!=self:
                raise ValueError('[Error] Cannot replace existing child of parent!')
    
    def __repr__(self):
        
        if self.parent==None:
            out='['+self.name+']'
        else:
            out=''
            length=15
            for i in range(1,self.level):
                out+=''.ljust(length,' ')
            out+='('+str(self.level)+')'
            
            out+=('['+self.name+']').rjust(length-1,'-')
        if len(self.children)>0:
            for child in self.children:
                out+='\n'+self.children[child].__repr__()
        return out
    
    

