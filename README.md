# tree2svg
A toy program written in python that turns a tree described in a text file into an SVG visible

# Requirements
Python 3 

# Usage
```
python3 treevis.py tree_description_file.txt
```
or
```
python3 treevis.py tree_description_file.txt svg_name.svg
```

For Unix, Linux users:
```
dos2unix treevis.py
chmod u+x treevis.py
./treevis.py tree_description_file.txt  # supply svg_name.svg if you want
```

# Tree description file syntax
As in "cooked wheaten food.txt", a tree description file is a text file encoded in UTF-8.
```
面食
+面条(Noodles)
++炒面(Stir-Fried Noodles with Vegetables, "Chow Mein")
++凉面(cold noodles in sauce)
++意大利面(spaghetti)
+包子/馒头类
++包子(steamed stuffed bun)
++馒头(steamed bun, "Manjuu")
++窝窝头(steamed bread of corn)
+饺子(Chinese dumpling, "Jiaozi")
; End of recipe
```

All lines before the line that starts with a semi-colon ";" are deemd nodes in the tree, except those begin with a sharp symbol "#". Empty lines are ignored as well. If there is no line begins with a ";", treevis.py will parse till the end of file.

Lines representing nodes are arranged in the order as that in preorder traversal (DLR) of the tree. Number of pluses "+" indicates the depth of the node in the tree. Invalid numbers of pluses, either too many or not sufficient, will lead to error.

# Limitations
0. Limited tests so far, expect bugs...
1. The font-size, curve color, etc, are hard coded and is not customizable via the command line interface.

# TODO
0. Tidy up the code... Methods like TreeVis._pre_traversal are used in the early stages of coding, but not in the present code. (Should they be removed?)
1. I do have a feeling that I am still coding in C, therefore some improvements could be made to put it "more python".



