import sqlite3


def create_db():
    '''Вспомогательная функция для создания таблиц БД '''
    db = connect_db()
    with app.open_resource('sql_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()

class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def addMenu(self, news_title, text_small, text_big, news_img):
        try:
                sql = f"SELECT news_title FROM news WHERE news_title = ?"
                self.__cur.execute(sql, (news_title,))
                if self.__cur.fetchone() is None:
                    self.__cur.execute(f"INSERT INTO news VALUES (NULL, ?, ?, ?, ?)", (news_title, text_small, text_big, news_img))
                    self.__db.commit()
        except sqlite3.Error as e:
            print('Ошибка добавления в БД', str(e))
            return False
        return True


    def delMenu(self, id=0):
        try:
            if id == 0:
                self.__cur.execute(f"DELETE FROM news")
            else:
                self.__cur.execute(f"DELETE FROM news WHERE id=={id}")
            self.__db.commit()
        except sqlite3.Error as e:
            print('Ошибка удаления из БД', str(e))
            return False
        return True

    def getMenu(self):
        try:
            sql = """SELECT *  FROM news"""
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res: return res
        except:
            print('Ошибка чтения из БД')
            return []
    def getNewsAnnoce(self):
        try:
            self.__cur.execute(f"SELECT id, news_title, text_small, news_img FROM news ORDER BY id DESC LIMIT 10")
            res = self.__cur.fetchall()
            if res: return res
        except sqlite3.Error as e:
            print("Ошибка получения новостных статей из БД" + str(e))
        return []
    def getNewsPost(self, newsid):
        try:
            self.__cur.execute(f"SELECT  news_title, text_big, news_img FROM news WHERE id = {newsid} LIMIT 1")
            res = self.__cur.fetchone()
            if res: return res
        except sqlite3.Error as e:
            print("Ошибка получения новостной статьи из БД" + str(e))
        return (False, False)

if __name__ == '__main__':
    from app import app, connect_db
    db = connect_db()
    db = FDataBase(db)

    # create_db()                                                       # Создать ДБ

    # for i in db.getMenu():                                            #
    #     print(i['url'])                                               # Вывести данные из ДБ

    # print(db.delMenu(id=0))                                           # Удалить данные из ДБ

    # print(db.addMenu('История Россиифвфывфыв', 'Бебраааааyyasydyasdytay', 'ggggg', 'https://wudgleyd.ru/wp-content/uploads/2/9/a/29ac8e6d6e342b6917b24abb6d85e8f9.jpeg'))   # Добавить данные в ДБ
