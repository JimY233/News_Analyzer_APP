##NLP Analysis

`app.py` is the api runned locally in my own computer and `ec2_nlp.py` is used on EC2    
html files are saved in templates folder  
alayze the files saved in sqlite3 database "mydatabase.db" (share the database with other two api)  
It also has nlp analysis function and use nltk and google cloud language api to implement nlp analysis and the functions are saved in `/NLP/nlp` folder  
On EC2 Run `sudo python3 ec2_nlp.py`  
<div align=center><img src="https://github.com/BUEC500C1/news-analyzer-JimY233/blob/main/Figures/ec2_nlp.PNG"/></div>

All is the same in the file uploader api but when you log in, you skip the upload and directly go to nlp analysis  

**Select**
After logging in, we can select the article to analyze  
Username is shown in "Hello username" and all files under this user_id will also be shown  
<div align=center><img src="https://github.com/BUEC500C1/news-analyzer-JimY233/blob/main/Figures/ec2_file_select.PNG"/></div>

**NLP analysis**
After selected the files to analyze, we can do nlp analysis  
Username is shown in "Hello username" and all files under this user_id will also be shown  
<div align=center><img src="https://github.com/BUEC500C1/news-analyzer-JimY233/blob/main/Figures/ec2_file_analysis1.PNG"/></div>
<div align=center><img src="https://github.com/BUEC500C1/news-analyzer-JimY233/blob/main/Figures/ec2_file_keyword.PNG"/></div>
<div align=center><img src="https://github.com/BUEC500C1/news-analyzer-JimY233/blob/main/Figures/ec2_file_sentiment.PNG"/></div>
keyword frequency and sentiment analysis is shown  
