from flask import Flask, render_template, url_for
import os
from config import Config
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page404.html', title='Страница не найдена')

if __name__ == "__main__":
    app.run()