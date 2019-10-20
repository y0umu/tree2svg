'''
datastructure.py
Implementing the underlying data structure.
Currently Node is implemented here.
'''
from .util import isascii
##################################################
#              Tree related classes
class Node:
    _nid = 0   # class variable, used to identify different nodes
    
    def __init__(self, parent, info):
        '''
        parent: Node class object, the parent of current Node
                Use "None" to indicate self is a root node
        info: str object
        '''
        self.nid = Node._nid
        Node._nid += 1
        self.info = info
        self.children = []
        self.isvirtual = False  # only the virtual root node should have this attribute true
        self.depth = -1 # modified by TreeVis __init__
        self.pxlen = -1
        self.x = -1
        self.y = -1
        if type(parent) == Node:
            # it is a normal node instead of a root node
            self.parent = parent
            parent.children.append(self)
        else:
            # it is a root node
            self.parent = self  # point to itself
            self.isvirtual = True

    def __repr__(self):
        return "Node_nid_" + str(self.nid)

    def __str__(self):
        msg = ".nid = " + str(self.nid) + "\n" \
              + ".info = " + self.info + "\n" \
              + ".depth = " + str(self.depth) + "\n" \
              + ".x = {0}, .y = {1}".format(str(self.x), str(self.y)) + "\n" \
              + ".parent = " + str(self.parent.nid) + "\n" \
              + ".children = " + str(self.children) + "\n"
        return msg

    @property
    def isleaf(self):
        '''Return True if self.children is empty'''
        if self.children == []:
            return True
        else:
            return False
        
##    def add_child(self, child):
##        '''Add an child to current node'''
##        self.children.append(child)
##        child.parent = self

    def nth_ancestor(self, nth):
        '''Return the nth ancestor of current node'''
        i = 0
        ancestor = self
        while i < nth:
            ancestor = ancestor.parent
            i += 1
        return ancestor

    def get_info_lenth(self):
        '''
        Return a tuple "length" that indicate the (approximate) length of
        self.info
        length[0] is the numbers of alphas, digits and punctuations
        length[1] is other characters including Chinese chars
        '''
        total = len(self.info)
        count = 0
        for ch in self.info:
            if isascii(ch):
                count += 1
        return (count, total - count)
