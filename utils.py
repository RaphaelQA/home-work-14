import collections
import json
import sqlite3

from flask import jsonify


def get_result(query):
    with sqlite3.connect("netflix.db") as con:
        con.row_factory = sqlite3.Row
        result = []

        for item in con.execute(query).fetchall():
            s = dict(item)

            result.append(s)

        return result


def get_one(query):
    with sqlite3.connect("netflix.db") as con:
        con.row_factory = sqlite3.Row
        result = dict(con.execute(query).fetchone())

        return result


def response_actors(name1: str = 'Jack Black', name2: str = 'Dustin Hoffman'):
    query = f"""
            SELECT * FROM netflix
            WHERE "cast" LIKE '%{name1}%' AND"cast" LIKE '%{name2}%' 
            """

    actors = []
    actors_1 = []
    actor = []
    result = get_result(query)
    for i in result:
        actors.append(i['cast'])
        x = ", ".join(actors)
        y = x.split(",")
    for g in y:
        actors_1.append(g.strip(" "))

    o = [item for item, count in collections.Counter(actors_1).items() if count > 2]

    for i in o:
        if i == name1:
            continue
        elif i == name2:
            continue
        else:
            actor.append(i)
    return actor

def search_content(type, release_year, listed_in):
    query = f"""
                SELECT title, release_year, listed_in FROM netflix
                WHERE type LIKE "%{type}%" AND release_year = "{release_year}"
                AND listed_in LIKE "%{listed_in}%"
                """

    result = []
    for i in get_result(query):
        result.append(
            {
                "title": i['title'],
                "release_year": i['release_year'],
                "listed_in": i['listed_in'],
             }
        )
    o = json.dumps(result)
    return o

print(search_content("Movie", 2016, "Dramas"))


