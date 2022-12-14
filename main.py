from flask import Flask, jsonify

from utils import get_result, get_one

app = Flask(__name__)


@app.get('/movie/<title>')
def get_movie_by_title(title):
    query = f"""
        SELECT * FROM netflix 
        WHERE title = "{title}"
        ORDER BY date_added DESC
    """

    query_result = get_one(query)

    movie = {
        "title": query_result['title'],
        "country": query_result['country'],
        "release_year": query_result['release_year'],
        "genre": query_result['listed_in'],
        "description": query_result['description'],
    }

    return jsonify(movie)


@app.get('/movie/<year1>/to/<year2>')
def get_movie_data(year1, year2):
    query = f"""
            SELECT * FROM netflix 
            WHERE release_year BETWEEN {year1} AND {year2}
            LIMIT 100
        """
    result = []

    for item in get_result(query):
        result.append(
            {
                "title": item['title'],
                "release_year": item['release_year'],
            }
        )
    return jsonify(result)


@app.get('/movie/rating/<value>')
def get_movie_by_rating(value):
    query = """
    SELECT * FROM netflix
    """

    if value == 'children':
        query += "WHERE rating = 'G'"
    elif value == 'family':
        query += "WHERE rating = 'G' or rating = 'PG' or rating = 'PG-13'"
    elif value == 'adult':
        query += "WHERE rating = 'R' or rating = 'NC-17'"
    else:
        return jsonify(error=404)

    result = []

    for item in get_result(query):
        result.append(
            {
                "title": item['title'],
                "rating": item['rating'],
                "description": item['description'],
            }
        )
    return jsonify(result)


@app.get('/genre/<genre>')
def get_movie_by_genre(genre):
    query = f"""
            SELECT * FROM netflix 
            WHERE listed_in LIKE "%{genre}%"
            ORDER BY date_added DESC
            LIMIT 10
        """

    result = []

    for item in get_result(query):
        result.append(
            {
                "title": item['title'],
                "rating": item['rating'],
                "description": item['description'],
            }
        )
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
