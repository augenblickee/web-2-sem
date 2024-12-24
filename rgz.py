from flask import Blueprint, render_template, abort, request, current_app, session, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3
from os import path
import bcrypt

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
    user_id = session.get('user_id')
    username = None
    if user_id:
        conn, cur = db_connect()
        try:
            cur.execute("SELECT username FROM users WHERE id = %s", (user_id,))
            user = cur.fetchone()
            if user:
                username = user['username']
        finally:
            db_close(conn, cur)

    return render_template('/rgz/main.html', username=username)

@rgz.route('/rgz/rest-api/initiatives/', methods=['GET'])
def get_initiatives():
    conn, cur = db_connect()
    cur.execute("""
        SELECT 
            initiatives.id, 
            initiatives.title, 
            initiatives.content, 
            initiatives.created_at, 
            initiatives.score,
            users.username AS author
        FROM initiatives
        LEFT JOIN users ON initiatives.created_by = users.id
        ORDER BY initiatives.score DESC
    """)
    initiatives = cur.fetchall()
    db_close(conn, cur)
    return initiatives

@rgz.route('/rgz/rest-api/register', methods=['POST'])
def register_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return {"success": False, "error": "Имя пользователя и пароль обязательны."}, 400

    # Генерация хэша пароля
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    conn, cur = db_connect()
    try:
        # Проверяем, существует ли пользователь с таким именем
        cur.execute("SELECT id FROM users WHERE username = %s", (username,))
        if cur.fetchone():
            return {"success": False, "error": "Пользователь с таким именем уже существует."}, 400

        # Сохраняем пользователя в базу данных
        cur.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", (username, password_hash.decode('utf-8')))
        conn.commit()
        return {"success": True}
    finally:
        db_close(conn, cur)

@rgz.route('/rgz/rest-api/login', methods=['POST'])
def login_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return {"success": False, "error": "Имя пользователя и пароль обязательны."}, 400

    conn, cur = db_connect()
    try:
        cur.execute("SELECT id, password_hash FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        if user:
            if bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
                session['user_id'] = user['id']
                return {"success": True}
            else:
                return {"success": False, "error": "Неправильное имя пользователя или пароль."}, 401
        else:
            return {"success": False, "error": "Неправильное имя пользователя или пароль."}, 401
    finally:
        db_close(conn, cur)


@rgz.route('/rgz/rest-api/logout', methods=['POST'])
def logout_user():
    session.pop('user_id', None)
    return {"success": True}



@rgz.route('/rgz/rest-api/initiatives/', methods=['POST'])
def add_initiative():
    user_id = session.get('user_id')
    if not user_id:
        return {"success": False, "error": "Вы не авторизованы."}, 401

    data = request.get_json()
    title = data.get('title')
    content = data.get('content')

    if not title or not content:
        return {"success": False, "error": "Название и текст инициативы обязательны."}, 400

    conn, cur = db_connect()
    try:
        cur.execute(
            "INSERT INTO initiatives (title, content, created_by) VALUES (%s, %s, %s)",
            (title, content, user_id)
        )
        conn.commit()
        return {"success": True}
    finally:
        db_close(conn, cur)
