# -*- coding: utf-8 -*-
import pymongo
import time

client = pymongo.MongoClient(host='127.0.0.1', port=27017)
db = client.note
collection = db.col

def add(name, data):
    ans = find(name)
    if ans:
        ans['data'] = data
        ans['time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        objectid = collection.update({'name': name}, ans)
    else:
        clust = {'name': name, 'time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), 'data': data}
        objectid = collection.insert_one(clust)
    return objectid


def find(name):
    return collection.find_one({"name": name})


def pwd(name, password):
    condition = {'name': name}
    ans = collection.find_one(condition)
    if ans:
        ans['password'] = password
    else:
        add(name, '')
        ans = collection.find_one(condition)
        ans['password'] = password
    return collection.update(condition, ans)


def file_path(name, path):
    condition = {'name': name}
    ans = collection.find_one(condition)
    ans['path'] = path
    return collection.update(condition, ans)

if __name__ == '__main__':
    a = pwd('12412', 'dsafsa')
    print(a)
