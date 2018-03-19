#!/usr/bin/python
import json
import mattock.api
from time import sleep
from mattock import carvpath
from router import TrivialRouter
from serializer import JsonSerializer
from throttler import DummyThrottler
from treewalker import TrivialTreeWalker
from mattock.api import MountPoint

#This class is meant for binding together the low level MattockFS language bindings with higher level
#module framework components and the actual module that uses a higher level API. The EventLoop will
#poll all of the active CarvPath mounts and will comunicate with appropriate user supplied framework
#components in order to allow modules using such a module frameworj to process incomming jobs using a
#higher level API.
class EventLoop:
    def __init__(self,modname, module, router=TrivialRouter(), serializer=JsonSerializer(), throttler=DummyThrottler(), treewalker=TrivialTreeWalker(), initial_policy=None):
        treewalker.set_module(module)
        jsonfile = "/etc/mattockfs.json"
        self.count = 0
        with open(jsonfile,"r") as f:
            jsondata = f.read()
            data = json.loads(jsondata)
            self.count=data["instance_count"]
        self.mountpoints = []
        self.workers = []
        for mpno in range(0,self.count):
            mppath = "/var/mattock/mnt/" + str(mpno)
            self.mountpoints.append(MountPoint(mppath))
        for mp in self.mountpoints:
            self.workers.append(mp.register_worker(modname,initial_policy))
        self.router = router
        self.serializer = serializer
        self.throttler = throttler
        self.treewalker = treewalker
        self.throttler.set_global_functors(self._fadvise_status,self._anycast_status)
    def _fadvise_status(self):
        dontneed = 0
        normal = 0
        for mp in self.mountpoints:
            obj = mp.fadvise_status()
            dontneed = dontneed + obj["dontneed"]
            normal = normal + obj["normal"]
        return  {"normal": normal, "dontneed": dontneed}
    def _anycast_status(self, actorname):
        setsize = 0
        setvolume = 0
        for mp in self.mountpoints:
            obj = mp.anycast_status(actorname)
            setsize = setsize + obj["set_size"]
            setvolume = setvolume + obj["set_volume"]
        return  {"set_size": setsize, "set_volume": setvolume}
    def _get_job(self):
        sleepcount = 0 
        while True:
            for index in  range(0,self.count):
                worker=self.workers[index]
                job = worker.poll_job()
                if job is None:
                    sleepcount = sleepcount + 1
                else:
                    sleepcount = 0
                    yield job,worker
                if sleepcount == self.count:
                    sleep(0.05)           
    def _child_submit(self,job,carvpath,meta):
        data_nexthop,data_routerstate,data_mimetype,data_ext,meta_nexthop,meta_routerstate=self.router.process_child_meta(meta)
        if meta_nexthop != None:
            self.throttler.on_anycast(meta_nexthop)
            metablob = self.serializer(meta)
            mutable = job.childdata(len(metablob))
            with open(mutable, "r+") as f:
                f.seek(0)
                f.write(metablob)
            meta_carvpath = job.frozen_childdata()
            job.childsubmit(carvpath=meta_carvpath,
                        nextactor=meta_nexthop,
                        routerstate=meta_routerstate,
                        mimetype=self.serializer.mimetype(),
                        extension=self.serializer.ext())
        if data_nexthop != None:
            self.throttler.on_anycast(data_nexthop)
            job.childsubmit(carvpath=carvpath,
                        nextactor=data_nexthop,
                        routerstate=data_routerstate,
                        mimetype=data_mimetype(),
                        extension=data_ext())
    def _allocate_storage(self,size):
        self.throttler.on_alloc(size)
        return self.job.childdata(size)
    def __call__(self):
        for job,worker in self._get_job():
            self.job=job
            self.throttler.set_worker(worker)
            self.router.set_state(job.router_state)
            toplevel_meta = self.treewalker.walk(job.carvpath,self.router.get_walk_argument(),self._child_submit,self._allocate_storage,job)
            self.router.process_parent_meta(toplevel_meta)
            meta_module,meta_router_state = self.router.get_parentmeta_routing_info()
            if meta_module != None:
                metablob = self.serializer(toplevel_meta)
                mutable = job.childdata(len(metablob))
                with open(mutable, "r+") as f:
                    f.seek(0)
                    f.write(metablob)
                meta_carvpath = job.frozen_childdata()
                job.childsubmit(carvpath=meta_carvpath,
                            nextactor=meta_module,
                            routerstate=meta_router_state,
                            mimetype=self.serializer.mimetype(),
                            extension=self.serializer.ext())
            data_module,data_router_state = self.router.get_parentdata_routing_info()
            if data_module == None:
                job.done()
            else:
                job.forward(data_module,data_router_state)
            self.router.clear_state()         

def run(module):
    name=module.name()
    el=EventLoop(name,module)
    el()
