from flask import Blueprint, render_template, request, redirect, session, make_response

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
    {'login': 'alex', 'password': '123','name':'Александор Йоу', 'sex':'male'},
    {'login': 'bob', 'password': '555','name':'БоБ Йоу', 'sex':'male'},
    {'login': 'gleb', 'password': '321','name':'Глеб Кубраков', 'sex':'male'},
    {'login': 'SUS', 'password': 'gleb','name':'СУС СУС', 'sex':'male'},
]


@lab4.route('/lab4/login', methods = ['GET', 'POST'])
def login():
    name = ''
    last_login = session.get('last_login', '') 
    if request.method == 'GET':
        if 'login' in session:
            authorized = True
            login = session['login']
            for user in users:
                if user['login'] == login:
                    name = user['name']
                    break
        else:
            authorized = False
            login = ''
        return render_template('lab4/login.html', authorized=authorized, login=login, name=name, last_login=last_login)
    
    login = request.form.get('login')
    password = request.form.get('password')
    session['last_login'] = login

    for user in users:
        if login == user['login'] and password == user['password']:
            session['login'] = login
            return redirect('/lab4/login')
        
    error = ''

    if login == '':       
        error = 'Введите логин!'
    elif password == '':       
        error = 'Введите пароль!'

    return render_template('lab4/login.html', error=error, authorized=False, last_login=last_login)


@lab4.route('/lab4/logout', methods = ['POST'])
def logout():
    session.pop('login', None)
    return redirect('/lab4/login')


@lab4.route('/lab4/temp', methods=['GET', 'POST'])
def fridge():
    snowflakes = 0
    temp = request.form.get('temp', '')
    output = ''

    if request.method == 'POST':
        if 'reset' in request.form:
            return render_template('/lab4/fridge.html', output='', temp='', snowflakes=0)

        if temp == '':
            output = 'Ошибка: не задана температура'
        elif int(temp) < -12:
            output = 'Не удалось установить температуру - слишком низкое значение'
        elif int(temp) > -1:
            output = 'Не удалось установить температуру - слишком высокое значение'
        elif -12 <= int(temp) <= -9:
            output = f'Установлена температура {temp}'
            snowflakes = 3
        elif -8 <= int(temp) <= -5:
            output = f'Установлена температура {temp}'
            snowflakes = 2
        elif -4 <= int(temp) <= -1:
            output = f'Установлена температура {temp}'
            snowflakes = 1

        return render_template('/lab4/fridge.html', output=output, temp=temp, snowflakes=snowflakes)

    return render_template('/lab4/fridge.html', output=output, temp=temp, snowflakes=snowflakes)
