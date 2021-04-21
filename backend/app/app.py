"""
Jiaming Yu U72316560
File Uploader Module
"""
import flask
from flask import Flask,render_template, request, redirect, url_for,flash,session

from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

import PyPDF2
import sqlite3
import os

import logging

#from nlp.nlp_search import *
#from nlp.NLPAPI import *

import os
from flask import jsonify

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24) 

#where database locally
#app.config['DATABASE'] = r'/home/ubuntu/news-analyzer-JimY233/mydatabase.db'
app.config['DATABASE'] = r'C:\Users\yjm57\OneDrive\Documents\GitHub\news-analyzer-JimY233\mydatabase.db'

#where pdf files saved locally
#app.config['UPLOAD_FOLDER'] = '/home/ubuntu/news-analyzer-JimY233/file_uploader/pdfexamples/'
#app.config['UPLOAD_FOLDER'] = 'C:/Users/user/Downloads/'
app.config['UPLOAD_FOLDER'] = 'C:/Users/yjm57/Downloads/'

@app.route('/')
def home():
   session.clear()
   #return render_template('login.html')
   return jsonify(
         login = False
    )

@app.route('/login', methods=['GET', 'POST'])
def login():
   error = None
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

            #return render_template('upload.html', user = username, filenames = values)
            return jsonify(
               login = True,
               error = error,
               user = username,
               filenames = values
            )

         cursor.close()
         conn.close()
         #flash(error)

   #return render_template('login.html')
   return jsonify(
         login = False,
         error = error
    )

@app.route('/register', methods=('GET', 'POST'))
def register():
   error = None
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
         #return render_template('login.html')
         return jsonify(
            signup = True
         )

      cursor.close()
      conn.close()
      #flash(error)

   #return render_template('register.html')
   return jsonify(
      signup = False,
      error = error
   )

	
@app.route('/upload', methods = ['GET', 'POST'])
#@app.route('/upload/<user_id>', methods = ['GET', 'POST'])
def upload_file():
   user_id = session.get('user_id')
   if user_id is None:
      #return render_template('login.html')
      return jsonify(
         login = False
    )

   if request.method == 'POST':
      if 'file' in request.files:
         f = request.files['file']
         if f.filename != '':
            filename = secure_filename(f.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            f.save(path)
            logging.info("PDF temporarily saved")

            page_content = ""
            pdfFileObj = open(path, 'rb') 
            pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
            totalpage = pdfReader.numPages
            logging.info("Number of pages:",totalpage)
            for page in range(totalpage): 
               pageObject = pdfReader.getPage(page) 
               page_content = page_content + pageObject.extractText()
            logging.info("PDF converted to text")

            #os.remove(path)
            #logging.info("PDF deleted")

            #database insert
            conn = sqlite3.connect(app.config['DATABASE'])
            cursor = conn.cursor ()
            cursor.execute('create table if not exists files (user_id, file_id, text)') 
            records = cursor.execute(
               'SELECT file_id FROM files WHERE user_id = ?', (user_id,)
            ).fetchall()
            updated = False
            for record in records:
               if record[0] == filename:
                  cursor.execute('update files set text = ? where user_id = ? and file_id = ?',(page_content,user_id,filename))
                  updated = True
            if updated:
               #flash('file uploaded and updated successfully')
               info = 'file uploaded and updated successfully'
            else:
               cursor.execute('insert into files values(?,?,?)',(user_id,filename,page_content))
               #flash('file uploaded and saved successfully')
               info = 'file uploaded and saved successfully'
            cursor.close()  
            conn.commit()   
            conn.close()

            pdfFileObj.close() 

         #f.filename=='' i.e. user did not select a file but click upload
         else:
            #flash("no files selected")
            error = "no files selected"
      
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
   return jsonify(
      user = user_id,
      filenames = records
   )


'''
@app.route('/select', methods = ['GET', 'POST'])
def file_select():
   error = None
   user_id = session.get('user_id')
   if user_id is None:
      #return render_template('login.html')
      return jsonify(
         login = False
      )
   
   conn = sqlite3.connect(app.config['DATABASE'])
   cursor = conn.cursor()
   records = cursor.execute('select file_id from files where user_id=?', (user_id,)).fetchall()
   cursor.close()
   conn.close()

   if request.method == 'POST' and 'selectedfile' in request.form:
      select = request.form['selectedfile']
      if not select:
         error = 'Please enter filename to be selected to analysis.'
         flash(error)
      else:
         for record in records:
            if record[0] == select:
               session['file_id'] = record[0]
               #return render_template('query.html', user = user_id,  filenames = records, selected = select)
               return jsonify(
                  select = True,
                  user = user_id,
                  filenames = records,
                  selected = select
               )

         #flash("wrong file name selected")
         error = "wrong file name selected"

   #return render_template('select.html', user = user_id,  filenames = records)
   return jsonify(
      select = False,
      error = error,
      user = user_id,
      filenames = records
   )



@app.route('/query', methods = ['GET', 'POST'])
def file_query():
   error = None
   user_id = session.get('user_id')
   if user_id is None:
      #return render_template('login.html')
      return jsonify(
         login = False
      )

   conn = sqlite3.connect(app.config['DATABASE'])
   cursor = conn.cursor()
   records = cursor.execute('select file_id from files where user_id=?', (user_id,)).fetchall()

   file_id = session.get('file_id')
   if file_id is None:
      #return render_template('select.html', user = user_id,  filenames = records)
      return jsonify(
         select = False,
         user = user_id,
         filenames = records
      )

   content = ""
   if request.method == 'POST':
      cursor.execute('select text from files where user_id=? and file_id=?', (user_id,file_id))
      content = cursor.fetchall()
      text = convert(content)
      if 'keyword' in request.form:
         keyword = request.form['keyword']
         if not keyword:
            error = 'Please enter key word.'
            #flash(error)
         else:
            freq = search_nlp(keyword,content)
            #return render_template('query.html', user = user_id,  filenames = records, selected = file_id, data=content, freq=freq)
            return jsonify(
               query = 1,
               error = error
               select = True,
               user = user_id,
               filenames = records,
               selected = file_id,
               data = content,
               freq = freq
            )
      else:
         sentiment = NLP_analyze(text)
         #return render_template('query.html', user = user_id,  filenames = records, selected = file_id, data=content, sentiment = sentiment)
         return jsonify(
            query = 2,
            error = error
            select = True,
            user = user_id,
            filenames = records,
            selected = file_id,
            data = content,
            sentiment = sentiment
         )
   cursor.close()
   conn.close()
   #return render_template('query.html', user = user_id,  filenames = records, selected = file_id)
   return jsonify(
      query = 0,
      error = error
      select = True,
      user = user_id,
      filenames = records,
      selected = file_id
   )
'''
if __name__ == '__main__':
  app.run(debug = True)
  #app.run(host='0.0.0.0', port=443)

