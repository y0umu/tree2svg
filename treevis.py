#!/usr/bin/python3
'''
treevis.py
Traslate your tree description file into SVG.
'''
# import sys    # sys.argv
import os # os.path.basename
import argparse

from treevis.treevisualizer import TreeVis
##################################################
# Command line interface & file input processing
def main():
    # Parse the command line
    cmd_parser = argparse.ArgumentParser(description="turns a tree described in a text file into an SVG visible")
    cmd_parser.add_argument("tree_description_file", metavar="<tree dedcription file>", \
                            help="The text file describing the tree. See README.md for syntax of such file")
    cmd_parser.add_argument("-o", "--output-file-name", metavar="output_SVG_file_name", \
                            help="Specify the output file name. If you don\'t give this option, it will be inferred from your input file name")
    args = cmd_parser.parse_args() # will exit the program if anything wrong

    # Build the tree
    basename = os.path.basename(args.tree_description_file)
    _name = basename.split(sep=".")
    outputname = _name[0]
    try:
        t = TreeVis(args.tree_description_file)
    except FileNotFoundError:
        print("No such file \"" + args.tree_description_file + "\"")
        return
    except IndexError:
        print("Error processing, invalid input file syntax?")
        return
    except:
        raise

    # Write to file
    if args.output_file_name is None:
        outputname += ".svg"
    else: # len(sys.argv) == 3:
        outputname = args.output_file_name
    t.writesvg(outputname)

    # Prompt the user upon finishing
    print("Tree visualization saved as \"" + outputname + "\"") 
##################################################

if __name__ == "__main__":
    main()
