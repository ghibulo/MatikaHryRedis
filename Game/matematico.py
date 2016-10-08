#!/usr/bin/python3
from tkinter import Tk, Canvas
from random import randint
from json import loads

ODPOCET = 1
body = 0

#Zkouším otevřít soubor s dávkama
davky = []
infoBody = []
cisloDavky = 0
try:
    davky = loads(open("data.json", 'rb').read().decode('UTF-8'))
except:
    pass

def nahodnaDavka():
    cisla = []
    for i in range(1,14):
        for j in range(4):
            cisla.append(i)
    d = [ODPOCET]
    for i in range(25):
        d.append(cisla.pop(randint(0,len(cisla)-1)))
    return d
    
def naberDavku():
    global cisloDavky
    if cisloDavky==len(davky):
        d = nahodnaDavka()
        c.itemconfig(infoDavka,text="Náhodná hra")
    else:
        d = davky[cisloDavky]
        cisloDavky += 1
        c.itemconfig(infoDavka,text="Dávka %i z %i"%(cisloDavky,len(davky)))
    return d
    


class Ctverec:
    def __init__(self,i,j):
        self.surface = c.create_rectangle(i*100,j*100,(i+1)*100,(j+1)*100,fill="white")
        self.text = c.create_text(i*100+50,j*100+50,text="",anchor="c",font=("Serif","50"))
        self.num = 0
    def insert(self,num):
        if self.num == 0:
            self.num = num
            c.itemconfig(self.text,text=str(num))
            c.itemconfig(aktivniCislo,text="")
            return True
        return False
    def reset(self):
        self.num = 0
        c.itemconfig(self.text,text="")

def spocti(*args):
    l = list(args)
    b = 0
    l=list(filter(lambda a: a != 0, l))
    if len(l)<2:
        return 0
    #Vyhodnocení dvojiček a trojiček
    dvojky = 0
    trojky = 0
    for i in range(1,14):
        if l.count(i)==2:
            dvojky+=1
        if l.count(i)==3:
            trojky+=1
        if l.count(i)==4:
            b+=4
    if dvojky==1 and trojky==1:
        b+=5
    elif trojky==1:
        b+=2
    elif dvojky==2:
        b+=3
    elif dvojky==1:
        b+=1
    #Vyhodnocení nejdelší postupky
    l=list(set(l))
    l.sort()
    apostupka = 1
    maxpostupka = 0
    posledni = l[0]
    for i in l:
        if i==posledni+1:
            apostupka+=1
        else:
            if apostupka>maxpostupka:
                maxpostupka=apostupka
            apostupka = 1
        posledni = i
    if apostupka>maxpostupka:
        maxpostupka=apostupka
    if maxpostupka==3:
        b+=1
    if maxpostupka==4:
        b+=3
    if maxpostupka==5:
        b+=6    
    print(list(args),"\tnejdelsi>",maxpostupka,"\tdvojicky>",dvojky,"\ttrojicky>",trojky,"\tbody",b)
    return b
def naboduj(ab):
    global hraje
    ab+=1
    c.itemconfig(aktivniCislo,text=str(ab))
    if ab<body:
        o.after(ab*10+100,lambda a=ab:naboduj(a))
    else:
        c.itemconfig(aktivniCislo,fill="green")
        hraje = False
                 

def vyhodnot():
    global konec,body,infoBody
    konec = True
    body = 0
    for i in range(5):
        b=spocti(ctverce[i][0].num,ctverce[i][1].num,ctverce[i][2].num,ctverce[i][3].num,ctverce[i][4].num)
        infoBody.append(c.create_text(i*100+50,490,text=str(b),fill="green"))
        body+=b
        b=spocti(ctverce[0][i].num,ctverce[1][i].num,ctverce[2][i].num,ctverce[3][i].num,ctverce[4][i].num)
        infoBody.append(c.create_text(490,i*100+50,text=str(b),fill="green"))
        body+=b
    b=spocti(ctverce[0][0].num,ctverce[1][1].num,ctverce[2][2].num,ctverce[3][3].num,ctverce[4][4].num)
    infoBody.append(c.create_text(490,490,text=str(b),fill="green"))
    body+=b
    b=spocti(ctverce[4][0].num,ctverce[3][1].num,ctverce[2][2].num,ctverce[1][3].num,ctverce[0][4].num)
    infoBody.append(c.create_text(490,10,text=str(b),fill="green"))
    body+=b
    c.itemconfig(aktivniCislo,text="0",fill="red")
    naboduj(0)
    
    
def insert(e):
    global umisteno
    if e.x in range(550,650) and e.y in range(10,50):
        novaHra()
    x = e.x//100
    y = e.y//100
    if x>4 or y>4 or not hraje:
        return None
    if not umisteno:
        umisteno = ctverce[x][y].insert(cislo)
def vyberCislo():
    return davka.pop(0)
def upravCaru():
    global cas,cislo,umisteno
    cas-=0.1
    if cas<0:
        if len(davka)>0:
            cas=ODPOCET
            cislo = vyberCislo()
            umisteno = False
            c.itemconfig(aktivniCislo,text=str(cislo))
        else:
            vyhodnot()  
    c.coords(cara,550,450,550+100*cas/ODPOCET,480)
    if not konec:
        c.after(100,upravCaru)
def novaHra():
    global hraje,davka,ODPOCET,cislo,cas,infoBody,umisteno,konec
    if hraje:
        return False
    hraje = True
    konec = False
    umisteno = False
    if len(infoBody)>0:
        for i in infoBody:
            c.delete(i)
    infoBody = []
    for i in range(5):
        for j in range(5):
            ctverce[i][j].reset()
            
    davka = naberDavku()
    ODPOCET = davka.pop(0)
    cas = ODPOCET
    cislo = vyberCislo()
    c.itemconfig(aktivniCislo,text=str(cislo))
    c.itemconfig(aktivniCislo,fill="black")
    c.after(100,upravCaru)
    

o = Tk()
c = Canvas(o,width=700,height=500);
c.pack()
ctverce = []
cas = ODPOCET
konec = False
umisteno = False
hraje = False
for i in range(5):
    ctverce.append([])
    for j in range(5):
        ctverce[i].append(Ctverec(i,j))



cislo = 0
aktivniCislo = c.create_text(600,250,text="",font=("Serif","100"))
cara = c.create_rectangle(550,450,650,470,fill="black")
infoDavka = c.create_text(600,70,text = "Spusť hru")
c.create_rectangle(550,10,650,50,fill="#aaf")
c.create_text(600,30,text="Nová hra")
#for i in range(5):
#    for j in range(5):
#        ctverce[i][j].insert(vyberCislo())
#vyhodnot()

c.bind("<Button>",insert)
#c.after(100,upravCaru)
o.mainloop()
