from flask import Flask, url_for, redirect, render_template, abort, request ,redirect
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4

app = Flask(__name__)

app.secret_key = 'GLEB'

app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)

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
                    <li><a href="/lab3">Третья лабораторная</a></li>
                    <li><a href="/lab4">Четвертая лабораторная</a></li>
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
