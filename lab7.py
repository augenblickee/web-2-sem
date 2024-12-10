from flask import Blueprint, render_template, abort, request, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3
from os import path

lab7 = Blueprint('lab7', __name__)

def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host='::1',
            database='osyagin_ivan_knowledge_base',
            user='osyagin_ivan_knowledge_base',
            password='KAKASHKI123'
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, 'database.db')
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
    return conn, cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

@lab7.route('/lab7/')
def lab():
    return render_template('/lab7/lab7.html')

@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    conn, cur = db_connect()
    cur.execute("SELECT * FROM films ORDER BY id")
    films = cur.fetchall()
    db_close(conn, cur)
    return films

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    conn, cur = db_connect()
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM films WHERE id = %s", (id,))
    else:
        cur.execute("SELECT * FROM films WHERE id = ?", (id,))
    film = cur.fetchone()
    db_close(conn, cur)
    if not film:
        return abort(404)
    return film

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    conn, cur = db_connect()
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("DELETE FROM films WHERE id = %s RETURNING id", (id,))
    else:
        cur.execute("DELETE FROM films WHERE id = ? RETURNING id", (id,))
    deleted = cur.fetchone()
    db_close(conn, cur)
    if not deleted:
        return abort(404)
    return '', 204

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    film = request.get_json()
    if not film or not all(k in film for k in ('title', 'title_ru', 'year', 'description')):
        return {'description': 'Некорректные данные'}, 400
    
    if not film['title_ru'] and not film['title']:
            return {'description': 'Напишите название'}, 400
    elif not film['title_ru']:
        return {'description': 'Напишите русское название'}, 400
    elif not (2024 >= int(film['year']) >= 1895) or film['year'] == '':
        return {'description': 'Дата введена некорректно'}, 400
    elif film['description'] == '':
        return {'description': 'Заполните описание'}, 400
    elif len(film['description']) > 2000:
        return {'description': 'Максимальная длинна описания - 2000 символов'}, 400
    if film['title_ru'] and not film['title']:
        film['title'] = film['title_ru']

    conn, cur = db_connect()
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute(
            """
            UPDATE films SET title = %s, title_ru = %s, year = %s, description = %s
            WHERE id = %s RETURNING id
            """,
            (film['title'], film['title_ru'], film['year'], film['description'], id)
        )
    else:
        cur.execute(
            """
            UPDATE films SET title = ?, title_ru = ?, year = ?, description = ?
            WHERE id = ? RETURNING id
            """,
            (film['title'], film['title_ru'], film['year'], film['description'], id)
        )
    updated = cur.fetchone()
    db_close(conn, cur)
    if not updated:
        return abort(404)
    return film

@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    film = request.get_json()
    if not film or not all(k in film for k in ('title', 'title_ru', 'year', 'description')):
        return {'description': 'Некорректные данные'}, 400
    
    if not film['title_ru'] and not film['title']:
        return {'description': 'Напишите название'}, 400
    elif not film['title_ru']:
        return {'description': 'Напишите русское название'}, 400
    elif not (2024 >= int(film['year']) >= 1895) or film['year'] == '':
        return {'description': 'Дата введена некорректно'}, 400
    elif film['description'] == '':
        return {'description': 'Заполните описание'}, 400
    elif len(film['description']) > 2000:
        return {'description': 'Максимальная длинна описания - 2000 символов'}, 400
    
    if film['title_ru'] and not film['title']:
        film['title'] = film['title_ru']
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute(
            """
            INSERT INTO films (title, title_ru, year, description)
            VALUES (%s, %s, %s, %s) RETURNING id
            """,
            (film['title'], film['title_ru'], film['year'], film['description'])
        )
    else:
        cur.execute(
            """
            INSERT INTO films (title, title_ru, year, description)
            VALUES (?, ?, ?, ?) RETURNING id
            """,
            (film['title'], film['title_ru'], film['year'], film['description'])
        )
    new_id = cur.fetchone()['id']
    db_close(conn, cur)
    return {'id': new_id}, 201
