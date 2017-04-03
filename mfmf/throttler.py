#!/usr/bin/python
class DummyThrottler:
    def set_global_functors(self,fadvise_status,anycast_status):
        self.fadvise_status = fadvise_status
        self.anycast_status = anycast_status
    def on_anycast(self,meta_nexthop):
        pass
    def on_alloc(self,size):
        pass
    def set_worker(self,worker):
        pass

