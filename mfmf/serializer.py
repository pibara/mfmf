#!/usr/bin/python
import json

class JsonSerializer:
    def mimetype(self):
        return "application/javascript"
    def ext(self):
        return "json"
    def __call__(self,meta):
       return json.dumps(meta) 
    
