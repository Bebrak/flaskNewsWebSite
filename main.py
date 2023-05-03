import datetime
import os
import sqlite3
from flask import Flask, render_template, g
from fdatabase import FDataBase
from config import Config
import requests
from bs4 import BeautifulSoup
from app import app, connect_db

def update_news(count_of_news=3):
    url = 'https://www.bragazeta.ru/'
    db = connect_db()
    db = FDataBase(db)
    # time.sleep(5)
    response = requests.get(url)
    bs = BeautifulSoup(response.text, "lxml")
    # n_title = bs.find('div', class_="col-md-6 order-sm-0 order-md-1 oder-lg-1 order-first main-news-article")
    # n_text = bs.find('div', class_="col-md-6 order-sm-0 order-md-1 oder-lg-1 order-first main-news-article")
    # n_text = bs.findall('p', class_='card-text')
    n_title = bs.find_all('h1', class_='title-small')
    print(n_title)
if __name__ == "__main__":
    update_news()
