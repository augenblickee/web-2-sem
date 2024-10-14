from flask import Blueprint, redirect, render_template, abort, request ,redirect

lab2 = Blueprint('lab2', __name__)

@lab2.route("/lab2/a")
def a():
    return 'без слэша'


@lab2.route("/lab2/a2")
def a2():
    return 'со слешем'


flower_list = [
    {"name": "роза", "price": 100},
    {"name": "тюльпан", "price": 50},
    {"name": "жимолость", "price": 70},
    {"name": "Глеб", "price": 2000},  
    {"name": "ананас", "price": 200}
]

@lab2.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id >= len(flower_list):
        return render_template('/lab2/flowerNotFound.html', total_flowers=len(flower_list), flower_list=flower_list), 404
    else:
        flower = flower_list[flower_id]
        return render_template('/lab2/lowerFound.html', flower=flower, flower_id=flower_id, total_flowers=len(flower_list), flower_list=flower_list)


@lab2.route('/lab2/flowers/delete')
def deleteFlower():
    global flower_list
    flower_list = []
    return redirect('/lab2/flowers')


@lab2.route('/lab2/add_flower')
def add_flower():
    flower_name = request.args.get('name')
    if flower_name:
        flower_list.append({"name": flower_name, "price": "Неизвестно"})
    return redirect('/lab2/flowers')
   

@lab2.route('/lab2/flowers')
def flowersList():
    return render_template('/lab2/flowers.html', flower_list=flower_list)


@lab2.route('/lab2/example')
def example():
    name = "Иван Осягин !!!"
    group = 'FBI-22'
    course = 3
    lab_num = 2
    fruits = [
        {"name": "Яблоко", "price": 200},
        {"name": "Круглый огурец", "price": 450},
        {"name": "Апельсин", "price": 300},
        {"name": "Глеб", "price": 24000},
        {"name": "Амням", "price": 2050},
        {"name": "Большая тыква", "price": 700}
    ]
    return render_template('/lab2/example.html',
                           name=name, group=group, course=course,
                           lab_num=lab_num, fruits=fruits)


@lab2.route('/lab2/')
def lab():
    return render_template('/lab2/lab2.html')


@lab2.route('/lab2/filters')
def filters():
    phrase = 'О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных...'
    return render_template('/lab2/filter.html', phrase=phrase)


@lab2.route('/lab2/calc/<int:a>/<int:b>')
def calc(a,b):
    return render_template('/lab2/calcLab2.html', a=a,b=b)


@lab2.route('/lab2/calc/')
@lab2.route('/lab2/calc')
def calcredirect():
    return redirect('/lab2/calc/1/1')


@lab2.route('/lab2/calc/<int:a>')
def calcredirect2(a):
    return redirect(f'/lab2/calc/{a}/1')


booklist = [
    {"author": "Хян Со", "name": 'Призрак в магазине канцтоваров', 'gender': 'Корейское', 'pageNum': 224},
    {"author": "Дадзай Осаму", "name": "Человек недостойный", 'gender': 'Классическая литература', 'pageNum': 192},
    {"author": "Харуки Мураками", "name": "Норвежский лес", 'gender': 'Современная японская литература', 'pageNum': 384},
    {"author": "Лев Толстой", "name": "Война и мир", 'gender': 'Русская классика', 'pageNum': 1225},
    {"author": "Федор Достоевский", "name": "Преступление и наказание", 'gender': 'Русская классика', 'pageNum': 671},
    {"author": "Габриэль Гарсия Маркес", "name": "Сто лет одиночества", 'gender': 'Латиноамериканская литература', 'pageNum': 417},
    {"author": "Джордж Оруэлл", "name": "1984", 'gender': 'Английская литература', 'pageNum': 328},
    {"author": "Михаил Булгаков", "name": "Мастер и Маргарита", 'gender': 'Русская литература', 'pageNum': 480},
    {"author": "Джейн Остин", "name": "Гордость и предубеждение", 'gender': 'Английская классическая литература', 'pageNum': 279},
    {"author": "Маргарет Этвуд", "name": "Рассказ служанки", 'gender': 'Современная литература', 'pageNum': 311}
]


@lab2.route('/lab2/booklist/')
def bookslist():
    global booklist
    return render_template('/lab2/booklist.html', booklist=booklist)


gamingPcList = [
    {"Name": "Игровое Безумие", "url": '/lab2/gaming1.webp', 'about': 'Безумный по самое не балуй'},
    {"Name": "Предвестник потной катки", "url": '/lab2/gaming2.webp', 'about': 'ИГРАТЬ! ИГРАТЬ! ИГРАТЬ!'},
    {"Name": "Играй не хочу!", "url": '/lab2/gaming3.jpg', 'about': 'Я уже реально не хочу....'},
    {"Name": "Ядерный зверь", "url": './lab2/gaming4.jpg', 'about': 'АНОМАЛИЯ в мире ИГРОВЫХ PC'},
    {"Name": "Чернобыльская игровуха", "url": '/lab2/gaming5.png', 'about': 'Из 4 реактора прямо к вам в квартиру!'}
]


@lab2.route('/lab2/gamingpcs')
def gamingPcsList():
    global gamingPcList
    return render_template('/lab2/gamingAF.html', gamingPcList=gamingPcList)


@lab2.route('/lab2/flowers/deleteNum/<int:num>')
def deleteNumFlower(num):
    if num <= len(flower_list) and num >= 0:
        flower_list.pop(num)
        return redirect('/lab2/flowers')
    else:
        abort(404)