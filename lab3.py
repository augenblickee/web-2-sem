from flask import Blueprint, render_template, request, make_response, redirect

lab3 = Blueprint('lab3', __name__)

errors ={}

@lab3.route('/lab3/')
def lab():
    age = request.cookies.get('age')
    name = request.cookies.get('name')
    name_color = request.cookies.get('name_color')
    return render_template('/lab3/lab3.html', name=name, name_color=name_color, age=age)


@lab3.route('/lab3/cookie')
def cookie():
    resp = make_response(redirect('/lab3/'))
    resp.set_cookie('name', 'ГЛЕБ', max_age=5)
    resp.set_cookie('age', '20')
    resp.set_cookie('name_color', 'red')
    return resp


@lab3.route('/lab3/del_cookie')
def del_cookie():
    resp = make_response(redirect('/lab3/'))
    resp.delete_cookie('name')
    resp.delete_cookie('age')
    resp.delete_cookie('name_color')
    return resp


@lab3.route('/lab3/form1')
def form1():
    user = request.args.get('user')
    age = request.args.get('age')
    if user == '':
        errors['user'] = 'Заполните поле!'
    else:
        errors['user'] = ''
    if age == '':
        errors['agee'] = 'Заполните поле!'
    else:
        errors['agee'] = ''
    sex = request.args.get('sex')
    return render_template('lab3/form1.html', user=user, age=age, sex=sex, errors=errors)


@lab3.route('/lab3/formTrain', methods=['GET', 'POST'])
def formTrain():
    ticketCost = 0
    fio = request.args.get('fio')
    place = request.args.get('place')
    linen = request.args.get('linen')
    luggage = request.args.get('luggage')
    age = request.args.get('age')
    start = request.args.get('start')
    end = request.args.get('end')
    date = request.args.get('date')
    insurance = request.args.get('insurance')

    argsNames = [fio, age, start, end, date]

    check = False

    if fio == '':
        errors['fio'] = 'Заполните поле!'
    else:
        errors['fio'] = ''

    if age == '':
        errors['age'] = 'Заполните поле!'
    elif  type(age) == str and (int(age) < 0 or int(age) > 120):
        errors['age'] = 'Возраст должен быть от 0 до 120 лет!'
    else:
        errors['age'] = ''

    if start == '':
        errors['start'] = 'Заполните поле!'
    else:
        errors['start'] = ''

    if end == '':
        errors['end'] = 'Заполните поле!'
    else:
        errors['end'] = ''

    if date == '':
        errors['date'] = 'Заполните поле!'
    else:
        errors['date'] = ''

    if all(argsNames) and (int(age) >= 0 and int(age) <= 120):
        check = True

    if check == True:
        if int(age) > 17:
            ticketCost += 1000
        else:
            ticketCost += 700

        if place == 'нижняя':
            ticketCost += 100
        elif place == 'нижняя боковая':
            ticketCost += 100
        
        if linen is not None:
            ticketCost += 75
        
        if luggage is not None:
            ticketCost += 250
        
        if insurance is not None:
            ticketCost += 150
        
    return render_template('lab3/formTrain.html', fio=fio, place=place, linen=linen, luggage=luggage,
                        age=age, start=start, end=end, date=date, insurance=insurance, errors=errors,
                        argsNames=argsNames, check=check, ticketCost=ticketCost)


@lab3.route('/lab3/order')
def order():
    return render_template('lab3/order.html')


price = 0

@lab3.route('/lab3/pay')
def pay():
    global price
    drink = request.args.get('drink')

    if drink == 'cofee':
        price = 120
    elif drink == 'black-tea':
        price = 80
    else:
        price = 70

    if request.args.get('milk') == 'on':
        price += 30
    if request.args.get('sugar') == 'on':
        price += 10

    return render_template('lab3/pay.html', price=price)


price = 0
@lab3.route('/lab3/success')
def success():
    global price
    return render_template('/lab3/success.html', price=price)

@lab3.route('/lab3/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        color = request.form.get('color')
        backgroundcolor = request.form.get('backgroundcolor')
        fontsize = request.form.get('fontsize')
        linkcolor = request.form.get('linkcolor')
        if color and backgroundcolor:
            resp = make_response(redirect('/lab3/settings'))
            resp.set_cookie('color', color)
            resp.set_cookie('backgroundcolor', backgroundcolor)
            resp.set_cookie('fontsize', fontsize)
            resp.set_cookie('linkcolor', linkcolor)
            return resp

    color = request.cookies.get('color')
    backgroundcolor = request.cookies.get('backgroundcolor')
    fontsize = request.cookies.get('fontsize')
    linkcolor = request.cookies.get('linkcolor')
    resp = make_response(render_template('lab3/settings.html', color=color, backgroundcolor=backgroundcolor,fontsize=fontsize, linkcolor=linkcolor))
    return resp


@lab3.route('/lab3/delete_cookies')
def deletecookies():
    resp = make_response(redirect('/lab3/settings'))
    resp.delete_cookie('color')
    resp.delete_cookie('backgroundcolor')
    resp.delete_cookie('fontsize')
    resp.delete_cookie('linkcolor')
    return resp