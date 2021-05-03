"""
Jiaming Yu U72316560
News Analyzer APP
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
from nlp.convert import *
from news.newsapi import *
from database.db import *

import os
from flask import jsonify
from flask_cors import CORS

import json


app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24) 
cors = CORS(app, supports_credentials=True, origins='http://localhost:3000')

#where database locally
#app.config['DATABASE'] = r'/home/ubuntu/news-analyzer-JimY233/mydatabase.db'
app.config['DATABASE'] = r'../mydatabase.db'

#where pdf files saved locally
#app.config['UPLOAD_FOLDER'] = '/home/ubuntu/news-analyzer-JimY233/file_uploader/pdfexamples/'
app.config['UPLOAD_FOLDER'] = '../upload_files'

@app.route('/api/logout')
def home():
   session.clear()
   #return render_template('login.html')

   return redirect('http://localhost:3000/')

@app.route('/api/login', methods=['GET', 'POST'])
def login():
   error = ""
   if request.method == 'POST':
      data = request.get_json()
      print(request, data)
      if data is not None:
         username = data['username']
         password = data['password']

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
            print(session)
            cursor.execute('create table if not exists files (user_id, file_id, text, sentiment)')
            cursor.execute('create table if not exists news (user_id, id INTEGER PRIMARY KEY, keyword, title, url, content, sentiment)')
            files_records = cursor.execute('select file_id from files where user_id=?', (username,)).fetchall()
            news_records = cursor.execute('select id, title, url from news where user_id=?', (username,)).fetchall()
            cursor.close()
            conn.close()

            #return render_template('upload.html', user = username, filenames = values)
            return jsonify({
                    'status' : 'success',
                    'user' : username,
            })

         cursor.close()
         conn.close()
         #flash(error)

   #return render_template('login.html')
   return jsonify({
         'status' : 'error',
         'message' : error
         })

@app.route('/api/register', methods=('GET', 'POST'))
def register():
   error = ""
   if request.method == 'POST':
      data = request.get_json()
      username = data['username']
      password = data['password']
      
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
         #return render_template('login.html')
         return jsonify({
                 'status' : 'success'
            })

      cursor.close()
      conn.close()
      #flash(error)

   #return render_template('register.html')
   return jsonify({
           'status' : 'error',
           'message' : error
       })

@app.route('/api/current_user', methods = ['GET'])
def get_current_user():
   print(session, session.get('user_id'))
   return jsonify({
      'user_id': session.get('user_id')})

@app.route('/api/getrecords', methods = ['GET', 'POST'])
def getrecords():
   error = None
   user_id = session.get('user_id')
   if user_id is None:
      #return render_template('login.html')
      return jsonify({
            'status' : 'error',
            'error' : 'session failed'
         })
   
   conn = sqlite3.connect(app.config['DATABASE'])
   cursor = conn.cursor()
   files_records = cursor.execute('select file_id from files where user_id=?', (user_id,)).fetchall()
   news_records = cursor.execute('select id, title, url from news where user_id=?', (user_id,)).fetchall()
   cursor.close()
   conn.close()
   return jsonify({
         'status' : 'success',
         'user' : user_id,
         'filenames' : files_records,
         'newsnames' : news_records
         })

@app.route('/api/rename', methods = ['GET', 'POST'])
def rename_file():
   user_id = session.get('user_id')
   if user_id is None:
      #return render_template('login.html')
      return jsonify({
            'status' : 'error',
            'error' : 'session failed'
         })  

   data = request.get_json()
   file_id = data['file_id']
   new_file_id = data['new_file_id']
   if file_id is None or new_file_id is None:
      return jsonify({
            'status' : 'error',
            'error' : 'please provide file_id and new_file_id'
         })
   conn = sqlite3.connect(app.config['DATABASE'])
   cursor = conn.cursor()
   if cursor.execute('SELECT file_id FROM files WHERE user_id = ? and file_id = ?', (user_id,file_id)).fetchone() is not None:
      cursor.execute('update files set file_id = ? where user_id = ? and file_id = ?',(new_file_id,user_id,file_id))
      cursor.close()
      conn.close()
      src = os.path.join(app.config['UPLOAD_FOLDER'], user_id, file_id)
      dst = os.path.join(app.config['UPLOAD_FOLDER'], user_id, new_file_id)
      os.rename(src,dst)
      return jsonify({
         'status' : 'success',
         'new_file_id' : new_file_id
      })  
   else:
      cursor.close()
      conn.close()
      return jsonify({
         'status' : 'error',
         'error' : 'file_id not inside the database'
      }) 

      
	
@app.route('/api/upload', methods = ['GET', 'POST'])
#@app.route('/upload/<user_id>', methods = ['GET', 'POST'])
def upload_file():
   user_id = session.get('user_id')
   if user_id is None:
      #return render_template('login.html')
      return jsonify({
            'status' : 'error',
            'error' : 'session failed'
         })

   if request.method == 'POST':
      print(request)
      if 'file' in request.files:
         f = request.files['file']
         if f.filename != '':
            filename = secure_filename(f.filename)
            current_user_path = os.path.join(app.config['UPLOAD_FOLDER'], user_id)
            if not os.path.exists(current_user_path):
               os.makedirs(current_user_path)
            path = os.path.join(app.config['UPLOAD_FOLDER'], user_id, filename)
            f.save(path)
            logging.info("Files saved")

            page_content = ""
            if os.path.splitext(filename)[-1][1:] == "pdf":
               pdfFileObj = open(path, 'rb') 
               pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
               totalpage = pdfReader.numPages
               logging.info("Number of pages:",totalpage)
               for page in range(totalpage): 
                  pageObject = pdfReader.getPage(page) 
                  page_content = page_content + pageObject.extractText()
               logging.info("PDF converted to text")
               pdfFileObj.close() 
            elif os.path.splitext(filename)[-1][1:] == "txt":   
               with open(path, "r",encoding='utf-8') as txtfile:
                  page_content = txtfile.read()
               logging.info("text received")
            else:
               page_content = filename

            #nlp analysis
            #sentiment = ""
            sentiment = NLP_analyze(page_content)
            #database insert
            conn = sqlite3.connect(app.config['DATABASE'])
            cursor = conn.cursor ()
            cursor.execute('create table if not exists files (user_id, file_id, text, sentiment)')
            records = cursor.execute(
               'SELECT file_id FROM files WHERE user_id = ?', (user_id,)
            ).fetchall()
            updated = False
            for record in records:
               if record[0] == filename:
                  cursor.execute('update files set text = ?, sentiment = ? where user_id = ? and file_id = ?',(page_content,sentiment,user_id,filename))
                  updated = True
            if updated:
               #flash('file uploaded and updated successfully')
               info = 'file uploaded and updated successfully'
            else:
               cursor.execute('insert into files values(?,?,?,?)',(user_id,filename,page_content,sentiment))
               #flash('file uploaded and saved successfully')
               info = 'file uploaded and saved successfully'
            cursor.close()  
            conn.commit()   
            conn.close()

         #f.filename=='' i.e. user did not select a file but click upload
         else:
            #flash("no files selected")
            error = "no files selected"
            return jsonify({
               'status' : 'error',
               'error' : error,
               'user' : user_id
               })
      
   #database search
   conn = sqlite3.connect(app.config['DATABASE'])
   cursor = conn.cursor()
   #cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
   #Tables=cursor.fetchall()
   #logging.info("Tables in the databse:",Tables)
   records = cursor.execute('select file_id from files where user_id=?', (user_id,)).fetchall()
   cursor.close()
   conn.close()

   #return render_template('upload.html', user = user_id, filenames = records)
   return jsonify({
      'status' : 'success',
      'info' : info,
      'user' : user_id,
      'uploaded' : filename,
      'filenames' : records
      })

@app.route('/api/multiupload', methods = ['GET', 'POST'])
#@app.route('/upload/<user_id>', methods = ['GET', 'POST'])
def multiupload_file():
   user_id = session.get('user_id')
   if user_id is None:
      #return render_template('login.html')
      return jsonify({
            'status' : 'error',
            'error' : 'session failed'
         })

   if request.method == 'POST':
      files = request.files.getlist("file")
      for f in files:
         if f.filename != '':
            filename = secure_filename(f.filename)
            current_user_path = os.path.join(app.config['UPLOAD_FOLDER'], user_id)
            if not os.path.exists(current_user_path):
               os.makedirs(current_user_path)
            path = os.path.join(app.config['UPLOAD_FOLDER'], user_id, filename)
            f.save(path)
            logging.info("Files saved")

            page_content = ""
            if os.path.splitext(filename)[-1][1:] == "pdf":
               pdfFileObj = open(path, 'rb') 
               pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
               totalpage = pdfReader.numPages
               logging.info("Number of pages:",totalpage)
               for page in range(totalpage): 
                  pageObject = pdfReader.getPage(page) 
                  page_content = page_content + pageObject.extractText()
               logging.info("PDF converted to text")
               pdfFileObj.close() 
            elif os.path.splitext(filename)[-1][1:] == "txt":   
               with open(path, "r",encoding='utf-8') as txtfile:
                  page_content = txtfile.read()
               logging.info("text received")
            elif os.path.splitext(filename)[-1][1:] == "docx": 
               docxfile = docx.opendocx(path)
               text_list = docx.getdocumenttext(docxfile)
               page_content = " ".join(text_list)
            else:
               page_content = filename
            #nlp analysis
            #sentiment = ""
            sentiment = NLP_analyze(page_content)
            #database insert
            conn = sqlite3.connect(app.config['DATABASE'])
            cursor = conn.cursor ()
            cursor.execute('create table if not exists files (user_id, file_id, text, sentiment)')
            records = cursor.execute(
               'SELECT file_id FROM files WHERE user_id = ?', (user_id,)
            ).fetchall()
            updated = False
            for record in records:
               if record[0] == filename:
                  cursor.execute('update files set text = ?, sentiment = ? where user_id = ? and file_id = ?',(page_content,sentiment,user_id,filename))
                  updated = True
            if updated:
               #flash('file uploaded and updated successfully')
               info = 'file uploaded and updated successfully'
            else:
               cursor.execute('insert into files values(?,?,?,?)',(user_id,filename,page_content,sentiment))
               #flash('file uploaded and saved successfully')
               info = 'file uploaded and saved successfully'
            cursor.close()  
            conn.commit()   
            conn.close()
      
   #database search
   conn = sqlite3.connect(app.config['DATABASE'])
   cursor = conn.cursor()
   #cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
   #Tables=cursor.fetchall()
   #logging.info("Tables in the databse:",Tables)
   records = cursor.execute('select file_id from files where user_id=?', (user_id,)).fetchall()
   cursor.close()
   conn.close()

   #return render_template('upload.html', user = user_id, filenames = records)
   return jsonify({
      'status' : 'success',
      'info' : info,
      'user' : user_id,
      'uploaded' : filename,
      'filenames' : records
      })

'''
@app.route('/api/select', methods = ['GET', 'POST'])
def file_select():
   error = None
   user_id = session.get('user_id')
   if user_id is None:
      #return render_template('login.html')
      return jsonify({
            'status' : 'error',
            'error' : 'session failed'
         })
   
   conn = sqlite3.connect(app.config['DATABASE'])
   cursor = conn.cursor()
   files_records = cursor.execute('select file_id from files where user_id=?', (user_id,)).fetchall()
   news_records = cursor.execute('select id, title from news where user_id=?', (username,)).fetchall()
   cursor.close()
   conn.close()

   data = request.get_json()
   select = data['select']
   if request.method == 'POST':
      if not select:
         error = 'Please enter filename to be selected to analysis.'
         #flash(error)
      else:
         for record in files_records:
            if record[0] == select:
               session['file_id'] = record[0]
               #return render_template('query.html', user = user_id,  filenames = records, selected = select)
               return jsonify({
                    'status' : 'success',
                    'user' : user_id,
                    'filenames' : files_records,
                    'newsnames' : news_records,
                    'file_id': select
                    })
         for record in news_records:
            if file_id.isdigit() and record[0] == int(select) or record[1] == select:
                session['file_id'] = record[0]
                return jsonify({
                    'status' : 'success',
                    'user' : user_id,
                    'filenames' : files_records,
                    'newsnames' : news_records,
                    'file_id': select
                    })

         #flash("wrong file name selected")
         error = "wrong file name selected"

   #return render_template('select.html', user = user_id,  filenames = records)
   return jsonify({
        'status' : 'error',
        'user' : user_id,
        'filenames' : records,
        'error' : error
        })

@app.route('/api/query', methods = ['GET', 'POST'])
def file_query():
   error = None
   user_id = session.get('user_id')
   if user_id is None:
      #return render_template('login.html')
      return jsonify({
            'status' : 'error',
            'error' : 'session failed'
         })

   data = request.get_json()
   if(data is not None):
       file_id = data['file_id']
       if file_id is None:
            return jsonify({
                    'status' : 'error',
                    'error' : 'no file_id'
                    })

   conn = sqlite3.connect(app.config['DATABASE'])
   cursor = conn.cursor()
   files_records = cursor.execute('select file_id from files where user_id=?', (user_id,)).fetchall()
   news_records = cursor.execute('select id, title from news where user_id=?', (username,)).fetchall()

   content = ""
   keyword = ""
   freq = 0
   sentiment = {}
   if request.method == 'POST':
        for record in files_records:
            if record[0] == file_id:
               session['file_id'] = record[0]
               cursor.execute('select text from files where user_id=? and file_id=?', (user_id,file_id))
        for record in news_records:
            if file_id.isdigit() and record[0] == int(file_id) or record[1] == file_id:
                session['file_id'] = record[0]
                cursor.execute('select content from news where user_id=? and file_id=?', (user_id,file_id))
        content = cursor.fetchall()
        text = convert(content)
        keyword = data['keyword']
        freq = 0
        if keyword is not None:
            freq = search_nlp(keyword,content)
        sentiment = NLP_analyze(text)

   cursor.close()
   conn.close()
   return jsonify({
        'status' : 'success',
        'user' : user_id,
        'filenames' : files_records,
        'newsnames' : news_records,
        'file_id': file_id,
        'search' : keyword,
        'frequency' : freq,
        'sentiment' : sentiment
        })
'''

@app.route('/api/show/<file_id>', methods = ['GET', 'POST'])
def file_show(file_id):
   error = ""
   user_id = session.get('user_id')
   if user_id is None:
      return jsonify({
            'status' : 'error',
            'error' : 'session failed'
         })
   if request.method == 'POST':
      data = request.get_json()
      file_id = data['file_id']
      if file_id is None:
         return jsonify({
               'status' : 'error',
               'error' : 'please provide file_id'
            })

   text = ""
   conn = sqlite3.connect(app.config['DATABASE'])
   cursor = conn.cursor()
   records = cursor.execute('select file_id from files where user_id=?', (user_id,)).fetchall()
   flag = False
   for record in records:
      if record[0] == file_id:
         session['file_id'] = record[0]
         flag = True
      error = "wrong file name selected"
   if(flag):
      cursor.execute('select text from files where user_id=? and file_id=?', (user_id,file_id))
      content = cursor.fetchall()
      cursor.execute('select sentiment from files where user_id=? and file_id=?', (user_id,file_id))
      sentiment = cursor.fetchall()
      text = convert(content)
      emotion = convert(sentiment)
      cursor.close()
      conn.close()
   else:
      return jsonify({
         'status' : 'error',
         'error' : error
      })
      cursor.close()
      conn.close()

   return jsonify({
         'status' : 'success',
         'content' : text,
         'sentiment' : emotion
      })

@app.route('/api/ingest', methods = ['GET', 'POST'])
def news_ingest():
   user_id = session.get('user_id')
   if user_id is None:
      #return render_template('login.html')
      return jsonify({
            'status' : 'error',
            'error' : 'session failed'
         })

   error = ""
   global articles
   if request.method == 'POST':
      titles = []
      contents = []
      urls = []
      articles = []
      data = request.get_json()
      if data is not None:
         num = data['num']
         keyword = data['keyword']
         if not num:
            error = 'Please enter number of news required.'
            #flash(error)
         elif not keyword:
            error = 'Please enter key word.'
            #flash(error)
         else:
            try:
               num = int(num)
            except:
               num = 1
               # flash("Invalid number and thus use default number = 1")
            if num >=1 and num <= 100:
               response_json = newsapi(keyword,num)
               # conn = sqlite3.connect(app.config['DATABASE'])
               # cursor = conn.cursor ()
               # cursor.execute('create table if not exists news (user_id, id INTEGER PRIMARY KEY, keyword, title, url, content, sentiment)')
               # existed = False
               # records = cursor.execute('select id, title from news where user_id=?', (user_id,)).fetchall()
               for i in response_json['articles']:
                  titles.append(i['title'])
                  contents.append(i['title']+" "+i['content'])
                  urls.append(i['url'])
                  #sentiment = ""
                  sentiment = NLP_analyze(i['title']+" "+i['content'])
                  articles.append([user_id,keyword,i['title'],i['url'],i['title']+" "+i['content'],sentiment])
               #    for record in records:
               #       if i['title'] == record[1]:
               #          existed = True
               #    if not existed:
               #       cursor.execute('insert into news (user_id, keyword, title, url, content, sentiment) values(?,?,?,?,?,?)',(user_id, keyword, i['title'], i['url'], i['title']+" "+i['content'], sentiment))
               # records = cursor.execute('select id, title, url from news where user_id=? and keyword = ?', (user_id,keyword)).fetchall()
               # cursor.close()  
               # conn.commit()   
               # conn.close()
               return jsonify({
                  'status' : 'success',
                  'user' : user_id,
                  'newsnames' : articles
                  })
      
   return jsonify({
      'status' : 'error',
      'error' : error,
      'user' : user_id,
      })

@app.route('/api/save_news/<title>', methods = ['GET', 'POST'])
def save_news(title):
   user_id = session.get('user_id')
   if user_id is None:
      #return render_template('login.html')
      return jsonify({
            'status' : 'error',
            'error' : 'session failed'
         })
   conn = sqlite3.connect(app.config['DATABASE'])
   cursor = conn.cursor ()
   cursor.execute('create table if not exists news (user_id, id INTEGER PRIMARY KEY, keyword, title, url, content, sentiment)')
   existed = False
   saved = False
   for article in articles:
      existed = True
      if article[2] == title:
         if len(list(cursor.execute('select * from news where title = ?',(title,)))) == 0:
            print(title)
            cursor.execute('insert into news (user_id, keyword, title, url, content, sentiment) values(?,?,?,?,?,?)',(article[0], article[1], article[2], article[3], article[4],article[5]))
            saved = True
   cursor.close()  
   conn.commit()   
   conn.close()

   if not saved:
      return jsonify({
         'status' : 'error',
         'error' : 'news already saved in the database',
         'newsnames' : title
         })

   if not existed:
      return jsonify({
         'status' : 'error',
         'error' : 'wrong newsnames',
         'newsnames' : title
         })

   return jsonify({
         'status' : 'success',
         'user' : user_id,
         'newsnames' : title
         })

@app.route('/api/shownews/<file_id>', methods = ['GET', 'POST'])
def news_show(file_id):
   error = ""
   user_id = session.get('user_id')
   if user_id is None:
      return jsonify({
            'status' : 'error',
            'error' : 'session failed'
         })
   if request.method == 'POST':
      data = request.get_json()
      file_id = data['file_id']
      if file_id is None:
         return jsonify({
               'status' : 'error',
               'error' : 'please provide file_id'
            })

   text = ""
   conn = sqlite3.connect(app.config['DATABASE'])
   cursor = conn.cursor()
   records = cursor.execute('select title from news where user_id=?', (user_id,)).fetchall()
   flag = False
   for record in records:
      print(record[0])
      if record[0] == file_id:
         session['file_id'] = record[0]
         flag = True
      error = "wrong file name selected"
      
   if(flag):
      cursor.execute('select content from news where user_id=? and title=?', (user_id,file_id))
      content = cursor.fetchall()
      cursor.execute('select sentiment from news where user_id=? and title=?', (user_id,file_id))
      sentiment = cursor.fetchall()
      cursor.execute('select url from news where user_id=? and title=?', (user_id,file_id))
      url = cursor.fetchall()
      text = convert(content)
      emotion = convert(sentiment)
      cursor.close()
      conn.close()
   else:
      cursor.close()
      conn.close()
      return jsonify({
         'status' : 'error',
         'error' : error
      })

   return jsonify({
         'status' : 'success',
         'url' : url,
         'content' : text,
         'sentiment' : emotion
      })


if __name__ == '__main__':
  app.run(debug = True)
  #app.run(host='0.0.0.0', port=443)

