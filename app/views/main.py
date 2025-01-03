from flask import Blueprint, render_template, redirect, url_for, request

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('index.html')
