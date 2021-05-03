# news-analyzer-app  
EC500 Final Project   
Group member:   
Jiaming Yu U72316560 jiamingy@bu.edu  
Wenqiang Yang U90452596 wqyang@bu.edu  

## User stories
**Secure File Uploader/Ingester**    
As a User, I want to  
upload various file types (pdf, docx,csv, etc.)  
be alerted if there were issues with uploading their files  
convert file types (e.g. from word, pdf to text)  
search for past files they have uploaded  
re-upload files when uploading fails  
secure uploading process  
keep my content private and safe  

**Text NLP Analysis:**  
As a user, I want to  
basic search functionality using keywords  
be able to pass text to the API and get in return its sentiment  
pass text into an API in other languages that could be understood or translated  
automatically extract and classify text data, such as tweets, emails  

**News feed Ingester**  
As a user, I want to  
search based on keywords  
discover content from the WEB through url  

## backend  
Using Flask as backend  
Database chosing sqlite  
Using session to secure  

**In homework2**     
Already finished basic function like upload PDF files, return sentiment and keyword frequency search, download news when determining number and keyword    
but frontend uses html   
You can see them under `/backend/hw2modules`. There are hree modules File_uploader, NLP, News_Ingester have tested working with html templates using `return render *.html`    

### Updated from project2 
The latest flask python file is `/backend/app/app.py` and `/backend/app/nlp_app.py`  
`/backend/app/app.py` has not implemented nlp part and the sentiment return is always "" for the convenience of testing  
`/backend/app/nlp_app.py` is the final version  

Finished:   
(1) Use Session to secure the backend     
(2) Use `request.get_json()`, `request.files()` and `return json files` to be consistent with REACT frontend         
(3) Added functions: `get_curent_user()`, `getrecords()`, `file_show()` and so on to rich the functionality      
It can be helpful for REACT frontend to get user_id, file_id, text, sentiment result from backend     
(4) For `upload_file()` and `multiupload_file()` files to be uploaded of all type like jpg will be saved into files and besides that, the content of `pdf`, `txt` and `docx`(import docx) files will be insert to database       
(5) `multiupload_file()` upload files allow uploading several files at one time using `request.files.getlist()`       
already tested successfully in REACT frontend     
(6) wrote `rename_files()` api so that the files can be renamed in database and renamed in stored folder    
(7) separate ingest news to get news information `news_ingest` and choose the news to save to database `save_news()`     
(8) `news_ingest` and `news_show()` return url so that user can click on the url link to see the original news    
(9) Implemented nlp part in `/backend/app/nlp_app.py`: sentiment result is saved in database when uploading or ingesting, then we can read it using `news_show()`  

Partially done:  
Clean db functions to db.py (already create db.py but functions in app.py have not been clean up totally)      

To be done:  
Continue to be consistent with REACT, especially nlp part(upload sentiment, search show sentiment)  
nlp function: translate and so on    
doc type allowed to upload  
Delete files

### Tested using postman   
**Login and signup**   
<div align=center><img src="https://github.com/wq-yang/news-analyzer-app/blob/main/backend/figures/postman_signup.PNG"/></div> 
<div align=center><img src="https://github.com/wq-yang/news-analyzer-app/blob/main/backend/figures/postman_login.PNG"/></div> 

**News Ingest**    
As you can see below, after logging in, api ingest news with url and sentiment, then it can shownews and savenews     
<div align=center><img src="https://github.com/wq-yang/news-analyzer-app/blob/main/backend/figures/postman_ingest.PNG"/></div> 
choose one title  
<div align=center><img src="https://github.com/wq-yang/news-analyzer-app/blob/main/backend/figures/postman_savenews.PNG"/></div> 
<div align=center><img src="https://github.com/wq-yang/news-analyzer-app/blob/main/backend/figures/postman_getrecords.PNG"/></div> 
<div align=center><img src="https://github.com/wq-yang/news-analyzer-app/blob/main/backend/figures/postman_shownews.PNG"/></div> 

**Frontend result**  
<div align=center><img src="https://github.com/wq-yang/news-analyzer-app/blob/main/backend/figures/fileshow.PNG"/></div> 
<div align=center><img src="https://github.com/wq-yang/news-analyzer-app/blob/main/backend/figures/ingest.PNG"/></div> 
<div align=center><img src="https://github.com/wq-yang/news-analyzer-app/blob/main/backend/figures/newsshow.PNG"/></div> 

## frontend  
Using React(with ant design)+Redux
- Login/register module
- Redux to manage login status
- Render different view with different login status
- File Uploader that support uploading multiple files
- List Uploaded Files
- File Content+Sentiment Viewer
- News Search Modal
- List Saved News Articles
- News Search Result+Sentiment Viewer

## APIs
1. Login: POST /api/login 
    - POST body: { username:foo, password:password }
    - response: 
        - if success: { 'status': 'success', 'user': user.to_json() }
        - if not success: { 'status': 'error', 'message': form.errors } 403
2. Register: POST /api/register
    - POST body: { username:foo, password:password }
    - response:
        - if success: { 'status': 'success' }
        - if not success: { 'status': 'error', 'message': form.errors } 403
3. Logout: GET /api/getout
    - response: redirect to home
4. Upload: POST /api/upload (with cookies)
    - POST body: {}
    - response:
        - if success: { 'status': 'success' }
        - if not success: { 'status': 'error', 'message': form.errors } 403
5. List uploaded files for user: GET /api/files/USERNAME OR GET /api/files/?username=foo
    response: { 'files': [ 'path_to_file_1', 'path_to_file_2', ... ] }

