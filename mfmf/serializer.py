#!/usr/bin/python
import json

class JsonSerializer:
    def __call__(self,meta):
       return json.dumps(meta) 

