from flask import Blueprint, render_template, request, session, current_app
from random import randint
import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3
from os import path

lab7 = Blueprint('lab7', __name__)


@lab7.route('/lab7/')
def lab():
    return render_template('/lab7/lab7.html')