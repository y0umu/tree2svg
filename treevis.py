#!/usr/bin/python3
'''
treevis.py
Traslate your tree description file into SVG.
'''
import sys    # sys.argv
import os # os.path.basename

from treevisualizer import TreeVis
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
