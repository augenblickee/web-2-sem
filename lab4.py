from flask import Blueprint, render_template, request, make_response, redirect

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