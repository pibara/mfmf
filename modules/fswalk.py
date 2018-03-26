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

class RegularFile:
    def __init__(self,imgpath,inode,name,fs,blocksize):
        self.name=name
        self.imgpath=imgpath
        self.inode=inode
        self.fs=fs
        self.blocksize=blocksize
    def children(self):
        return []
    def get_carvpath(self,allocate_storage):
        file_entry = self.fs.open_meta(inode=self.inode)
        size = file_entry.info.meta.size
        if size > 0:
            for attr in file_entry:
                if attr.info.name == None:
                    cp = ""
                    for run in attr:
                        runstart = self.blocksize * run.addr
                        runlen = self.blocksize * run.len
                        subcp = str(runstart) + "+" + str(runlen)
                        if cp != "":
                            cp = cp + "_"
                        cp = cp + subcp
                    return self.imgpath[cp]["0+"+str(size)].as_file_path()
        return self.imgpath["S0"].as_file_path()
    def get_meta(self):
        meta = {}
        meta["name"] = self.name
        return meta

class SubDir:
    def __init__(self,imgpath,inode,name,fs,blocksize,level):
        self.name=name
        self.level = level + 1
        self.imgpath=imgpath
        self.inode=inode
        self.fs=fs
        self.blocksize=blocksize
        self.level = level + 1
    def children(self):
        file_entry = self.fs.open_meta(inode=self.inode)
        for dent in file_entry.as_directory():
            directory_entry = dent.info.name.name
            entry_name = directory_entry.decode("utf8")
            entry_addr = int(dent.info.name.meta_addr)
            entry_type = dent.info.name.type
            if str(entry_type) == 'TSK_FS_NAME_TYPE_DIR' and entry_name != ".." and entry_name != ".":
                yield SubDir(self.imgpath,entry_addr,entry_name,self.fs,self.blocksize,self.level)
            if str(entry_type) == 'TSK_FS_NAME_TYPE_REG':
                yield RegularFile(self.imgpath,entry_addr,entry_name,self.fs,self.blocksize)
    def get_carvpath(self,allocate_storage):
        return None
    def get_meta(self):
        meta = {}
        meta["name"] = self.name
        return meta
    
class RootNode:
    def __init__(self,carvpathfile):
        self.cp=carvpathfile
        self.imgpath = carvpathfile.as_file_path()
        self.img=pytsk3.Img_Info(self.imgpath)
        self.fs=None
        try:
            self.fs = pytsk3.FS_Info(self.img)
            self.ino = self.fs.info.root_inum
            self.blocksize = self.fs.info.block_size
        except:
            pass
    def children(self):
        if self.fs != None:
            blocksize = self.fs.info.block_size
            file_entry = self.fs.open_meta(inode=self.ino)
            for dent in file_entry.as_directory():
                directory_entry = dent.info.name.name
                entry_name = directory_entry.decode("utf8")
                entry_addr = int(dent.info.name.meta_addr)
                entry_type = dent.info.name.type
                if str(entry_type) == 'TSK_FS_NAME_TYPE_DIR' and entry_name != "..":
                    yield SubDir(self.cp,entry_addr,entry_name,self.fs,self.blocksize,0)
                if str(entry_type) == 'TSK_FS_NAME_TYPE_REG':
                    yield RegularFile(self.cp,entry_addr,entry_name,self.fs,self.blocksize)
    def get_meta(self):
        meta = {}
        if self.fs != None:
            meta["block_size"] = self.fs.info.block_size
        return meta

class FsWalkModule:
    def root(self,carvpathfile,arg):
        return RootNode(carvpathfile)
    def name(self):
        return "fswalk"

run(FsWalkModule())

