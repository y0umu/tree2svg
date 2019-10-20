'''
util.py
Provides utility functions for other modules
'''
##################################################
def isascii(s):
    '''A simple hack to determine whether string s is ASCII'''
    return len(s) == len(s.encode())
