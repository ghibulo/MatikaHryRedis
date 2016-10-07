from redis import StrictRedis
import socket
import json

#redis = StrictRedis(host='192.168.4.141',  port=6379, password='linux', db=0)


#redis.setex("comp1", 60*30, '{"app": "test", "name": "Michal Voráček", "score":50}')
#redis.setex("comp1", 60*30, 'nejhorší operační systém')

class RedisClient:
    def __init__(self, ahost, apassw, aport=6379, ex = 3600):
        self.redis=StrictRedis(host=ahost,  port=aport, password=apassw, db=0)


    def addMyself(self):
        s = self.redis.get("iplist").decode("utf-8")
        iplist = json.loads(s)
        self.mykey = json.dumps(socket.gethostbyname(socket.gethostname()))
        iplist.append(self.mykey)
        self.redis.setex("iplist", 60*60, json.dumps(iplist))
        

    def sendData(self, ke, val):
        """" dodelat zapisovani a updatovani konkretnich klicu """
        json.loads(self.redis.get(self.mykey))
        self.redis.setex(self.mykey, 60*60, json.dumps({ke:val}))




rc = RedisClient('192.168.4.141', 'linux', 6379 )
rc.addMyself()
rc.sendData("hra", "krychle")




    
    
    


