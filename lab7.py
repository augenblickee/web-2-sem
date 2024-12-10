from flask import Blueprint, render_template, abort, request
from random import randint
import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3
from os import path


lab7 = Blueprint('lab7', __name__)


@lab7.route('/lab7/')
def lab():
    return render_template('/lab7/lab7.html')


films = [
    {
        'title': 'Gleb Kubra',
        'title_ru': 'Глеб Кубра',
        'year': 2003,
        'description': (
            'Глеб Кубра, сын простых рабочих, с детства мечтал о большом успехе. '
            'Он учился на отлично, проявлял недюжинный ум и невероятную хватку. В юном возрасте '
            'Глеб начинает свой путь в бизнесе, быстро пробиваясь сквозь конкуренцию и '
            'преодолевая препятствия. Его амбиции и нестандартный подход к ведению дел '
            'привлекают внимание крупных игроков, и вскоре Глеб становится одним из самых богатых '
            'людей в стране. Однако его стремительный взлет сопровождается и падением, связанным '
            'с обвинениями в коррупции и мошенничестве.'
        ),
    },
    {
        'title': 'Cool mommy',
        'title_ru': 'Крутая мамочка',
        'year': 2020,
        'description': (
            '"Крутая мамочка" - это веселая и трогательная комедия о силе '
            'материнской любви и невероятных подвигах, которые способна совершить любая мама, чтобы защитить своих детей.'
        ),
    },
    {
        'title': 'Gabob',
        'title_ru': 'Габоб',
        'year': 1999,
        'description': (
            '"Габоб" - это жуткий фильм ужасов, который шокировал зрителей своей безжалостной жестокостью и '
            'мрачной атмосферой. Сюжет вращается вокруг древнего демонического существа, '
            'которое пробуждается в современном мире и начинает терроризировать небольшую деревню. '
            'Фильм, запрещенный в ряде стран за чрезмерное насилие и психологическое давление, погружает зрителей в '
            'мир абсолютного ужаса, где каждый поворот сюжета становится все более пугающим и непредсказуемым. "Габоб" - '
            'это не просто фильм, это испытание на прочность нервов, которое оставит вас в состоянии шока и трепета.'
        ),
    }
]

@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    return films


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    if id >= len(films):
        return abort(404)
    else:
        return films[id]
    

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    if id >= len(films):
        return abort(404)
    else:
        del films[id]
        return '', 204


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    if id >= len(films):
        return abort(404)
    else:
        film = request.get_json()
        if not film['title_ru'] and not film['title']:
            return {'description': 'Напишите название'}, 400
        elif not film['title_ru']:
            return {'description': 'Напишите русское название'}, 400
        elif not (2024 >= int(film['year']) >= 1895) or film['year'] == '':
            return {'description': 'Дата введена некорректно'}, 400
        elif film['description'] == '':
            return {'description': 'Заполните описание'}, 400
        elif len(film['description']) > 2000:
            return {'description': 'Максимальная длинна описания - 2000 символов'}, 400
    
        if film['title_ru'] and not film['title']:
            film['title'] = film['title_ru']
        films[id] = film
        return films[id]
    

@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    film = request.get_json() 
    if not film or not all(k in film for k in ('title', 'title_ru', 'year', 'description')):
        return abort(400, "Invalid film data") 
    else:
        if not film['title_ru'] and not film['title']:
            return {'description': 'Напишите название'}, 400
        elif not film['title_ru']:
            return {'description': 'Напишите русское название'}, 400
        elif not (2024 >= int(film['year']) >= 1895) or film['year'] == '':
            return {'description': 'Дата введена некорректно'}, 400
        elif film['description'] == '':
            return {'description': 'Заполните описание'}, 400
        elif len(film['description']) > 2000:
            return {'description': 'Максимальная длинна описания - 2000 символов'}, 400
        
        if film['title_ru'] and not film['title']:
            film['title'] = film['title_ru']
        films.append(film) 
        return {'id': len(films) - 1}, 201  