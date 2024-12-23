from flask import Flask, Blueprint, render_template, request, redirect, url_for, session

rgz = Blueprint('rgz', __name__)

@rgz.route('/rgz/')
def main():
    return render_template('/rgz/main.html')