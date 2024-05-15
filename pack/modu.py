# 宣告使用 sqlite3 模組
import sqlite3
import json
import csv


def create_database():
    '''建立資料表'''
    # 建立對檔案型資料庫 library.db 的物件參考
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    # 建立資料表: 【users】
    cursor.execute('''CREATE TABLE users
                    (user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    password TEXT NOT NULL)''')
    # 建立資料表: 【books】
    cursor.execute('''CREATE TABLE books
                    (book_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL,
                    publisher TEXT NOT NULL,
                    year INTEGER NOT NULL)''')
    conn.commit()
    conn.close()


def read_users_file(filename):
    '''讀取使用者檔後, insert into 資料表 users'''
    try:
        with open(filename, 'r', encoding="utf-8") as csvfile:
            users = csv.DictReader(csvfile)
            for u in users:
                if u['username'] and u['password']:
                    insert_users(u['username'], u['password'])
    except FileNotFoundError:
        print(f"{filename} 找不到檔案...")
        return 'error'
    except Exception as e:
        print('開檔發生錯誤...')
        print(f'錯誤代碼為：{e.errno}')
        print(f'錯誤訊息為：{e.strerror}')
        print(f'錯誤檔案為：{e.filename}')
        return 'error'


def read_books_file(filename):
    '''讀取圖書檔後, insert into 資料表 books'''
    try:
        with open(filename, 'r', encoding="utf-8") as jsonfile:
            books = json.load(jsonfile)
            for b in books:
                if b['title'] and b['author'] and b['publisher'] and b['year']:
                    insert_book(b['title'], b['author'], b['publisher'], b['year'])
    except FileNotFoundError:
        print(f"{filename} 找不到檔案...")
        return 'error'
    except Exception as e:
        print('開檔發生錯誤...')
        print(f'錯誤代碼為：{e.errno}')
        print(f'錯誤訊息為：{e.strerror}')
        print(f'錯誤檔案為：{e.filename}')
        return 'error'


def insert_book(title, author, publisher, year):
    '''insert into 資料表 books'''
    try:
        conn = sqlite3.connect('library.db')
        c = conn.cursor()
        c.execute("INSERT INTO books(title, author, publisher, year) SELECT ?, ?, ?, ? WHERE NOT EXISTS(SELECT 1 FROM books WHERE title=?);",
                  (title, author, publisher, year, title))
        if c.rowcount > 0:
            print(f"異動 {c.rowcount} 記錄")
        else:
            print(f"書名 {title} 已存在.")
        conn.commit()
    except sqlite3.Error as error:
        print(f"新增 books 作業發生錯誤：{error}")
    conn.close()


def insert_users(username, password):
    '''insert into 資料表 users'''
    try:
        conn = sqlite3.connect('library.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                  (username, password))
        conn.commit()
    except sqlite3.Error as error:
        print(f"新增 users 作業發生錯誤：{error}")
    conn.close()


def authenticate_user():
    '''檢查帳密是否正確'''
    try:
        username = input("請輸入帳號：")
        password = input("請輸入密碼：")
        conn = sqlite3.connect("library.db")
        c = conn.cursor()
        c.execute("SELECT username FROM users WHERE username=? AND password=?",
                  (username, password))
        user = c.fetchone()
        conn.close()
        if user:
            return True
        else:
            return False
    except sqlite3.Error as error:
        print(f"查詢 users 作業發生錯誤：{error}")
        return 'error'


def add_record():
    title = input("請輸入要新增的標題：")
    author = input("請輸入要新增的作者：")
    publisher = input("請輸入要新增的出版社：")
    year = input("請輸入要新增的年份：")
    if title and author and publisher and year:
        insert_book(title, author, publisher, year)
        list_records()
    else:
        print("=>給定的條件不足，無法進行新增作業")


def delete_record():
    title = input("請問要刪除哪一本書？：")
    if title:
        try:
            conn = sqlite3.connect("library.db")
            c = conn.cursor()
            c.execute("DELETE FROM books WHERE title=?", (title,))
            if c.rowcount > 0:
                print(f"異動 {c.rowcount} 記錄")
            else:
                print(f"書名 {title} 不存在.")
            conn.commit()
            conn.close()
            list_records()
        except sqlite3.Error as error:
            print(f"刪除 books 作業發生錯誤：{error}")
    else:
        print("=>給定的條件不足，無法進行刪除作業")


def modify_record():
    title = input("請問要修改哪一本書的標題？：")
    new_title = input("請輸入要更改的標題：")
    author = input("請輸入要更改的作者：")
    publisher = input("請輸入要更改的出版社：")
    year = input("請輸入要更改的年份：")
    if title and new_title and author and publisher and year:
        try:
            conn = sqlite3.connect("library.db")
            c = conn.cursor()
            c.execute("SELECT title,author,publisher,year FROM books WHERE title=?", (new_title,))
            result_all = c.fetchall()
            if result_all and title != new_title:
                print(f"書名 {new_title} 已存在.")
            else:
                try:
                    c.execute("UPDATE books SET title=?, author=?, publisher=?, year=? WHERE title=?",
                              (new_title, author, publisher, year, title))
                    if c.rowcount > 0:
                        print(f"異動 {c.rowcount} 記錄")
                    else:
                        print(f"書名 {title} 不存在.")
                    conn.commit()
                    conn.close()
                    list_records()
                except sqlite3.Error as error:
                    print(f"更新 books 作業發生錯誤：{error}")
        except sqlite3.Error as error:
            print(f"查詢 books 作業發生錯誤：{error}")
    else:
        print("=>給定的條件不足，無法進行修改作業")


def query_record():
    keyword = input("請輸入想查詢的關鍵字：")
    if keyword:
        try:
            conn = sqlite3.connect("library.db")
            c = conn.cursor()
            c.execute("SELECT title,author,publisher,year FROM books WHERE title LIKE ? OR author LIKE ?",
                      ('%'+keyword+'%', '%'+keyword+'%'))
            result_all = c.fetchall()
            print_records(result_all)
            conn.close()
        except sqlite3.Error as error:
            print(f"查詢 books 作業發生錯誤：{error}")
    else:
        print(f"關鍵字 {keyword} 無填值.")


def list_records():
    try:
        conn = sqlite3.connect("library.db")
        c = conn.cursor()
        c.execute("SELECT title,author,publisher,year FROM books ")
        result_all = c.fetchall()
        print_records(result_all)
        conn.close()
    except sqlite3.Error as error:
        print(f"查詢 books 作業發生錯誤：{error}")


def users_records(csvfile):
    '''檢查 users 是否有資料'''
    conn = sqlite3.connect("library.db")
    c = conn.cursor()
    try:
        c.execute("SELECT username,password FROM users ")
        result_all = c.fetchall()
        if not result_all:
            return read_users_file(csvfile)
    except sqlite3.Error as error:
        print(f"查詢 books 作業發生錯誤：{error}")
        return 'error'
    conn.close()


def books_records(jsonfile):
    '''檢查 books 是否有資料'''
    conn = sqlite3.connect("library.db")
    c = conn.cursor()
    try:
        c.execute("SELECT title,author,publisher,year FROM books ")
        result_all = c.fetchall()
        if not result_all:
            return read_books_file(jsonfile)
    except sqlite3.Error as error:
        print(f"查詢 books 作業發生錯誤：{error}")
        return 'error'
    conn.close()


def print_records(records):
    if records:
        print(f"|{'書名':{chr(12288)}^12}|{'作者':{chr(12288)}^12}|{'出版社':{chr(12288)}^12}|{'年份':^4}|")
        for row in records:
            print(f"|{row[0]:{chr(12288)}<12}|{row[1]:{chr(12288)}<12}|{row[2]:{chr(12288)}<12}|{row[3]:<6}|")
    else:
        print("無相符記錄")


def display_menu():
    print("")
    print(f"{'-'*19}")
    print(f"{'資料表 CRUD':{chr(12288)}^12}")
    print(f"{'-'*19}")
    print(f"{'1. 增加記錄':{chr(12288)}^12}")
    print(f"{'2. 刪除記錄':{chr(12288)}^12}")
    print(f"{'3. 修改記錄':{chr(12288)}^12}")
    print(f"{'4. 查詢記錄':{chr(12288)}^12}")
    print(f"{'5. 資料清單':{chr(12288)}^12}")
    print(f"{'-'*19}")
