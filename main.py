import datetime
import os
import sqlite3
from flask import Flask, render_template, g
from fdatabase import FDataBase
from config import Config
import requests
from bs4 import BeautifulSoup
from app import app, connect_db

def update_news():
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

if __name__ == "__main__":
    update_news()
