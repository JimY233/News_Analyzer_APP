##File Uploader API
`app.py` is the api runned locally in my own computer and `ec2_fileuploader.py` is used on EC2  
html files are saved in templates folder  
Use PyPDF2 to convert pdf to text and save the text part in sqlite3 database "mydatabase.db"     
It also has nlp analysis function and use nltk and google cloud language api to implement nlp analysis and the functions are saved in `/file_uploader/nlp` folder 

On EC2 Run `sudo python3 ec2_fileuploader.py`  
<div align=center><img src="https://github.com/BUEC500C1/news-analyzer-JimY233/blob/main/Figures/ec2_file_run.PNG"/></div>

Then we go to EC2 link: ec2-52-15-71-138.us-east-2.compute.amazonaws.com:443   

PDF files and database location:  
<div align=center><img src="https://github.com/BUEC500C1/news-analyzer-JimY233/blob/main/Figures/file_location.PNG"/></div>

**Log in**
and meet the login website (html file is `login.html` in templates folder)  
<div align=center><img src="https://github.com/BUEC500C1/news-analyzer-JimY233/blob/main/Figures/ec2_file_login.PNG"/></div>

**Register**
We can register one account (`register.html`)  
<div align=center><img src="https://github.com/BUEC500C1/news-analyzer-JimY233/blob/main/Figures/ec2_file_register.PNG"/></div>

**Upload**
After logging in, we can see the upload system (`upload.html`)  
Username is shown in "Hello username" and all files under this user_id will also be shown  
As we can see, we can check whether the files with the same name is already in the database and decide to update it  
If the file is the first time uploaded, "save" will show.  
<div align=center><img src="https://github.com/BUEC500C1/news-analyzer-JimY233/blob/main/Figures/ec2_file_upload.PNG"/></div>
<div align=center><img src="https://github.com/BUEC500C1/news-analyzer-JimY233/blob/main/Figures/ec2_file_update.PNG"/></div>
<div align=center><img src="https://github.com/BUEC500C1/news-analyzer-JimY233/blob/main/Figures/ec2_file_save.PNG"/></div>

**Select**
Then we can click "Analyze" to nlp analyze the articles, we can select the article to analyze  
Username is shown in "Hello username" and all files under this user_id will also be shown  
<div align=center><img src="https://github.com/BUEC500C1/news-analyzer-JimY233/blob/main/Figures/ec2_file_select.PNG"/></div>

**NLP analysis**
After selected the files to analyze, we can do nlp analysis  
Username is shown in "Hello username" and all files under this user_id will also be shown  
<div align=center><img src="https://github.com/BUEC500C1/news-analyzer-JimY233/blob/main/Figures/ec2_file_analysis1.PNG"/></div>
<div align=center><img src="https://github.com/BUEC500C1/news-analyzer-JimY233/blob/main/Figures/ec2_file_keyword.PNG"/></div>
<div align=center><img src="https://github.com/BUEC500C1/news-analyzer-JimY233/blob/main/Figures/ec2_file_sentiment.PNG"/></div>
keyword frequency and sentiment analysis is shown  
