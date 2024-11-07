import sqlite3

from flask import g

DATABASE = "database.db"


def get_db():
    db = getattr(g, "_database", None)

    if db is None:
        db = g._database = sqlite3.connect(DATABASE)

    return db


def query_db(query, args=(), one=False):
    db = get_db()
    cur = db.execute(query, args)
    rv = cur.fetchall()
    cur.close()
    db.commit()

    return (rv[0] if rv else None) if one else rv


def init_db():
    db = sqlite3.connect(DATABASE)

    with open("schema.sql", "r") as f:
        db.cursor().executescript(f.read())

    db.commit()
