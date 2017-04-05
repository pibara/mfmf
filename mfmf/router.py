#!/usr/bin/python
import json
#Trivial router that routs data to single tool toolchain based soly on mime-type.
class TrivialRouter:
    def __init__(self):
        #Simple json that maps from mime-type to module;ext
        with open("/etc/mfmf/mattock_trivial_router_conf.json","r") as f:
            jsondata = f.read()
            self.rules = json.loads(jsondata) 
    def _mime_to_module(self,mime):
        if mime in self.rules:
            rule = self.rules[mime]
            return rule[0:rule.find(";")]
        return None
    def _mime_to_ext(self,mime):
        if mime in self.rules:
            rule = self.rules[mime]
            return rule[rule.find(";")+1:]
        return "dat"
    def process_child_meta(self,meta):
        mime = meta["mime-type"]
        return self._mime_to_module(mime),"",mime,self._mime_to_ext(mime),None,""
    def set_state(self,router_state):
        pass
    def get_walk_argument(self):
        return None
    def process_parent_meta(self,toplevel_meta):
        pass
    def get_parentmeta_routing_info(self):
        return None,""
    def clear_state(self):
        pass
    def get_parentdata_routing_info(self):
        return None,""


