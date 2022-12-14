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

def response_actors(name1:str = 'Rose McIver', name2:str = 'Ben Lamb'):
    query = f"""
            SELECT * FROM netflix
            WHERE "cast" LIKE '%{name1}%' AND"cast" LIKE '%{name2}%' 
            """

    actors = []

    result = get_result(query)
    for item in result:
        actors.append(
            {'actor': item['cast'],}
        )
    return actors


print(response_actors())