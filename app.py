from flask import Flask

app = Flask(__name__)

@app.route('/web')
def web():
    return """<!doctype html>
        <html>
            <body>
                <h1>web-server on flask</h1>
                <a href="/author">author</a>
            <body>
        </html>"""

@app.route("/author")
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
                <a href="/web">web</a>
            <body>
        </html>"""