from flask import Blueprint, render_template, request, redirect, session

lab4 = Blueprint('lab4', __name__)

@lab4.route('/lab4/')
def lab():
    return render_template('lab4/lab4.html')


@lab4.route('/lab4/div-form')
def div_form():
    return render_template('lab4/div-form.html')


@lab4.route('/lab4/div', methods = ['POST'])
def div():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    op = request.form.get('op')
    if op == '/':
        if x1 == '' or x2 == '':
            return render_template('lab4/div.html', error='Оба поля должны быть заполнены!')
        elif x2 == '0':
            return render_template('lab4/div.html', error='На ноль делить нельзя!')
        x1 = int(x1)
        x2 = int(x2)
        result = x1 / x2
    elif op == '+':
        if x1 == '':
            x1 = '0'
        if x2 == '':
            x2 = '0'
        x1 = int(x1)
        x2 = int(x2)
        result = x1 + x2

    elif op == '*':
        if x1 == '':
            x1 = '1'
        if x2 == '':
            x2 = '1'
        x1 = int(x1)
        x2 = int(x2)
        result = x1 * x2

    elif op == '-':
        if x1 == '' or x2 == '':
            return render_template('lab4/div.html', error='Оба поля должны быть заполнены!')
        x1 = int(x1)
        x2 = int(x2)
        result = x1 - x2
    else:
        if x1 == '' or x2 == '' or (x1 == '0' and x2 == '0'):
            return render_template('lab4/div.html', error='Заполните поля или нолики свои тут не пихайте куда попало!')
        x1 = int(x1)
        x2 = int(x2)
        result = x1 ** x2
    return render_template('lab4/div.html', x1=x1, x2=x2, result=result, op=op)


tree_count = 1


@lab4.route('/lab4/tree', methods = ['GET', 'POST'])
def tree():
    global tree_count
    if request.method == 'GET':
        return render_template('/lab4/tree.html', tree_count=tree_count)
    
    operation = request.form.get('operation')

    if operation == 'cut':
        if tree_count > 0:
            tree_count -= 1
        else:
            tree_count = 0
    elif operation == 'plant':
        if tree_count <= 10:
            tree_count += 1
        else:
            tree_count = 10
    return redirect('/lab4/tree')


users = [
    {'login': 'alex', 'password': '123'},
    {'login': 'bob', 'password': '555'},
    {'login': 'gleb', 'password': '321'},
    {'login': 'SUS', 'password': 'gleb'},
]


@lab4.route('/lab4/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'login' in session:
            authorized = True
            login = session['login']
        else:
            authorized = False
            login = ''
        return render_template('lab4/login.html', authorized=authorized, login=login)
    
    login = request.form.get('login')
    password = request.form.get('password')

    for user in users:
        if login == user['login'] and password == user['password']:
            session['login'] = login
            return redirect('/lab4/login')
            
    error = 'Неверные данные'
    return render_template('lab4/login.html', error=error, authorized=False)


@lab4.route('/lab4/logout', methods = ['POST'])
def logout():
    session.pop('login', None)
    return redirect('/lab4/login')