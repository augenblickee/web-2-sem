from flask import Blueprint, render_template, abort, request, current_app, session
import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3
from os import path

rgz = Blueprint('rgz', __name__)

def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host='::1',
            database='rgz',
            user='rgz',
            password='MAMA200'
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

def rows_to_dicts(rows):
    return [dict(row) for row in rows]

@rgz.route('/rgz/')
def main():
    return render_template('/rgz/main.html')

@rgz.route('/rgz/rest-api/initiatives/', methods=['GET'])
def get_initiatives():
    conn, cur = db_connect()
    cur.execute("SELECT id, title, content, created_at, score FROM initiatives ORDER BY created_at DESC LIMIT 20")
    initiatives = cur.fetchall()
    db_close(conn, cur)
    return rows_to_dicts(initiatives)

@rgz.route('/rgz/rest-api/initiatives/<int:id>', methods=['GET'])
def get_initiative(id):
    conn, cur = db_connect()
    cur.execute("SELECT * FROM initiatives WHERE id = %s", (id,))
    initiative = cur.fetchone()
    db_close(conn, cur)
    if not initiative:
        return abort(404)
    return dict(initiative)

@rgz.route('/rgz/rest-api/initiatives/', methods=['POST'])
def add_initiative():
    if 'user_id' not in session:
        return {'description': 'Требуется авторизация'}, 403
    initiative = request.get_json()
    if not initiative or not all(k in initiative for k in ('title', 'content')):
        return {'description': 'Некорректные данные'}, 400
    conn, cur = db_connect()
    cur.execute(
        """
        INSERT INTO initiatives (title, content, created_by) 
        VALUES (%s, %s, %s) RETURNING id
        """, 
        (initiative['title'], initiative['content'], session['user_id'])
    )
    new_id = cur.fetchone()['id']
    db_close(conn, cur)
    return {'id': new_id}, 201

@rgz.route('/rgz/rest-api/initiatives/<int:id>', methods=['DELETE'])
def delete_initiative(id):
    if 'user_id' not in session:
        return {'description': 'Требуется авторизация'}, 403
    conn, cur = db_connect()
    cur.execute("SELECT created_by FROM initiatives WHERE id = %s", (id,))
    initiative = cur.fetchone()
    if not initiative or initiative['created_by'] != session['user_id']:
        db_close(conn, cur)
        return abort(403)
    cur.execute("DELETE FROM initiatives WHERE id = %s", (id,))
    db_close(conn, cur)
    return '', 204

@rgz.route('/rgz/rest-api/initiatives/<int:id>/vote', methods=['POST'])
def vote_initiative(id):
    if 'user_id' not in session:
        return {'description': 'Требуется авторизация'}, 403
    vote = request.get_json()
    if not vote or 'vote' not in vote or vote['vote'] not in (-1, 1):
        return {'description': 'Некорректный голос'}, 400
    conn, cur = db_connect()
    cur.execute("SELECT * FROM votes WHERE user_id = %s AND initiative_id = %s", (session['user_id'], id))
    if cur.fetchone():
        db_close(conn, cur)
        return {'description': 'Вы уже голосовали'}, 400
    cur.execute(
        """
        INSERT INTO votes (user_id, initiative_id, vote) 
        VALUES (%s, %s, %s)
        """, 
        (session['user_id'], id, vote['vote'])
    )
    cur.execute(
        "UPDATE initiatives SET score = score + %s WHERE id = %s RETURNING score", 
        (vote['vote'], id)
    )
    score = cur.fetchone()['score']
    db_close(conn, cur)
    return {'score': score}, 200
