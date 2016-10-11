#!/usr/bin/python3
from redis import StrictRedis
from json import dumps, loads
from tkinter import Tk, Frame, Label
from random import randint
from redisClient import Gl

h1 = ("Arial",20)
h2 = ("Arial",15)

#redis = StrictRedis(host='192.168.4.141',  port=6379, password='linux', db=0)

#redis = StrictRedis(host='localhost',  port=6379, db=0)
redis = Gl.getRedisLog()
exp_time = 60*60

class Session:
    def __init__(self, redis, areset = True):
        self.redis = redis
        if areset:
            self.iplist = []
            self.flushAllIP()
        self.updateIPList()

    def setKey(self, key, value):
        self.redis.setex(key, exp_time, dumps(value))
        
    def getKey(self, key):
        get = self.redis.get(key)
        if get is not None:
            return loads(get.decode("utf-8"))
        return None
    def delKey(self, key):
        self.redis.setex(key,1,"")
    def updateIPList(self):
        self.iplist=self.getKey("iplist")
        self.iplist=list(set(self.iplist))
        #for klic in self.iplist:
        #    print(self.getKey(klic))
        return self.iplist
    
    def flushAllIP(self):
        for klic in self.iplist:
            delKey(klic)
        self.iplist = []
        self.setKey("iplist", self.iplist)

class App:
    def __init__(self,app,o,w,h):
        self.title = app[0]
        self.key = app[1]
        self.o = o
        self.center = w/2
        self.width = w-100
        self.height = h
        self.f = Frame(height=h, width=w, bg="white")
        self.f.pack(padx = 200, pady = 5, side="left")
        Label(self.f,text = self.title, font=h1, bg="#acc").pack(fill="x")
        self.pLabel = []
        for i in range(5):
            self.pLabel.append(Label(self.f,text="%i. Neznámý žák"%(i+1),font=h2, bg="white"))
            self.pLabel[i].pack(anchor="w")
        Label(self.f,text = "Soutěž učeben",font=h1).pack()
        self.pu1 = Label(self.f, text = "PU1: 0", font=h2, bg="white")
        self.pu1.pack()
        self.pu2 = Label(self.f, text = "PU2: 0", font=h2, bg="white")
        self.pu2.pack()
        self.showStudents()
                         
        
    def showStudents(self):
        zaci = []
        pu1 = []
        pu2 = []
        for i in s.iplist:
            try:
                zak = s.getKey(i)
                jmeno = zak["jmeno"][0]+" "+zak["jmeno"][1]
                body = zak[self.key]
                body.sort(reverse=True)
                if len(body)>3:
                    body=body[:3]
                b = sum(body)
                ucebna = zak["hostname"]
                if ucebna[2]=="1":
                    pu1.append(b)
                if ucebna[2]=="2":
                    pu2.append(b)
                zaci.append((jmeno,b))
                zaci = sorted(zaci, key=lambda student: student[1], reverse=True)
            except:
                pass
        for i in range(5):
            if i<len(zaci):
                self.pLabel[i].config(text=str(i+1)+". "+zaci[i][0]+"("+str(round(zaci[i][1],2))+")")

        try:
            self.pu1.config(text = "PU1: "+str(round(sum(pu1)/len(pu1))))
            self.pu2.config(text = "PU2: "+str(round(sum(pu2)/len(pu2))))
        except:
            self.pu1.config(text = "PU1: -")
            self.pu2.config(text = "PU2: -")

            
        
    def update(self):
        self.showStudents()
         
        
     
        
class Prezenter:
    """Třída pro práci s projektorem"""
    def __init__(self,apps):
        self.apps=apps
        self.count = len(apps)
        pad = 3
        self.o = Tk()
        self.o.configure(background='white')
        self.width = self.o.winfo_screenwidth()
        self.height = self.o.winfo_screenheight() 
        self._geom='200x200+0+0'
        self.o.geometry("{0}x{1}+0+0".format(self.width-pad, self.height-pad))
        self.o.bind('<Escape>',self.toggle_geom)
        self.appPointers = []
        for app in apps:
            self.appPointers.append(App(app,self.o,self.width/self.count,self.height*0.7))
        self.o.after(1000, self.news)
        self.o.mainloop()
    def toggle_geom(self,event):
        geom=self.o.winfo_geometry()
        self.o.geometry(self._geom)
        self._geom=geom
    
    def news(self):
        s.updateIPList()
        for app in self.appPointers:
            app.update()
        self.o.after(5000, self.news)
    
s = Session(redis, True)

o = Prezenter([["Je to krychle?","krychle"],["Matematico","matematico"]])



