# -*- coding: utf-8 -*-
import redis
class redis_db(object):
    def __init__(self,redis_data):
        self.redis_connect=redis.Redis(host='localhost',port='6379',db=1)
        self.redis_data=redis_data
    def redis_insert(self):
        if (self.redis_connect.exists(self.redis_data)):
            return False
        else:
            self.redis_connect.set(self.redis_data,"1")
            return True
    def redis_delete(self):
        if (self.redis_connect.exists(self.redis_data)):
            self.redis_connect.delete(self.redis_data)

