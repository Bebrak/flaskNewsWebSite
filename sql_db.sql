create table if not exists news (
id integer primary key autoincrement,
news_title text not null,
news_text text not null
);