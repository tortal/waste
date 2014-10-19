#  -*- coding: utf-8 -*-
# python 2.7.5
# author: roy.nard@gmail.com
# os: win32

enableDebug = None

def log(*msgs):
    if not enableDebug:
        return
    msg = [str(s) + ' ' for s in msgs]
    print ''.join(msg)