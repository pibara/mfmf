#!/usr/bin/python
import magic

class TrivialTreeWalker:
    def __init__(self,module=None):
        self.module = module
    def set_module(self,module):
        self.module = module
    def mimetype(self,cp):
        mimetype = magic.detect_from_filename(cp).mime_type
        return mimetype
    def _node_walk(self,node,child_submit,allocate_storage,job,level):
        for childnode in node.children():
            self._node_walk(childnode,child_submit,allocate_storage,job,level+1)
            cp = childnode.get_carvpath(allocate_storage)
            meta = childnode.get_meta()
            if not "mime-type" in meta:
                meta["mime-type"] = self.mimetype(cp)
            child_submit(job,cp,meta)
    def walk(self,carvpath,argument,child_submit,allocate_storage,job):
        node = self.module.root(carvpath,argument)
        self._node_walk(node,child_submit,allocate_storage,job,0)
        meta = node.get_meta()
        return meta

 
