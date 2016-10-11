from redis import StrictRedis
import socket
import json
from tkinter import *


class Gl:
    exp_time = 60*60
    indRed = 'b307'
    redis_parameters = {'local': ('localhost', None),
                        'skola': ('192.168.4.141', 'linux'),
                        'b307': ('192.168.3.137', 'linux')}
    @staticmethod
    def getRedisLog(key=indRed):
        pas = Gl.redis_parameters[key][1] 
        if pas is None:
            return StrictRedis(host=Gl.redis_parameters[key][0], port=6379)
        else:
            return StrictRedis(host=Gl.redis_parameters[key][0], port=6379, password=pas)


#redis = StrictRedis(host='192.168.4.141',  port=6379, password='linux', db=0)


#redis.setex("comp1", exp_time, '{"app": "test", "name": "Michal Voráček", "score":50}')
#redis.setex("comp1", exp_time, 'nejhorší operační systém')



class RedisClient:
    def __init__(self, ahost, apassw, aport=6379):
        self.client_key = json.dumps(socket.gethostbyname(socket.gethostname()))+json.dumps(socket.gethostname())
        self.client_values = ""
        if apassw is None:
            self.redis = StrictRedis(host=ahost,  port=aport,  db=0)
        else:
            self.redis = StrictRedis(host=ahost,  port=aport, password=apassw, db=0)

    def add_myself(self):
        s = self.redis.get("iplist")
        ips = "[]" if s is None else s.decode("utf-8")
        iplist = json.loads(ips)
        if self.client_key not in iplist:
            iplist.append(self.client_key)
            self.redis.setex("iplist", 60*60, json.dumps(iplist))

    def am_I_added(self):
        s = self.redis.get("iplist")
        ips = "[]" if s is None else s.decode("utf-8")
        iplist = json.loads(ips)
        return self.client_key in iplist

    def send_data(self, akey, aval):
        """
        :param akey: klic, pod ktery chce  klient zapisovat
        :param aval: hodnota, ktera nahradi puvodni hodnotu
        :return:
        """
        my_values = self.redis.get(self.client_key)
        self.client_values = {} if my_values is None else json.loads(my_values.decode('utf-8'))
        self.client_values[akey] = aval
        self.redis.setex(self.client_key, Gl.exp_time, json.dumps(self.client_values))


    def get_data(self, akey):
        """
        :param akey: klic jehoz data klient potrebuje
        :return: kdyz klic existuje, vrati hodnotu, jinak None
        """
        my_values = self.redis.get(self.client_key)
        self.client_values = {} if my_values is None else json.loads(my_values.decode('utf-8'))
        return self.client_values.get(akey, None)


    def add_data(self, akey, aval):
        """
        :param akey: klic, pod ktery chce  klient zapisovat
        :param aval: hodnota, ktera se prida k puvodnim hodnotam ulozenym v 'list'
        :return:
        """
        d = self.get_data(akey)
        if d is None:
            vykony = []
        else:
            vykony = d
        vykony.append(aval)
        self.send_data(akey, vykony)



class Identity:
    """
    - Zepta se na jmeno
    - zapise svuj klic do seznamu 'iplist'
    - zapise sve jmeno do hodnot pod svym klicem
    """
    def __init__(self, parent):
        # user closed window
        self.closed_window = True
        # get redis
        self.redis_ok = True
        try:
            self.redis = RedisClient(Gl.redis_parameters[Gl.indRed][0], Gl.redis_parameters[Gl.indRed][1])
        except:
            self.redis_ok = False

        print("1: "+str(self.redis_ok))


        # hide main window
        self.parent = parent
        parent.withdraw()

        wind = self.top = Toplevel(parent)
        wind.focus_set()
        wind.attributes("-topmost", True)
        wind.title("Identifikace")
        wind.geometry('%dx%d+%d+%d' % (400, 150, 100, 200))
        self.name, self.surname = None, None
        self.myLabel = Label(wind, text='Jméno:')
        self.myLabel.pack()
        self.EntryN = Entry(wind)
        try:
            if self.redis.am_I_added():
                nm = self.redis.get_data("jmeno")
                self.redis_ok = True
                if nm is not None:
                    self.name, self.surname = nm
                    self.EntryN.insert(END, self.name)
        except:
            self.redis_ok = False

        print("2: "+str(self.redis_ok))
        self.EntryN.pack()
        self.myLabel = Label(wind, text='Přijímení:')
        self.myLabel.pack()
        self.EntryS = Entry(wind)
        if self.surname is not None:
            self.EntryS.insert(END, self.surname)
        self.EntryS.pack()
        self.SubmitButton = Button(wind, text='Začneme?', command=self.send)
        self.SubmitButton.pack()

    def send(self):
        self.name = self.EntryN.get()
        self.surname = self.EntryS.get()
        try:
            self.redis.add_myself()
        except:
            self.redis_ok = False

        print("3: "+str(self.redis_ok))
        try:
            self.redis.send_data("jmeno", [self.name, self.surname])
        except:
            self.redis_ok = False

        print("4: "+str(self.redis_ok))
        try:
            self.redis.send_data("hostname", socket.gethostname())
        except:
            self.redis_ok = False
        print("5: "+str(self.redis_ok))
        self.closed_window = False
        self.top.destroy()
        # unhide parent again
        self.parent.deiconify()







    
    
    


