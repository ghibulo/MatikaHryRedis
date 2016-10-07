from redis import StrictRedis
redis = StrictRedis(host='192.168.4.141',  port=6379, password='linux', db=0)


redis.setex("comp1", 60*30, '{"app": "test", "name": "Michal Voráček", "score":50}')
print(redis.get("comp1"))
