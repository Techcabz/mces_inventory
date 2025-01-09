from flask import Blueprint, render_template, redirect, url_for, request

main = Blueprint('main', __name__)


@main.route('/login')
def login():
    return render_template('auth/login.html')


@main.route('/register')
def register():
    return render_template('auth/register.html')


@main.route('/')
def home():
    return render_template('index.html')
