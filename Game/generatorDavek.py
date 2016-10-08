#Generátor dávek pro PY
from random import randint
from json import dumps
def cistaDavka():
    a = []
    for i in range(1,14):
        for j in range(4):
            a.append(i)
    return a
def generuj(pocet, cas):
    print("Generuji %i dávek s časem %i na tah"%(pocet,cas))
    komplet = []
    for i in range(pocet):
        d = cistaDavka()
        nd = [cas]
        for j in range(25):
            nd.append(d.pop(randint(0,len(d)-1)))
        komplet.append(nd)
    return komplet
        

print("Vytvářím soubor data.json. \nPokud soubor existoval, jeho obsah bude smazán \nPokud tento soubor bude ve stejné složce jako matematico.py, bodou hry načítány z něj.")
soubor = open("data.json","wb")
print("Soubor vytvořen.")
pocet = int(input("Počet dávek, které mají být vytvořeny:"))
if (input("Všechny dávky mají stejný čas na tah? (y/n):"))=="y":
    cas = int(input("Jaký čas v s (1-15):"))
    ret = generuj(pocet,cas)
else:
    ad = 0
    md = 1
    ret = []
    while md<pocet:
        kolik = int(input("Pro dávku %i až:"%(ad)))
        cas = int(input("platí čas:"))
        md = kolik
        pc = md-ad
        ret.extend(generuj(pc,cas))
        ad+=pc
print("Zapisuji dávky do souboru ...")
print(dumps(ret))
soubor.write(bytes(dumps(ret),"UTF-8"))
print("Zápis proběhl v pořádku. Já se loučím.")
soubor.close()
