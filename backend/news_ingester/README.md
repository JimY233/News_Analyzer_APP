## News Ingester 
 
`app.py` is the api runned locally in my own computer and `ec2_news.py` is used on EC2   
html files are saved in templates folder  
Use News Api to download news according to keyword. Functions are in `/news_ingester/news`  
Saved in sqlite3 database "mydatabase.db", all three apis shares the same database   
It also has nlp analysis function and use nltk and google cloud language api to implement nlp analysis and the functions are saved in `/news_ingester/nlp` folder  
On EC2 Run `sudo python3 ec2_fileuploader.py`  
<div align=center><img src="https://github.com/BUEC500C1/news-analyzer-JimY233/blob/main/Figures/ec2_news_run.PNG"/></div>

**Log in**
Then we go to EC2 link:  ec2-52-15-71-138.us-east-2.compute.amazonaws.com:443
and meet the login website (html file is `login.html` in templates folder)  
<div align=center><img src="https://github.com/BUEC500C1/news-analyzer-JimY233/blob/main/Figures/ec2_news_login.PNG"/></div>

**Register**
We can register one account (`register.html`)  
<div align=center><img src="https://github.com/BUEC500C1/news-analyzer-JimY233/blob/main/Figures/ec2_file_register.PNG"/></div>

**Ingest**
After logging in, we can see the news ingester system (`ingest.html`)  
Username is shown in "Hello username" and all files under this user_id will also be shown  
You can decide the keyword and number of news you want to download and save to the database  
<div align=center><img src="https://github.com/BUEC500C1/news-analyzer-JimY233/blob/main/Figures/ec2_news_ingest.PNG"/></div>

**Select**
Then we can click "Analyze" to nlp analyze the articles, we can select the article to analyze. Here I implement primary key and thus we just need to input 1,2,3 as news_id  
<div align=center><img src="https://github.com/BUEC500C1/news-analyzer-JimY233/blob/main/Figures/ec2_news_select.PNG"/></div>

**NLP Analysis**
After selected the files to analyze, we can do nlp analysis  
<div align=center><img src="https://github.com/BUEC500C1/news-analyzer-JimY233/blob/main/Figures/ec2_news_sentiment.PNG"/></div>

