from flask import Flask, url_for, redirect, render_template

app = Flask(__name__)
create = False
delete = False

@app.route('/lab1/web')
def web():
    return """<!doctype html>
        <html>
            <body>
                <h1>web-server on flask</h1>
                <a href="/lab1/author">author</a>
            <body>
        </html>""", 200, {
            "X-Server": "sample",
            'Content-Type': 'text/plain; charset=utf-8'}

@app.route("/lab1/author")
def author():
    name = "Осягин Иван Дмитриевич"
    group = "FBI-22"
    faculty = "FB"

    return """<!doctype html>
        <html>
            <body>
                <p>Студент: """ + name + """</p>
                <p>Группа: """ + group + """</p>
                <p>Факультет: """ + faculty + """</p>
                <a href="/lab1/web">web</a>
            <body>
        </html>"""

@app.route('/lab1/oak')
def oak():
    path = url_for('static', filename='oak.jpg')
    css = url_for('static', filename='lab1.css')
    return '''
    <!doctype html>
    <html>
        <head>
            <link rel="stylesheet" href="''' + css + '''">
        </head>
        <body>
            <h1>Дуб</h1>
            <img src="''' + path + '''">
        </body>
    </html>
    '''  

count = 0
@app.route("/lab1/counter")
def counter():
    global count
    count += 1
    return '''
    <!doctype html>
    <html>
        <body>
            Сколько раз вы заходили: ''' + str(count) + '''
            <a href="/clear">очистить</a>
        </body>
    </html>
    '''  

@app.route('/lab1/info')
def info():
    return redirect("/lab1/author")

@app.route('/lab1/created')
def created():
    global create
    css = url_for('static', filename='lab1.css')
    if delete is True:
        return '''
        <!doctype html>
        <html>
            <head>
                <link rel="stylesheet" href="''' + css + '''">
            </head>
            <body>
                <h1>ТЫ ДОЛОМАЛ ЕГО, ЗАЧЕМ ИЗДЕВАТЬСЯ!?!?!?!? &#128544;</h1>
                <div><i>:(</i></div>
                <a href="/lab1/resource">Назад</a>
            </body>
        </html>
        ''', 400

    elif create is False:
        create = True
        path = url_for('static', filename='monster.webp')
        return '''
        <!doctype html>
        <html>
            <head>
                <link rel="stylesheet" href="''' + css + '''">
            </head>
            <body>
                <h1>Компьютер успешно ВКЛЮЧЕН! &#128520;</h1>
                <img src="''' + path + '''">
                <p><a href="/lab1/resource">Назад</a></p>
            </body>
        </html>
        ''', 201
    
    else:
        return '''
        <!doctype html>
        <html>
            <head>
                <link rel="stylesheet" href="''' + css + '''">
            </head>
            <body>
                <h1>ТЫ УЖЕ ВКЛЮЧИЛ КОМПЬЮТЕР, ЧЕГО ТЫ ХОЧЕШЬ!? &#128544;</h1>
                <div><i>:(</i></div>
                <a href="/lab1/resource">Назад</a>
            </body>
        </html>
        ''', 400

@app.route('/lab1/delete')
def delete():
    global create
    global delete
    css = url_for('static', filename='lab1.css')
    path = url_for('static', filename='broken.jpg')

    if delete is True or create is False:
        return '''
        <!doctype html>
        <html>
            <head>
                <link rel="stylesheet" href="''' + css + '''">
            </head>
            <body>
                <h1>ТЫ ЛИБО КОМПЬЮТЕР УЖЕ ДОЛОМАЛ, ЛИБО НЕ ВКЛЮЧИЛ</h1>
                <a href="/lab1/resource">Назад</a>
            </body>
        </html>
        ''', 400

    else:
        delete = True
        return '''
        <!doctype html>
        <html>
            <head>
                <link rel="stylesheet" href="''' + css + '''">
            </head>
            <body>
                <h1>Доигрался.... Компьютер сломан &#9760;</h1>
                <img src="''' + path + '''">
                <div><i>:(</i></div>
                <a href="/lab1/resource">Назад</a>
            </body>
        </html>
        ''', 200


@app.route('/lab1/resource')
def resource():
    global create
    global delete
    status = ''
    css = url_for('static', filename='lab1.css')
    if create is True:
        status = 'Вы включали компьютер &#128077;'
    else:
        status = 'Вы еще не включали компьютер &#128557;'
    return '''
    <!doctype html>
    <html>
        <head>
            <title>Лабораторная 1</title>
            <link rel="stylesheet" href="{}">
        </head>
        <body>
            <header>
                <h1>Статус игрового "зверя"</h1>
            </header>
            <main>
                <h1>{}</h1>
                <ul>
                    <li><a href="/lab1/created">Включить компютер</a></li>
                    <li><a href="/lab1/delete">Сломать компьютер</a></li>
                </ul>
            </main>
            <footer>
                &copy; Осягин Иван, ФБИ-22, 3 курс, 2024
            </footer>
        </body>
    </html>
    '''.format(css, status)

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

@app.route('/clear')
def clear():
    global count
    count = 0
    return redirect("/lab1/counter")

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

@app.route('/lab1')
def lab1():
    return '''
    <!doctype html>
    <html>
        <head>
            <title>Лабораторная 1</title>
        </head>
        <body>
            <header>
                <h1>НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных</h1>
            </header>
            <main>
                <h1>Лабораторная 1</h1>
                <p>Flask — фреймворк для создания веб-приложений на языке программирования Python, 
                использующий набор инструментов Werkzeug, а также шаблонизатор Jinja2. Относится к категории 
                так называемых микрофреймворков — минималистичных каркасов веб-приложений, 
                сознательно предоставляющих лишь самые базовые возможности.</p>
                <a href="/">Назад на главную</a>
                <h1>Список рутов</h1>
                <ul>
                    <li><a href="/lab1/web">web</a></li>
                    <li><a href="/lab1/author">author</a></li>
                    <li><a href="/lab1/oak">oak</a></li>
                    <li><a href="/lab1/counter">counter</a></li>
                    <li><a href="/lab1/info">info</a></li>
                    <li><a href="/lab1/resource">доп задание resource</a></li>
                    <li><a href="/lab1/gaming_monster">gaming_monster</a></li>
                </ul>
            </main>
            <footer>
                 &copy; Осягин Иван, ФБИ-22, 3 курс, 2024
            </footer>
        </body>
    </html>
    '''
@app.route('/error/400')
def error_400():
    return 'BAD REQUEST', 400

@app.route('/error/401')
def error_401():
    return 'UNAUTHORIZED', 401

@app.route('/error/402')
def error_402():
    return 'PAYMENT REQUIRED', 402

@app.route('/error/403')
def error_403():
    return 'FORBIDDEN', 403

@app.route('/error/405')
def error_405():
    return 'METHOD NOT ALLOWED', 405

@app.route('/error/418')
def error_418():
    return 'IM A TEAPOT', 418

@app.route('/lol500')
def lol500():
    1 / 0

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

@app.route('/lab1/gaming_monster')
def gamingpc():
    path = url_for('static', filename='pc.jpg')
    css = url_for('static', filename='lab1.css')
    return '''
    <!doctype html>
    <html>
        <head>
            <title>Лабораторная 1</title>
            <link rel="stylesheet" href="''' + css + '''">
        </head>
        <body>
            <main>
                <h1>Игровой «монстр»</h1>
                <p>Высшая похвала для компьютера — «зверский». Такая техника не тормозит и не «виснет», 
                он быстр, красив и надежен. Чтобы обладать такой «зверь-машиной», до сих пор было необходимо собирать 
                его самостоятельно, «разгоняя» процессор, отыскивая самые производительные и качественные комплектующие. 
                Однако за последний год многие производители компьютеров стали выпускать специальные «форсированные» версии своих ПК. 
                Одной из последних и наиболее мощных машин можно считать Dell XPS 720 H2C.</p>
                <img src="''' + path + '''">
                <p>Этого «монстра» компания Dell совсем недавно начала продавать в России. 
                Вообще, 700-я серия Dell — это машины топ-уровня, на доводку и «разгон» которых 
                разработчик не жалеет ни сил, ни средств. Результат, как правило, получался достойным, 
                естественно, за немалые деньги заказчика. Так вышло и на этот раз.</p>
                <p>Не стоит путать обычную 720-ю серию Dell c XPS 720 H2C. Первый представляет из себя пусть и высокопроизводительный, 
                но рядовой десктоп, которых на рынке достаточно много, практически каждый производитель способен предложить аналогичный продукт. 
                XPS 720 H2C — совсем другое дело.</p>
                <p>В сухой строчке спецификации на себя сразу обращает внимание фраза «Частота процессора Intel Core 2 Extreme QX6800 — 3,46 ГГц». 
                Процессоров с такой частотой Intel не выпускает. Даже у новейшего QX9650, которого еще нет в нашей стране, частота только 3 ГГц. 
                Разгадка проста — четырехъядерный процессор QX6800 разогнан на заводе специалистами Dell. Чем это отличается от «разгона» в домашних условиях? 
                «Разгон» в заводских условиях совершенно безопасен для компьютера и для пользователя, который не будет страдать от снижения стабильности 
                работы ПК, что так часто бывает при домашнем «разгоне».</p>
                <p>Производительность в играх зависит от мощности видеокарты. А в последнее время — и от их количества, 
                ведь производители видеоакселераторов уже разработали технологии, позволяющие устанавливать несколько видеокарт в один ПК. 
                В отличие от компьютеров Dell обычной 720-й серии у H2C сразу установлены две мощнейшие видеокарты nVidia GeForce 8800 GTX с 
                768 Мб видеопамяти каждая. Мы затрудняемся назвать игры, которые бы требовали такой мощности, да и вряд ли такие появятся в ближайшем году.</p>
                <p>Более того, в XPS 720 H2C используется графический ускоритель AGEIA(r) PhysXTM, который делает игры еще более реальными. 
                В играх, которые поддерживают работу с данным ускорителем, каждый волосок или пылинка, как в реальной жизни, 
                реагируют на малейшее дуновение ветра благодаря тысячам «интеллектуальных крупиц» игрового изображения, которые поддерживает PhysX.</p>
                <p>Объем оперативной памяти в 4 Гб сделает честь любому сетевому серверу, с такими 
                показателями можно в принципе не беспокоиться об оптимизации производительности компьютера еще ближайшие несколько лет.</p>
            </main>
            <footer>
                 &copy; Осягин Иван, ФБИ-22, 3 курс, 2024
            </footer>
        </body>
    </html>
    ''', 200, {
        'Content-Language': 'ru', 
        'Who-Made-It': 'Ivan Osyagin', 
        'What-Have-I-Ate-Today': 'Pelmeni' 
    }

@app.route("/lab2/a")
def a():
    return 'без слэша'

@app.route("/lab2/a2")
def a2():
    return 'со слешем'

flower_list = ['роза', "тюльпан", "ЖИМОЛОСТЬ)", "Глеб", "Ананас"]
@app.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    css = url_for('static', filename='lab1.css')
    
    if flower_id >= len(flower_list):
        return f'''
        <!doctype html>
        <html>
            <head>
                <link rel="stylesheet" href="{css}">
            </head>
            <body>
            <h1>ТАКОГО ЦВЕТОЧКА НЕТ :(</h1>
            <p>Всего цветков: {len(flower_list)}</p>
            <a href="/lab2/flowers">Вернуться на главную</a>
            </body>
        </html>
        ''', 404
    else:
        flower_name = flower_list[flower_id]
        return f'''
        <!doctype html>
        <html>
            <head>
                <link rel="stylesheet" href="{css}">
            </head>
            <body>
            <h1>Цветок: {flower_name}</h1>
            <p>Номер цветка: {flower_id}</p>
            <p>Всего цветков: {len(flower_list)}</p>
            <p>Полный список: {flower_list}</p>
            <a href="/lab2/flowers">Вернуться на главную</a>
            </body>
        </html>
        '''

@app.route('/lab2/flowers/delete')
def deleteFlower():
    global flower_list
    flower_list = []
    return redirect('/lab2/flowers')

@app.route('/lab2/add_flower/', defaults={'name': ''})
@app.route('/lab2/add_flower/<name>')
def add_flower(name):
    css = url_for('static', filename='lab1.css')
    if name == '':
        return f'''
    <!doctype html>
    <html>
        <head>
            <link rel="stylesheet" href="{css}">
        </head>
        <body>
        <h1>Вы не написали название цветка!</h1>
        <p>Всего цветков: {len(flower_list)}</p>
        <p>Полный список: {flower_list}</p>
        <a href='>
        </body>
    </html>
    ''', 400
    else:
        flower_list.append(name)
        return f'''
    <!doctype html>
    <html>
        <head>
            <link rel="stylesheet" href="{css}">
        </head>
        <body>
        <h1>Цветок добавлен!</h1>
        <p>Название нового цветка: {name}</p>
        <p>Всего цветков: {len(flower_list)}</p>
        <p>Полный список: {flower_list}</p>
        <a href='>
        </body>
    </html>
    '''
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