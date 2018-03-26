#!/usr/bin/python
#This is both a test and a demo of the EventLoop usage in the base mattock
#language binding.
try:
    #If you build your own module framework, it is sugested you name it fmfw as working title
    #so all mfmf modules work out of the box potentially. 
    from fmfw import run
except:
    from mfmf import run

class RootNode:
    def __init__(self,carvpathfile):
        self.cp=carvpathfile
        imgpath = carvpathfile.as_file_path()
        with open(imgpath,"r") as f:
            meta = f.read()
    def children(self):
        return []
    def get_meta(self):
        meta = {}
        return meta

class DsmModule:
    def root(self,carvpathfile,arg):
        return RootNode(carvpathfile)
    def name(self):
        return "dsm"

run(DsmModule())

