from apscheduler.schedulers.background import BackgroundScheduler
import datetime
import os
import sqlite3
from flask import Flask, render_template, g, abort
from config import Config
import requests
from bs4 import BeautifulSoup
from fdatabase import FDataBase

def update_news():
    try:
        n_url, n_img = [], []
        url = 'https://www.bragazeta.ru/'
        db = connect_db()
        db = FDataBase(db)
        response = requests.get(url)
        bs = BeautifulSoup(response.text, "lxml")
        n_title = bs.find('div', class_="col-md-6 order-sm-0 order-md-1 oder-lg-1 order-first main-news-article").find_all('h1', class_='title-small')
        n_text_small = bs.find('div', class_="col-md-6 order-sm-0 order-md-1 oder-lg-1 order-first main-news-article").find_all('p', class_='card-text')
        for i in bs.find_all('div', class_="media"):
            n_url.append(i.find('a', href=True)['href'])
            n_img.append(i.find('img', src=True)['src'])
        for i in range(len(n_title)):
            url = n_url[i]
            n_text_big = ''
            response = requests.get(url)
            bs = BeautifulSoup(response.text, "lxml")
            lst_text_big = bs.find('div', class_="video-show").find_all('p')
            for j in lst_text_big:
                n_text_big += j.text
                n_text_big += ' '
            n_text_big = n_text_big.strip()
            db.addMenu(n_title[i].text, n_text_small[i].text, n_text_big, n_img[i])
    except:
        print('Ошибка при получении данных')

sched = BackgroundScheduler(daemon=True)
sched.add_job(update_news,'interval',hours=3)
sched.start()

app = Flask(__name__)
app.config.from_object(Config)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'fdb.db')))
app.permanent_session_lifetime = datetime.timedelta(seconds=60)

def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
        return g.link_db

@app.route('/')
def index():
    db = get_db()
    database = FDataBase(db)
    return render_template('index.html', news=database.getNewsAnnoce(), news_left=database.getNewsAnnocePopular(), news_up=database.getNewsAnnoceRedactor())
@app.route('/news/<int:id_news>')
def showNews(id_news):
    db = get_db()
    database = FDataBase(db)
    news_title, text_big, news_img = database.getNewsPost(id_news)
    if not news_title:
        abort(404)
    return render_template('aticle.html', news_title=news_title, text_big=text_big, news_img=news_img)

@app.route('/about')
def about():
    return render_template('about.html')
def job():
    print('bebra')
@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page404.html', title='Страница не найдена')



if __name__ == "__main__":
    app.run()