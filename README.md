# tree2svg
A python program that turns a tree described in a text file into an SVG visible.
Useful as a simple mindmap generator. You can also utilize it to illustrate your websites, papers, etc.

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
1. The font-size, curve color, etc, are hard coded and is not customizable via the command line interface. Further, since the exact coordinates are computed based on the font size and the number of characters in one node, it could be troublesome to handle the font size differences between different fonts. Currently I have no idea on how to cope with it. In fact, the current implemetation uses an approximate, inaccurate estimate. If you have played with this program you may find that you have to add whitespaces to the end of certain nodes in order to not interlace the text with the connection lines ("path" in SVG parlance).
2. If one node contains too much stuff, it could look ugly in the SVG (very long line for that node). Maybe a "smart" way to automatically warp the lines should be implemented.
3. Alignment cannot be adjusted.

# TODO
1. Rewrite the command line argument parsing interface using standard library argparse.
2. A parser class may need implementing if I were to make the tree descrpition file more complex (and more flexible).
