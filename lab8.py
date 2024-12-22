from flask import Blueprint, render_template, abort, request, current_app, redirect, session
from werkzeug.security import check_password_hash, generate_password_hash
from db import db
from db.models import users, articles
from flask_login import login_user, login_required, current_user, logout_user

lab8 = Blueprint('lab8', __name__)

@lab8.route('/lab8/')
def lab():
    if current_user.is_authenticated:
        user = current_user.login
    else:
        user = 'Анонимус' 
    return render_template('/lab8/lab8.html', user=user)

@lab8.route('/lab8/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab8/register.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')
    if not login_form:
        return render_template('lab8/register.html', error = 'Путой логин!')
    if not password_form:
        return render_template('lab8/register.html', error = 'Путой пароль!')

    login_exists = users.query.filter_by(login = login_form).first()
    if login_exists:
        return render_template('lab8/register.html', error = 'Такой пользователь уже существует!')
    
    password_hash = generate_password_hash(password_form)
    new_user = users(login = login_form, password = password_hash)
    db.session.add(new_user)
    db.session.commit()
    login_user(new_user, remember=False)
    return redirect('/lab8/')


@lab8.route('/lab8/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab8/login.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')
    if not login_form:
        return render_template('lab8/login.html', error = 'Путой логин!')
    if not password_form:
        return render_template('lab8/login.html', error = 'Путой пароль!')
    
    user = users.query.filter_by(login = login_form).first()

    remember = False
    if request.form.get('remember'):
        remember = True
    if user:
        if check_password_hash(user.password, password_form):
            login_user(user, remember=remember)
            return redirect('/lab8/')
        
    return render_template('/lab8/login.html', error = 'Неправльно введены данные!')


@lab8.route('/lab8/articles/')
@login_required
def article_list():
    return 'Список статей'


@lab8.route('/lab8/logout')
@login_required
def logout():
    logout_user()
    return redirect('/lab8/')


@lab8.route('/lab8/create/', methods = ['GET', 'POST'])
@login_required
def create():
        login_id = current_user.id
        if request.method == 'GET':
            return render_template('/lab8/create.html')
        
        title = request.form.get('title')
        article_text = request.form.get('article_text')
        is_public = request.form.get('is_public') == '1'

        if not (title and article_text):
            return render_template('/lab8/create.html', error='Введите текст и название статьи!')

        new_article = articles(login_id = login_id, title = title, article_text = article_text, is_public = is_public)
        db.session.add(new_article)
        db.session.commit()

        return redirect('/lab8/')