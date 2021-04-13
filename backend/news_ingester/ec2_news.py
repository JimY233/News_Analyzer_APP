"""
Jiaming Yu U72316560
News Ingester Module
"""

import flask
from flask import Flask,render_template, request, redirect, url_for,flash,session

from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

import PyPDF2
import sqlite3
import os

import logging

from nlp.nlp_search import *
from nlp.NLPAPI import *
from news.newsapi import *

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24) 

#where database locally
app.config['DATABASE'] = r'/home/ubuntu/news-analyzer-JimY233/mydatabase.db'
#app.config['DATABASE'] = r'C:\Users\yjm57\OneDrive\Documents\GitHub\news-analyzer-JimY233\mydatabase.db'

#where pdf files saved locally
app.config['UPLOAD_FOLDER'] = '/home/ubuntu/news-analyzer-JimY233/file_uploader/pdfexamples/'
#app.config['UPLOAD_FOLDER'] = 'C:/Users/user/Downloads/'
#app.config['UPLOAD_FOLDER'] = 'C:/Users/yjm57/Downloads/'

@app.route('/')
def home():
   session.clear()
   return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
   if request.method == 'POST':
      if 'username' in request.form and 'password' in request.form:
         username = request.form['username']
         password = request.form['password']

         conn = sqlite3.connect(app.config['DATABASE'])
         cursor = conn.cursor()
         cursor.execute('create table if not exists user (username, password)') 

         error = None
         user = cursor.execute(
             'SELECT * FROM user WHERE username = ?', (username,)
         ).fetchone()
         #print(user)
         if user is None:
            error = 'Incorrect username.'
         #user is tuple 0-username 1-password; to change this, we can use detect_types when connect
         elif not check_password_hash(str(user[1]), password):
            error = 'Incorrect password.'

         if error is None:
            session.clear()
            session['user_id'] = user[0]
            cursor.execute('create table if not exists files (user_id, file_id, text)')
            values = cursor.execute('select file_id from files where user_id=?', (username,)).fetchall()
            cursor.close()
            conn.close()

            return render_template('ingest.html', user = username, filenames = values)

         cursor.close()
         conn.close()
         flash(error)

   return render_template('login.html')

@app.route('/register', methods=('GET', 'POST'))
def register():
   if request.method == 'POST':
      username = request.form['username']
      password = request.form['password']
      
      conn = sqlite3.connect(app.config['DATABASE'])
      cursor = conn.cursor ()
      cursor.execute('create table if not exists user (username, password)') 
      
      error = None
      if not username:
         error = 'Username is required.'
      elif not password:
         error = 'Password is required.'
      elif cursor.execute(
         'SELECT username FROM user WHERE username = ?', (username,)
      ).fetchone() is not None:
         error = 'User {} is already registered.'.format(username)     

      if error is None:
         cursor.execute(
               'INSERT INTO user (username, password) VALUES (?, ?)',
               (username, generate_password_hash(password))
         )
         cursor.close()
         conn.commit() 
         conn.close()
         return render_template('login.html')

      cursor.close()
      conn.close()
      flash(error)

   return render_template('register.html')

	
@app.route('/ingest', methods = ['GET', 'POST'])
#@app.route('/upload/<user_id>', methods = ['GET', 'POST'])
def news_ingest():
   user_id = session.get('user_id')
   if user_id is None:
      return render_template('login.html')

   if request.method == 'POST':
      titles = []
      contents = []
      if 'num' in request.form and 'keyword' in request.form:
         num = request.form['num']
         keyword = request.form['keyword']
         if not num:
            error = 'Please enter number of news required.'
            flash(error)
         elif not keyword:
            error = 'Please enter key word.'
            flash(error)
         else:
            try:
               num = int(num)
            except:
               num = 1
               flash("Invalid number and thus use default number = 1")
            if num >=1 and num <= 100:
               response_json = newsapi(keyword,num)
               conn = sqlite3.connect(app.config['DATABASE'])
               cursor = conn.cursor ()
               cursor.execute('create table if not exists news (user_id, id INTEGER PRIMARY KEY, keyword, title, content)') 
               existed = False
               records = cursor.execute('select id, title from news where user_id=?', (user_id,)).fetchall()
               for i in response_json['articles']:
                  titles.append(i['title'])
                  contents.append(i['title']+" "+i['content'])
                  for record in records:
                     if i['title'] == record[1]:
                        existed = True
                  if not existed:
                     cursor.execute('insert into news (user_id, keyword, title, content) values(?,?,?,?)',(user_id,keyword,i['title'], i['title']+" "+i['content']))
               flash('news downloaded successfully')
               records = cursor.execute('select id, title from news where user_id=?', (user_id,)).fetchall()
               cursor.close()  
               conn.commit()   
               conn.close()

               return render_template('ingest.html', user = user_id, records = records, titles = titles, content = contents)

            else:
               flash("number out of range")
      
   conn = sqlite3.connect(app.config['DATABASE'])
   cursor = conn.cursor()
   records = cursor.execute('select id, title from news where user_id=?', (user_id,)).fetchall()
   cursor.close()
   conn.close()

   return render_template('ingest.html', user = user_id, records = records)

@app.route('/select', methods = ['GET', 'POST'])
def file_select():
   user_id = session.get('user_id')
   if user_id is None:
      return render_template('login.html')
   
   conn = sqlite3.connect(app.config['DATABASE'])
   cursor = conn.cursor()
   records = cursor.execute('select id, title from news where user_id=?', (user_id,)).fetchall()
   cursor.close()
   conn.close()

   if request.method == 'POST' and 'selectedfile' in request.form:
      select = request.form['selectedfile']
      if not select:
         error = 'Please enter filename to be selected to analysis.'
         flash(error)
      else:
         select = int(select)
         for record in records:
            if record[0] == select:
               session['news_id'] = record[0]
               return render_template('query.html', user = user_id,  filenames = records, selected = record[1])
         flash("wrong news id selected")

   return render_template('select.html', user = user_id,  filenames = records)


@app.route('/query', methods = ['GET', 'POST'])
def file_query():
   user_id = session.get('user_id')
   if user_id is None:
      return render_template('login.html')

   conn = sqlite3.connect(app.config['DATABASE'])
   cursor = conn.cursor()
   records = cursor.execute('select id, title from news where user_id=?', (user_id,)).fetchall()

   file_id = session.get('news_id')
   if file_id is None:
      return render_template('select.html', user = user_id,  filenames = records)

   content = ""
   if request.method == 'POST':
      cursor.execute('select content from news where user_id=? and id=?', (user_id,file_id))
      content = cursor.fetchall()
      text = convert(content)
      if 'keyword' in request.form:
         keyword = request.form['keyword']
         if not keyword:
            error = 'Please enter key word.'
            flash(error)
         else:
            freq = search_nlp(keyword,content)
            return render_template('query.html', user = user_id,  filenames = records, selected = file_id, data=content, freq=freq)
      else:
         sentiment = NLP_analyze(text)
         return render_template('query.html', user = user_id,  filenames = records, selected = file_id, data=content, sentiment = sentiment)

   cursor.close()
   conn.close()
   return render_template('query.html', user = user_id,  filenames = records, selected = file_id)

if __name__ == '__main__':
  #app.run(debug = True)
  app.run(host='0.0.0.0', port=443)

