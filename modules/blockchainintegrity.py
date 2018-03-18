#!/usr/bin/python
#This is both a test and a demo of the EventLoop usage in the base mattock
#language binding.
import json
try:
    #If you build your own module framework, it is sugested you name it fmfw as working title
    #so all mfmf modules work out of the box potentially. 
    from fmfw import run
except:
    from mfmf import run

def process_merkletree_root_hash(hsh):
    print hsh
    return "00000000"

class RootNode:
    def __init__(self,carvpathfile):
        imgpath = carvpathfile.as_file_path()
        mtree = {}
        self.merkleroot = None
        with open(imgpath,"r") as f:
            try:
                mtree = json.loads(f.read())
            except:
                print "Oops: invalid json."
                pass
        if "mh" in mtree:
            self.merkleroot = mtree["mh"]
        else:
            print "Oops: no 'mh' in merkletree JSON."
    def children(self):
        return []
    def get_meta(self):
        meta = {}
        if self.merkleroot != None:
            meta["transaction_id"] =  process_merkletree_root_hash(self.merkleroot)
        return meta

class BlockChainIntegrityModule:
    def root(self,carvpathfile,arg):
        return RootNode(carvpathfile)
    def name(self):
        return "blockchainintegrity"

run(BlockChainIntegrityModule())

