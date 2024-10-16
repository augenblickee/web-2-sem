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


smartPhoneList = [
    {'Name':'IPhone 9', 'Color':'red','MEM':128, 'Price':30000},
    {'Name':'Samsung Galaxy SS14', 'Color':'blue','MEM':128, 'Price':45000},
    {'Name':'Xiaomi Mi 1000', 'Color':'black','MEM':256, 'Price':35000},
    {'Name':'Google Pixel 10 XXL LARGE', 'Color':'white','MEM':128, 'Price':40000},
    {'Name':'OneMinus -10', 'Color':'silver','MEM':256, 'Price':42000},
    {'Name':'Huawei Google Play', 'Color':'gold','MEM':128, 'Price':38000},
    {'Name':'Sony Xperia 1 III', 'Color':'purple','MEM':256, 'Price':50000},
    {'Name':'LG Velvet', 'Color':'green','MEM':128, 'Price':32000},
    {'Name':'Motorola Edge', 'Color':'gray','MEM':256, 'Price':34000},
    {'Name':'Nokia 8.3', 'Color':'blue','MEM':128, 'Price':28000},
    {'Name':'Oppo Reno 5', 'Color':'pink','MEM':128, 'Price':33000},
    {'Name':'Vivo X60', 'Color':'black','MEM':256, 'Price':36000},
    {'Name':'Realme 8 Pro', 'Color':'red','MEM':128, 'Price':25000},
    {'Name':'Asus ROG Phone 5', 'Color':'white','MEM':256, 'Price':48000},
    {'Name':'ZTE Axon 30', 'Color':'black','MEM':128, 'Price':31000},
    {'Name':'Lenovo Legion Phone Duel', 'Color':'blue','MEM':256, 'Price':45000},
    {'Name':'BlackBerry Key2', 'Color':'silver','MEM':128, 'Price':37000},
    {'Name':'Alcatel 3X', 'Color':'gold','MEM':64, 'Price':18000},
    {'Name':'Meizu 18', 'Color':'purple','MEM':128, 'Price':30000},
    {'Name':'TCL 20 Pro', 'Color':'green','MEM':256, 'Price':34000},
    {'Name':'Honor 50', 'Color':'gray','MEM':128, 'Price':32000}
]


@lab3.route('/lab3/smartPhone')
def smartPhone():
    min = request.args.get('min')
    max = request.args.get('max')
    showList =[]
    if min == '':
        errors['min'] = 'Заполните поле!'
    else:
        errors['min'] = ''

    if max == '':
        errors['max'] = 'Заполните поле!'
    else:
        errors['max'] = ''

    if (min and max):
        for i in smartPhoneList:
            if i['Price'] >= int(min) and i['Price'] <= int(max):
                showList.append(i)

    return render_template('/lab3/smartPhone.html', min=min, max=max, errors=errors, smartPhoneList=smartPhoneList,
                           showList=showList)
    
