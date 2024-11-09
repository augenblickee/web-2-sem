from flask import Blueprint, render_template, request, redirect, session, make_response
import psycopg2

lab5 = Blueprint('lab5', __name__)

@lab5.route('/lab5/')
def lab():
    return render_template('lab5/lab5.html')

@lab5.route('/lab5/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')

    login = request.form.get('login')
    password = request.form.get('password')

    if not (login and password):
        return render_template('lab5/register.html', error='Заполните все поля')
    
    conn = psycopg2.connect(
        host = '::1',
        database = 'osyagin_ivan_knowledge_base',
        user = 'osyagin_ivan_knowledge_base',
        password = 'KAKASHKI123'
    )

    cur = conn.cursor()

    cur.execute(f"SELECT login FROM users WHERE login='{login}';")
    if cur.fetchone():
        return render_template('lab5/register.html', error='Кто-то уже занял такое имя!')
    
    cur.execute(f"INSERT INTO users (login, password) VALUES ('{login}', '{password}');")

    conn.commit()
    cur.close()
    conn.close()

    return render_template('lab5/succses.html', login=login)