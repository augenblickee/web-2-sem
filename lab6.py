from flask import Blueprint, render_template, request, session, current_app
from random import randint
import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3
from os import path

lab6 = Blueprint('lab6', __name__)

# offices = []
# for i in range(1, 11):
#     offices.append({'number': i, 'tenant': '', 'price': 900 + randint(-400, 400)})

def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host = '::1',
            database = 'osyagin_ivan_knowledge_base',
            user = 'osyagin_ivan_knowledge_base',
            password = 'KAKASHKI123'
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


@lab6.route('/lab6/')
def lab():
    return render_template('lab6/lab6.html')


def get_offices_from_db():
    conn, cur = db_connect()
    cur.execute("SELECT * FROM offices ORDER BY number")
    offices = cur.fetchall()
    db_close(conn, cur)
    return [dict(office) for office in offices]

@lab6.route('/lab6/json-rpc-api/', methods=['POST'])
def api():
    data = request.json
    id = data['id']
    result = {
        'jsonrpc': '2.0',
        'id': id
    }

    if data['method'] == 'info':
        result['result'] = get_offices_from_db()
        return result
    
    login = session.get('login')
    if not login:
        result['error'] = {
            'code': 1,
            'message': 'Unauthorized'
        }
        return result
    
    conn, cur = db_connect()
    office_number = data.get('params')
    
    if data['method'] == 'booking':
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT tenant FROM offices WHERE number = %s", (office_number,))
        else:
            cur.execute("SELECT tenant FROM offices WHERE number = ?", (office_number,))
        office = cur.fetchone()
        if office and office['tenant']:
            result['error'] = {
                'code': 2,
                'message': 'Already booked'
            }
        else:
            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute("UPDATE offices SET tenant = %s WHERE number = %s", (login, office_number))
            else:
                cur.execute("UPDATE offices SET tenant = ? WHERE number = ?", (login, office_number))
            conn.commit()
            result['result'] = 'success'
    
    elif data['method'] == 'cancel':
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT tenant FROM offices WHERE number = %s", (office_number,))
        else:
            cur.execute("SELECT tenant FROM offices WHERE number = ?", (office_number,))
        office = cur.fetchone()
        if office and office['tenant'] == '':
            result['error'] = {
                'code': 3,
                'message': 'Office not booked'
            }
        elif office and office['tenant'] != login:
            result['error'] = {
                'code': 4,
                'message': "You didn't book this office"
            }
        else:
            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute("UPDATE offices SET tenant = '' WHERE number = %s", (office_number,))
            else:
                cur.execute("UPDATE offices SET tenant = '' WHERE number = ?", (office_number,))
            conn.commit()
            result['result'] = 'success'
    
    else:
        result['error'] = {
            'code': -32601,
            'message': 'Method not found'
        }
    
    db_close(conn, cur)
    return result
