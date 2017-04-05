#!/usr/bin/python
#This is both a test and a demo of the EventLoop usage in the base mattock
#language binding.
try:
    #If you build your own module framework, it is sugested you name it fmfw as working title
    #so all mfmf modules work out of the box potentially. 
    from fmfw import run
except:
    from mfmf import run

import pytsk3

class Partition:
    def __init__(self,carvpath,ptype):
        self.carvpath=carvpath
        self.ptype=ptype
        if ptype[-2:].lower() == "fs":
            self.mime = "application/file-system"
        else:
            if ptype.lower() == "unallocated":
                self.mime = "disk-partition/unallocated"
            else:
                self.mime = None
    def get_carvpath(self,allocate_storage):
        return self.carvpath
    def children(self):
        return []
    def get_meta(self):
        meta = {}
        meta["partition-type"] = self.ptype
        if self.mime != None:
            meta["mime-type"] = self.mime
        return meta

    
class RootNode:
    def __init__(self,carvpathfile):
        self.cp=carvpathfile
        imgpath = carvpathfile.as_file_path()
        img=pytsk3.Img_Info(imgpath)
        self.volume = pytsk3.Volume_Info(img)
    def children(self):
        blocksize = self.volume.info.block_size
        for part in self.volume:
            poffset = part.start * blocksize
            psize = part.len * blocksize
            pdesc = part.desc
            carvpath = self.cp[str(poffset) + "+" + str(psize)]
            yield Partition(carvpath.as_file_path(),pdesc)
    def get_meta(self):
        meta = {}
        meta["block_size"] = self.volume.info.block_size
        meta["endian"] = str(self.volume.info.endian)
        meta["part_count"] = self.volume.info.part_count
        meta["vstype"] = str(self.volume.info.vstype)
        return meta

class MmlsModule:
    def root(self,carvpathfile,arg):
        return RootNode(carvpathfile)
    def name(self):
        return "mmls"

run(MmlsModule())

