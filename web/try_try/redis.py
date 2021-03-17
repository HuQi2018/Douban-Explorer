import redis
from django.shortcuts import HttpResponse
from utils.redis_pool import POOL

def index(request):
    conn = redis.Redis(connection_pool=POOL)
    conn.hset('kkk','age',18)

    return HttpResponse('设置成功')
def order(request):
    conn = redis.Redis(connection_pool=POOL)
    data = conn.hget('kkk','age')
    # print(data)
    return HttpResponse('获取成功'+str(data, encoding = "utf-8"))

def redis_save(key,data):
    conn = redis.Redis(connection_pool=POOL)
    if data: #有数据表示存储
        conn.set(key, data)
        conn.expire(key, 60*60*24)#存储24小时
    else:  #无有数据表示提数据
        data = conn.get(key)
        return data