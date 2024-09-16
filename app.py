from flask import Flask, url_for, redirect

app = Flask(__name__)

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
    return '''
<!doctype html>
<html>
    <body>
        <h1>Cоздано успешно</h1>
        <div><i>что-то задано...</i></div>
    </body>
</html>
''', 201

@app.errorhandler(404)
def not_found(err):
    path = url_for('static', filename='404.jpg')
    return '''
    <!doctype html>
    <html>
        <body>
            <img src="''' + path + '''">
        </body>
    </html>
    '''  

@app.route('/clear')
def clear():
    global count
    count = 0
    return redirect("/lab1/counter")