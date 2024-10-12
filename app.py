from flask import Flask, url_for, redirect, render_template, abort, request ,redirect
from lab1 import lab1

app = Flask(__name__)

app.register_blueprint(lab1)

@app.errorhandler(404)
def not_found(err):
    path = url_for('static', filename='404.jpg')
    css = url_for('static', filename='lab1.css')
    return '''
    <!doctype html>
    <html>
        <head>
            <link rel="stylesheet" href="''' + css + '''">
        </head>
        <body>
            <main>
                <h1>ОЙ)))) ОШИБОЧКА)))</h1>
                <img src="''' + path + '''">
            <main>
        </body>
    </html>
    '''  

@app.route("/")
@app.route("/index")
def start():
    return '''
    <!doctype html>
    <html>
        <head>
            <title>НГТУ, ФБ, Лабораторные работы</title>
        </head>
        <body>
            <header>
                <h1>НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных</h1>
            </header>
            <main>
                <ul>
                    <li><a href="/lab1">Первая лабораторная</a></li>
                    <li><a href="/lab2">Вторая лабораторная</a></li>
                </ul>
            </main>
            <footer>
                 &copy; Осягин Иван, ФБИ-22, 3 курс, 2024
            </footer>
        </body>
    </html>
    '''

@app.errorhandler(500)
def err_505(err):
    path = url_for('static', filename='500.png')
    css = url_for('static', filename='lab1.css')
    return '''
    <!doctype html>
    <html>
        <head>
            <link rel="stylesheet" href="''' + css + '''">
        </head>
        <body>
            <main>
                <h1>МЫ ПОДЕЛМИЛИ НА НОЛЬ ЧТО-ТО) НЕ ПАРЬТЕСЬ</h1>
                <img src="''' + path + '''">
            <main>
        </body>
    </html>
    '''  
@app.route("/lab2/a")
def a():
    return 'без слэша'

@app.route("/lab2/a2")
def a2():
    return 'со слешем'

flower_list = [
    {"name": "роза", "price": 100},
    {"name": "тюльпан", "price": 50},
    {"name": "жимолость", "price": 70},
    {"name": "Глеб", "price": 2000},  
    {"name": "ананас", "price": 200}
]

@app.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id >= len(flower_list):
        return render_template('flowerNotFound.html', total_flowers=len(flower_list), flower_list=flower_list), 404
    else:
        flower = flower_list[flower_id]
        return render_template('flowerFound.html', flower=flower, flower_id=flower_id, total_flowers=len(flower_list), flower_list=flower_list)

@app.route('/lab2/flowers/delete')
def deleteFlower():
    global flower_list
    flower_list = []
    return redirect('/lab2/flowers')

@app.route('/lab2/add_flower')
def add_flower():
    flower_name = request.args.get('name')
    if flower_name:
        flower_list.append({"name": flower_name, "price": "Неизвестно"})
    return redirect('/lab2/flowers')
   
@app.route('/lab2/flowers')
def flowersList():
    return render_template('flowers.html', flower_list=flower_list)

@app.route('/lab2/example')
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
    return render_template('example.html',
                           name=name, group=group, course=course,
                           lab_num=lab_num, fruits=fruits)

@app.route('/lab2/')
def lab2():
    return render_template('lab2.html')

@app.route('/lab2/filters')
def filters():
    phrase = 'О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных...'
    return render_template('filter.html', phrase=phrase)

@app.route('/lab2/calc/<int:a>/<int:b>')
def calc(a,b):
    return render_template('calcLab2.html', a=a,b=b)

@app.route('/lab2/calc/')
@app.route('/lab2/calc')
def calcredirect():
    return redirect('/lab2/calc/1/1')

@app.route('/lab2/calc/<int:a>')
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

@app.route('/lab2/booklist/')
def bookslist():
    global booklist
    return render_template('booklist.html', booklist=booklist)

gamingPcList = [
    {"Name": "Игровое Безумие", "url": 'gaming1.webp', 'about': 'Безумный по самое не балуй'},
    {"Name": "Предвестник потной катки", "url": 'gaming2.webp', 'about': 'ИГРАТЬ! ИГРАТЬ! ИГРАТЬ!'},
    {"Name": "Играй не хочу!", "url": 'gaming3.jpg', 'about': 'Я уже реально не хочу....'},
    {"Name": "Ядерный зверь", "url": 'gaming4.jpg', 'about': 'АНОМАЛИЯ в мире ИГРОВЫХ PC'},
    {"Name": "Чернобыльская игровуха", "url": 'gaming5.png', 'about': 'Из 4 реактора прямо к вам в квартиру!'}
]

@app.route('/lab2/gamingpcs')
def gamingPcsList():
    global gamingPcList
    return render_template('gamingAF.html', gamingPcList=gamingPcList)

@app.route('/lab2/flowers/deleteNum/<int:num>')
def deleteNumFlower(num):
    if num <= len(flower_list) and num >= 0:
        flower_list.pop(num)
        return redirect('/lab2/flowers')
    else:
        abort(404)