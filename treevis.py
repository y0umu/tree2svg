#!/usr/bin/python3

import sys    # sys.argv 
from itertools import takewhile
from xml.etree.ElementTree import Element, SubElement, ElementTree
import os # os.path.basename
##################################################
def isascii(s):
    return len(s) == len(s.encode())

##################################################
#                Tree related classes
class Node:
    _nid = 0   # class variable, used to identify different nodes
    
    def __init__(self, parent, info):
        '''parent: Node class object, the parent of current Node
                   Use "None" to indicate self is a root node
           info: str object'''
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
        '''Return a tuple "length" that indicate the (approximate) length of
        self.info
        length[0] is the numbers of alphas, digits and punctuations
        length[1] is other characters including Chinese chars'''
        total = len(self.info)
        count = 0
        for ch in self.info:
            if isascii(ch):
                count += 1
        return (count, total - count)
##################################################
def get_pluses_num(string):
    '''Return how many pluses "+" are there in the beggining of a string'''
    return len(tuple(takewhile(lambda c: c == "+" ,string)))

##################################################
def get_nth_depth_pxlen(nth_depth_nodes):
    '''Return the maximum pxlen of nth depth nodes
    invoacation: get_nth_depth_pxlen(treeObject.get_nth_level(n))'''
    return max((nd.pxlen for nd in nth_depth_nodes))

##################################################
def get_svg_path_str(tree, node0, node1):
    '''Return the string in the "d" attribute of svg path widget '''
    x0 = node0.x + node0.pxlen + tree.const_pxlen0 / 2.0
    y0 = node0.y - tree.const_pxlen1 / 4.0
    x1 = node1.x
    y1 = node1.y - tree.const_pxlen1 / 4.0
    x_mid = (x0 + x1) / 2.0
    y_mid = (y0 + y1) / 2.0
    string = "M " + str(x0) + " " + str(y0)\
             + " Q " \
             + str(x_mid) + " " + str(y1) + " " + str(x1) + " " + str(y1)
    return string
##################################################
class TreeVis:
    def __init__(self, filename):
        '''Initialize the tree with a the input file'''
        self._lines = []
        self.pxlens = []
        self.const_pxlen0 = 9 # approximate pixels for alphas and digits
        self.const_pxlen1 = 16 # approximate pixels for Chinese chars
        self._svg_viewbox = [-5, -5, 100, 100]

        with open(filename,"r", encoding="UTF-8") as f:
            for line in f:
                if line[0] == ";":
                    # Stop parsing if there is a ';' in the beginning of a line
                    # If there is no ';' in the file, parse all of it
                    break
                elif line[0] in ("#", "\n"):
                    # use the '#' as the commenting letter
                    continue
                else:
                    self._lines.append(line.rstrip("\n"))
        self.root = Node(None, "[virtual root]")
        self.pretrav_nodes = []
        node0 = self.root
        self.pretrav_nodes.append(node0)
        N = len(self._lines)
        if N >= 1:
            preline_pluses = get_pluses_num(self._lines[0])
        i = 0
        while i < N:
            thisline_pluses = get_pluses_num(self._lines[i])
            
            if thisline_pluses > preline_pluses:
                node1 = Node(node0, self._lines[i].lstrip("+"))
            elif thisline_pluses == preline_pluses:
                # Please note that the very begining node is surely in this branch
                node1 = Node(node0.parent, self._lines[i].lstrip("+"))
            else:
                node1 = Node(node0.nth_ancestor(preline_pluses - thisline_pluses + 1), self._lines[i].lstrip("+"))
            self.pretrav_nodes.append(node1)
            node1.depth = thisline_pluses + 1
            node0 = node1
            preline_pluses = thisline_pluses
            i += 1
            
        self._mark_pxlen()
        self._mark_coordinates()
        
    def _pre_traversal(self, node, result_nodes):
        '''Pre traverse nodes in the tree'''
        result_nodes.append(node)
        if node.isleaf:
            return
        for child in node.children:
            self._pre_traversal(child, result_nodes)
            
    def _pre_traversal_to_nth_level(self, node, i, n, nth_level_nodes):
        '''Pre traverse nodes that is in the depth of level n in the tree'''
        #if node.isvirtual == False:
            #print("Current node is " + node.info)
        #print("i=" + str(i))
        if i == n:
            #print(str(n) + "th nodes contain " + node.info)
            #print("returns\n")
            nth_level_nodes.append(node)
            return
        if node.isleaf:
            #print("  reached leaf node" + node.info)
            return
        i += 1
        #print("we have children:")
        #for c in node.children:
        #    print("  "  + c.info)
        for child in node.children:
            #print("  ->Before node " + child.info + " is dived in, i=" + str(i))
            self._pre_traversal_to_nth_level(child, i, n, nth_level_nodes)
            #print( " <-Returned from " + child.info + ", i=" + str(i))

    def pre_traversal(self):
        '''Pre traverse all nodes in the tree'''
        try:
            result_nodes = self.pretrav_nodes
        except:
            result_nodes = []
            self._pre_traversal(self.root, result_nodes)
            self.pretrav_nodes = result_nodes
        return result_nodes

    def get_nth_level(self, n):
        '''Return a list of Nodes at the same depth of level n (n = 0,1,...)'''
        nth_level_nodes = []
        self._pre_traversal_to_nth_level(self.root, 0, n, nth_level_nodes)
        return nth_level_nodes

    def _mark_pxlen(self):
        '''Add pixel lengths info to nodes'''  
        i = 1 # ignore the virtual node in the very begining of nodes
        while i < len(self.pretrav_nodes):
            length = self.pretrav_nodes[i].get_info_lenth()
##            print("node info length:" + str(length))
            self.pretrav_nodes[i].pxlen = length[0] * self.const_pxlen0 + length[1] * self.const_pxlen1
            i += 1

        i = 0
        nodes = self.get_nth_level(i)
        while nodes != []:
            max_pxlen = get_nth_depth_pxlen(nodes)
            self.pxlens.append(max_pxlen)
##            print(self.pxlens)
            i += 1
            nodes = self.get_nth_level(i)
            
    def _mark_coordinates(self):
        # Now we mark the coordinates of each node
        ori_x = 0
        ori_y = self.const_pxlen1 + 2
        y = ori_y   
        px_x_interval = 20
        px_y_interval = 30
        nodes = self.pretrav_nodes
        nodes[1].x = ori_x
        nodes[1].y = y
        view_max_x = ori_x + self.pxlens[nodes[1].depth]
        i = 2
        while i < len(nodes):
            if nodes[i].parent == nodes[i-1]:
                # is children
                nodes[i].x = nodes[i-1].x \
                             + self.pxlens[nodes[i-1].depth] \
                             + px_x_interval
                nodes[i].y = y
            elif nodes[i].depth == nodes[i-1].depth:
                # is sibling
                y += px_y_interval
                nodes[i].x = nodes[i-1].x
                nodes[i].y = y
                pass
            elif nodes[i].depth < nodes[i-1].depth:
                # is ancestor (not necessary parent)
                y += px_y_interval
                nodes[i].x = ori_x \
                             + px_x_interval * (nodes[i].depth - 1) \
                             + sum(self.pxlens[1:nodes[i].depth])
                nodes[i].y = y                
            else:
                raise UserWarning("Unexpected branch reached")
            x = nodes[i].x + self.pxlens[nodes[i].depth]
            if x > view_max_x:
                view_max_x = x
            i += 1
            self._svg_viewbox[2] = view_max_x + 2*abs(self._svg_viewbox[0])
            self._svg_viewbox[3] = y + 2*abs(self._svg_viewbox[1])
        

    def writesvg(self, svgfname):
        '''Write to SVG file'''
        viewbox = self._svg_viewbox
        viewbox_string = ""
        for i in range(0,3):
            viewbox_string += str(viewbox[i]) + " "
        viewbox_string += str(viewbox[3])
        root = Element("svg", \
                       {"xmlns": "http://www.w3.org/2000/svg", \
                        "version": "1.1", \
                        "viewBox": viewbox_string })
        texts = []
        for nd in self.pretrav_nodes[1:]:
            text_widget = SubElement(root, "text", {"x": str(nd.x), \
                                                    "y": str(nd.y), \
                                                    "fill":"navy", \
                                                    "font-size": "16"})
            text_widget.text = nd.info
        
        # draw curves
        i = 1
        nodes = self.pretrav_nodes
        while i < len(nodes):
            if not nodes[i].isleaf:
                for child in nodes[i].children:
                    path_string = get_svg_path_str(self, nodes[i], child)
                    path_widget = SubElement(root, "path", {"d": path_string,\
                                                        "stroke-width": "1",\
                                                        "stroke": "red",\
                                                        "fill":"none"})
            i += 1
        tree = ElementTree(root)
        tree.write(svgfname, encoding="utf-8")
            

##################################################
# Command line interface & file input processing
def main():
    def cmd_help():
        print("Usage: treevis.py <tree dedcription file> [output SVG file name]")
        
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        cmd_help()
        return
    
    basename = os.path.basename(sys.argv[1])
    _name = basename.split(sep=".")
    outputname = _name[0]
    try:
        t = TreeVis(sys.argv[1])
    except FileNotFoundError:
        print("No such file \"" + sys.argv[1] + "\"")
        return
    except IndexError:
        print("Error processing, invalid input file syntax?")
        return
    except:
        raise
        
    if len(sys.argv) == 2:
        outputname += ".svg"
    else: # len(sys.argv) == 3:
        outputname = sys.argv[2]
    t.writesvg(outputname)
    print("Tree visualization saved as \"" + outputname + "\"")
    
##################################################

if __name__ == "__main__":
    main()
