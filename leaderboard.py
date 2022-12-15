from cmath import exp
from pydoc import doc
import databases
import collections
import dataclasses
import sqlite3
import textwrap
import uuid
import databases
import toml
import redis
import os
import socket
import httpx
import json
from time import sleep

from quart import Quart, g, request, abort
from quart_schema import QuartSchema, RequestSchemaValidationError, validate_request

app = Quart(__name__)
QuartSchema(app)

result = None
counter = 0
time = 0
while result is None:
    try:
        game_URL = socket.getfqdn("127.0.0.1:5400")
        result = httpx.get("http://"+game_URL)
    except httpx.RequestError:
        time.sleep(5.0)
        time += 5
        counter += 1
        print("Waiting for game service, alloted time: ", time, " seconds\n")

@dataclasses.dataclass
class Results:
    username: str
    game_id: str
    guesses: int
    result: str

# Ideas:
#     Make 2 databases:
#         (db=0) for "game_id", {result: guesses},
#         (db=1) for "users", {username: score}
#
#     db=0 will be for tracking results of games+guesses of a certain user (game_id is UNIQUE)
#     db=1 will be for calling top 10 of ALL users
#
#     Might need 2 redis connections





@app.route("/results", methods=["POST"])
@validate_request(Results)
async def results(data):
    result = dataclasses.asdict(data)
    r = redis.Redis(db=0, charset="utf-8", decode_responses=True)
    r2 = redis.Redis(db=1, charset="utf-8", decode_responses=True)
    username = result.get("username")
    game_id = result.get("game_id")
    res = result.get("result")
    guesses = result.get("guesses")

    score = 0
    if guesses <= 0 or guesses > 6:
        return {"Error" : "Invalid number of guesses"}, 400
    if guesses == 1 and res == 'W' or res == 'w':
        score = 6
    elif guesses == 2 and res == 'W' or res == 'w':
        score = 5
    elif guesses == 3 and res == 'W' or res == 'w':
        score = 4
    elif guesses == 4 and res == 'W' or res == 'w':
        score = 3
    elif guesses == 5 and res == 'W' or res == 'w':
        score = 2
    elif guesses == 6 and res == 'W' or res == 'w':
        score = 1

    try:
        r.zadd(game_id, {res: guesses}, nx=True)
        check_user_exists = r2.zrange("users", 0, -1, withscores=True)
        for i in range(len(check_user_exists)):
            if check_user_exists[i][0] == username:
                r2.zadd("users", {username: score}, incr=True)
                print(r2.zrange("users", 0, -1, withscores=True))
                return { username : "score has increased by " + str(score) }, 200
        r2.zadd("users", {username: score}, nx=True)
        return { username : "has been added to the leaderboard with a score of " + str(score) }, 200

    except:
        return {"Error" : "Could not add results to redis"}, 400


# @app.route("/test/<string:username>", methods=["GET"])
# async def pop(username):
#     # r = redis.Redis()
#     redi = redis.StrictRedis(host='localhost', port=6379,db=0, charset="utf-8", decode_responses=True)
#     user = username
#     # keys = redi.keys('*')
#     # for key in keys:
#     #     print("key being checked", key)
#     #     type = redi.type(key)
#     #     if type == "string":
#     #         vals = redi.get(key)
#     #         print("string", vals)
#     #     if type == "hash":
#     #         vals = redi.hgetall(key)
#     #         print("hash", vals)
#     #     if type == "zset":
#     #         vals = redi.zrange(key, 0, -1, withscores=True)
#     #         print("zset", vals)
#     #     if type == "list":
#     #         vals = redi.lrange(key, 0, -1)
#     #         print("list", vals)
#     #     if type == "set":
#     #         vals = redi.smembers(key)
#     #         print("set", vals)
#     # zkey = 'test'
#     # dict = {}
#     # dict['15648-barry'] = 15648
#     # redis.zadd(zkey,dict)
#     # user = "username"
#     # data = "hello world"
#     # score = 12
#     # redisClient.zadd("KEY", {data: score})
#     # for i in range(0, 9):
#     #     score = i
#     #     result = 'W'
#     #     r.zadd({"Player "+str(i), {score, result}})
#
#     return "hallo"

@app.route("/top10", methods=["GET"])
async def top10():
    r = redis.Redis(db=1, charset="utf-8", decode_responses=True)
    leaderboard = r.zrevrange("users", 0, 9, withscores=True)
    return leaderboard
