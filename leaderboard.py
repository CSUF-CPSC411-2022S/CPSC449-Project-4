# leaderboard: hypercorn leaderboard --reload --debug --bind leaderboard.local.gd:$PORT --access-logfile - --error-logfile - --log-level DEBUG
# primary: ./bin/litefs -config ./etc/primary.yml
# secondary1: ./bin/litefs -config ./etc/secondary1.yml
# secondary2: ./bin/litefs -config ./etc/secondary2.yml
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

from quart import Quart, g, request, abort
from quart_schema import QuartSchema, RequestSchemaValidationError, validate_request

app = Quart(__name__)
QuartSchema(app)


async def _connect_db():
    database = databases.Database(app.config["DATABASES"]["URL"])
    await database.connect()
    return database

def _get_db():
    if not hasattr(g, "sqlite_db"):
        g.sqlite_db = _connect_db()
    return g.sqlite_db


@dataclasses.dataclass
class results:
    score: str
    result: str


@app.teardown_appcontext
async def close_connection(exception):
    db = getattr(g, "_sqlite_db", None)
    if db is not None:
        await db.disconnect()

@app.route("/results", methods=["POST"])
async def results(data):
    db = await _get_db()
    game = dataclasses.asdict(data)
    r = redis.Redis(db=0)
    r.mset({"Result" : game.get("result"), "Score": game.get("score")})


@app.route("/top10", methods=["GET"])
async def top10():
    db = await _get_db()
    r = redis.Redis()
    leaderboard = r.get("top10")
