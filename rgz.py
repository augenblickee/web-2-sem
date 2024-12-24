from flask import Blueprint, render_template, request, current_app, session, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3
from os import path
import bcrypt
from datetime import datetime

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


def format_date(date_str):
    if isinstance(date_str, str):
      date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
      return date_obj.strftime('%Y-%m-%d %H:%M:%S')
    else:
      return date_str.strftime('%Y-%m-%d %H:%M:%S')


def get_user_name():
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
    return username
    

@rgz.route('/rgz/')
def main():
    username = get_user_name()
    return render_template('/rgz/main.html', username=username)


@rgz.route('/rgz/rest-api/initiatives/', methods=['GET'])
def get_initiatives():
    conn, cur = db_connect()
    try:
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
        for initiative in initiatives:
            initiative['created_at'] = format_date(initiative['created_at'])
        return jsonify(initiatives)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
      db_close(conn, cur)


@rgz.route('/rgz/rest-api/register', methods=['POST'])
def register_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Имя пользователя и пароль обязательны."}), 400

    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    conn, cur = db_connect()
    try:
        cur.execute("SELECT id FROM users WHERE username = %s", (username,))
        if cur.fetchone():
            return jsonify({"error": "Пользователь с таким именем уже существует."}), 400

        cur.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", (username, password_hash.decode('utf-8')))
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
      db_close(conn, cur)

@rgz.route('/rgz/rest-api/login', methods=['POST'])
def login_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Имя пользователя и пароль обязательны."}), 400

    conn, cur = db_connect()
    try:
        cur.execute("SELECT id, password_hash FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        if user:
            if bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
                session['user_id'] = user['id']
                return jsonify({"success": True})
            else:
               return jsonify({"error": "Неправильное имя пользователя или пароль."}), 401
        else:
            return jsonify({"error": "Неправильное имя пользователя или пароль."}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
      db_close(conn, cur)


@rgz.route('/rgz/rest-api/logout', methods=['POST'])
def logout_user():
    session.pop('user_id', None)
    return jsonify({"success": True})


@rgz.route('/rgz/rest-api/initiatives/', methods=['POST'])
def add_initiative():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Вы не авторизованы."}), 401

    data = request.get_json()
    title = data.get('title')
    content = data.get('content')

    if not title or not content:
        return jsonify({"error": "Название и текст инициативы обязательны."}), 400

    conn, cur = db_connect()
    try:
        cur.execute(
            "INSERT INTO initiatives (title, content, created_by) VALUES (%s, %s, %s)",
            (title, content, user_id)
        )
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
      db_close(conn, cur)

@rgz.route('/rgz/rest-api/my-initiatives/', methods=['GET'])
def get_my_initiatives():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Вы не авторизованы."}), 401

    conn, cur = db_connect()
    try:
        cur.execute("""
            SELECT 
                initiatives.id, 
                initiatives.title, 
                initiatives.content, 
                initiatives.created_at, 
                initiatives.score
            FROM initiatives
            WHERE initiatives.created_by = %s
            ORDER BY initiatives.created_at DESC
        """, (user_id,))
        initiatives = cur.fetchall()
        for initiative in initiatives:
            initiative['created_at'] = format_date(initiative['created_at'])
        return jsonify(initiatives)
    except Exception as e:
         return jsonify({"error": str(e)}), 500
    finally:
        db_close(conn, cur)


@rgz.route('/rgz/rest-api/initiatives/<int:id>/', methods=['DELETE'])
def delete_initiative(id):
    user_id = session.get('user_id')
    if not user_id:
       return jsonify({"error": "Вы не авторизованы."}), 401

    conn, cur = db_connect()
    try:
        cur.execute("""
            SELECT created_by FROM initiatives WHERE id = %s
        """, (id,))
        initiative = cur.fetchone()
        if not initiative or initiative['created_by'] != user_id:
            return jsonify({"error": "Вы не можете удалить эту инициативу."}), 403

        cur.execute("DELETE FROM initiatives WHERE id = %s", (id,))
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db_close(conn, cur)


@rgz.route('/rgz/rest-api/initiatives/<int:id>/', methods=['PUT'])
def update_initiative(id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Вы не авторизованы."}), 401

    data = request.get_json()
    title = data.get('title')
    content = data.get('content')

    if not title or not content:
        return jsonify({"error": "Название и текст инициативы обязательны."}), 400

    conn, cur = db_connect()
    try:
        # Проверяем, принадлежит ли инициатива текущему пользователю
        cur.execute("""
            SELECT created_by FROM initiatives WHERE id = %s
        """, (id,))
        initiative = cur.fetchone()
        if not initiative or initiative['created_by'] != user_id:
            return jsonify({"error": "Вы не можете редактировать эту инициативу."}), 403

        # Обновляем инициативу
        cur.execute("""
            UPDATE initiatives 
            SET title = %s, content = %s
            WHERE id = %s
        """, (title, content, id))
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
       db_close(conn, cur)