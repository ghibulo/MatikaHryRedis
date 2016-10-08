from redis import StrictRedis
import socket
import json


exp_time = 60*60

#redis = StrictRedis(host='192.168.4.141',  port=6379, password='linux', db=0)


#redis.setex("comp1", exp_time, '{"app": "test", "name": "Michal Voráček", "score":50}')
#redis.setex("comp1", exp_time, 'nejhorší operační systém')

class RedisClient:
    def __init__(self, ahost, apassw, aport=6379):
        self.client_key = json.dumps(socket.gethostbyname(socket.gethostname()))
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
        
    def send_data(self, akey, aval):
        my_values = self.redis.get(self.client_key)
        self.client_values = {} if my_values is None else json.loads(my_values.decode('utf-8'))
        self.client_values[akey] = aval
        self.redis.setex(self.client_key, exp_time, json.dumps(self.client_values))




#rc = RedisClient('192.168.4.141', 'linux', 6379 )
if __name__ == "__main__":
    rc = RedisClient('localhost', None, 6379)
    rc.add_myself()
    rc.send_data("skore", 50)




    
    
    


