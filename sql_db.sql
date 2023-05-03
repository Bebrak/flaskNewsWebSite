create table if not exists news (
id integer primary key autoincrement,
news_title text not null,
text_small text not null,
text_big text not null,
news_img text not null
);