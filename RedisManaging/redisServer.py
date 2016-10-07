from redis import StrictRedis
from json import dumps, loads
from tkinter import Tk
from random import randint

redis = StrictRedis(host='192.168.4.141',  port=6379, password='linux', db=0)

class Session:
    def __init__(self,redis):
        self.redis = redis
        iplist = []
        self.flushAllIP()
        self.updateIPList()
        
        
    def setKey(self,key,value):
        self.redis.setex(key, 60*60, dumps(value))
        
    def getKey(self,key):
        get = self.redis.get(key)
        if not get is None:
            return loads(get.decode("utf-8"))
        return None
    
    def updateIPList(self):
        self.iplist=self.getKey("iplist")
        self.iplist=list(set(self.iplist))
        for klic in self.iplist:
            print(self.getKey(klic))
        return self.iplist
    
    def flushAllIP(self):
        iplist = []
        self.setKey("iplist",iplist)

def news():
    print(s.updateIPList())
    o.after(1000,news)
    
s = Session(redis)

o = Tk()
o.after(1000,news)
o.mainloop()

