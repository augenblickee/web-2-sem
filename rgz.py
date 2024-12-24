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
        db_path = path.join(dir_path, 'databasergz.db')
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

def rows_to_dicts(rows):
    #sqlite3 передает в конект роу формат, а апи с ним не работает, переделал в словарик
    return [dict(row) for row in rows]

def get_user_name():
    user_id = session.get('user_id')
    username = None
    if user_id:
        conn, cur = db_connect()
        try:
            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute("SELECT username FROM users WHERE id = %s", (user_id,))
            else:
                cur.execute("SELECT username FROM users WHERE id = ?", (user_id,))
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

@rgz.route('/rgz/rest-api/user-data', methods=['GET'])
def get_user_data():
    user_id = session.get('user_id')
    return jsonify({'user_id': user_id})


@rgz.route('/rgz/rest-api/initiatives/', methods=['GET'])
def get_initiatives():
    page = request.args.get('page', 1, type=int)
    per_page = 20
    offset = (page - 1) * per_page
    user_id = session.get('user_id')

    conn, cur = db_connect()
    try:
        if current_app.config['DB_TYPE'] == 'postgres':
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
                LIMIT %s OFFSET %s
            """, (per_page, offset))
        else:
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
            """, (per_page, offset))
        initiatives = cur.fetchall()
        if current_app.config['DB_TYPE'] != 'postgres':
            initiatives = rows_to_dicts(initiatives)
        for initiative in initiatives:
             initiative['created_at'] = format_date(initiative['created_at'])
             if user_id:
                # проверяем наличие голоса
                 if current_app.config['DB_TYPE'] == 'postgres':
                    cur.execute("SELECT vote FROM votes WHERE user_id = %s AND initiative_id = %s", (user_id, initiative['id']))
                 else:
                    cur.execute("SELECT vote FROM votes WHERE user_id = ? AND initiative_id = ?", (user_id, initiative['id']))
                 vote_data = cur.fetchone()
                 if vote_data:
                    if current_app.config['DB_TYPE'] != 'postgres':
                       vote_data = dict(vote_data)
                    initiative['user_vote'] = vote_data['vote'] 
                 else:
                     initiative['user_vote'] = 0

        # Получаем общее количество инициатив
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT COUNT(*) FROM initiatives")
        else:
            cur.execute("SELECT COUNT(*) FROM initiatives")
        total_count = cur.fetchone()['count']

        return jsonify({
            "initiatives": initiatives,
            "total_count": total_count,
            "page": page,
            "per_page": per_page,
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
      db_close(conn, cur)

@rgz.route('/rgz/rest-api/vote/<int:initiative_id>/', methods=['POST'])
def vote_initiative(initiative_id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Вы не авторизованы."}), 401

    data = request.get_json()
    vote_value = data.get('vote')

    if vote_value not in [-1, 1]:
        return jsonify({"error": "Недопустимое значение голоса."}), 400

    conn, cur = db_connect()
    try:
        # Проверяем, существует ли уже голос пользователя за эту инициативу
        if current_app.config['DB_TYPE'] == 'postgres':
             cur.execute("SELECT vote FROM votes WHERE user_id = %s AND initiative_id = %s", (user_id, initiative_id))
        else:
            cur.execute("SELECT vote FROM votes WHERE user_id = ? AND initiative_id = ?", (user_id, initiative_id))
        existing_vote = cur.fetchone()
        
        # Получаем текущий рейтинг инициативы
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT score FROM initiatives WHERE id = %s", (initiative_id,))
        else:
            cur.execute("SELECT score FROM initiatives WHERE id = ?", (initiative_id,))
        current_score = cur.fetchone()['score']
        if current_score is None:
            current_score = 0

        new_score = current_score
        if existing_vote:
            new_score = current_score + vote_value - existing_vote['vote']
            # Обновляем голос
            if current_app.config['DB_TYPE'] == 'postgres':
                 cur.execute("UPDATE votes SET vote = %s WHERE user_id = %s AND initiative_id = %s", (vote_value, user_id, initiative_id))
            else:
                 cur.execute("UPDATE votes SET vote = ? WHERE user_id = ? AND initiative_id = ?", (vote_value, user_id, initiative_id))
        else:
            new_score = current_score + vote_value
            # Сохраняем голос
            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute("INSERT INTO votes (user_id, initiative_id, vote) VALUES (%s, %s, %s)", (user_id, initiative_id, vote_value))
            else:
                 cur.execute("INSERT INTO votes (user_id, initiative_id, vote) VALUES (?, ?, ?)", (user_id, initiative_id, vote_value))

        # Обновляем рейтинг инициативы
        if current_app.config['DB_TYPE'] == 'postgres':
             cur.execute("""
                UPDATE initiatives
                SET score = %s
                WHERE id = %s
            """, (new_score, initiative_id))
        else:
            cur.execute("""
                UPDATE initiatives
                SET score = ?
                WHERE id = ?
            """, (new_score, initiative_id))
        
        return jsonify({"success": True, "new_score": new_score})

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
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT id FROM users WHERE username = %s", (username,))
        else:
            cur.execute("SELECT id FROM users WHERE username = ?", (username,))
        if cur.fetchone():
            return jsonify({"error": "Пользователь с таким именем уже существует."}), 400

        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", (username, password_hash.decode('utf-8')))
        else:
            cur.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password_hash.decode('utf-8')))
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
        if current_app.config['DB_TYPE'] == 'postgres':
             cur.execute("SELECT id, password_hash FROM users WHERE username = %s", (username,))
        else:
             cur.execute("SELECT id, password_hash FROM users WHERE username = ?", (username,))
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
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute(
                "INSERT INTO initiatives (title, content, created_by) VALUES (%s, %s, %s)",
                (title, content, user_id)
            )
        else:
             cur.execute(
                "INSERT INTO initiatives (title, content, created_by) VALUES (?, ?, ?)",
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
        if current_app.config['DB_TYPE'] == 'postgres':
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
        else:
             cur.execute("""
                SELECT 
                    initiatives.id, 
                    initiatives.title, 
                    initiatives.content, 
                    initiatives.created_at, 
                    initiatives.score
                FROM initiatives
                WHERE initiatives.created_by = ?
                ORDER BY initiatives.created_at DESC
            """, (user_id,))
        initiatives = cur.fetchall()
        if current_app.config['DB_TYPE'] != 'postgres':
            initiatives = rows_to_dicts(initiatives)
        for initiative in initiatives:
            initiative['created_at'] = format_date(initiative['created_at'])
        return jsonify(initiatives)
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
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("""
                SELECT created_by FROM initiatives WHERE id = %s
            """, (id,))
        else:
             cur.execute("""
                SELECT created_by FROM initiatives WHERE id = ?
            """, (id,))
        initiative = cur.fetchone()
        if is_admin(user_id):
            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute("""
                    UPDATE initiatives 
                    SET title = %s, content = %s
                    WHERE id = %s
                """, (title, content, id))
            else:
                cur.execute("""
                    UPDATE initiatives 
                    SET title = ?, content = ?
                    WHERE id = ?
                """, (title, content, id))
        else:
            if not initiative or initiative['created_by'] != user_id:
                return jsonify({"error": "Вы не можете редактировать эту инициативу."}), 403
            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute("""
                    UPDATE initiatives 
                    SET title = %s, content = %s
                    WHERE id = %s
                """, (title, content, id))
            else:
                 cur.execute("""
                    UPDATE initiatives 
                    SET title = ?, content = ?
                    WHERE id = ?
                """, (title, content, id))
        return jsonify({"success": True})
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
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("""
                SELECT created_by FROM initiatives WHERE id = %s
            """, (id,))
        else:
            cur.execute("""
                SELECT created_by FROM initiatives WHERE id = ?
            """, (id,))
        initiative = cur.fetchone()
        if is_admin(user_id):
            if current_app.config['DB_TYPE'] == 'postgres':
                 cur.execute("DELETE FROM initiatives WHERE id = %s", (id,))
            else:
                 cur.execute("DELETE FROM initiatives WHERE id = ?", (id,))
        else:
            if not initiative or initiative['created_by'] != user_id:
                return jsonify({"error": "Вы не можете удалить эту инициативу."}), 403
            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute("DELETE FROM initiatives WHERE id = %s", (id,))
            else:
                 cur.execute("DELETE FROM initiatives WHERE id = ?", (id,))
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db_close(conn, cur)

def is_admin(user_id):
    if not user_id:
        return False
    conn, cur = db_connect()
    try:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT is_admin FROM users WHERE id = %s", (user_id,))
        else:
            cur.execute("SELECT is_admin FROM users WHERE id = ?", (user_id,))
        user = cur.fetchone()
        if user:
            return user['is_admin']
        return False
    except Exception as e:
        return False
    finally:
      db_close(conn, cur)