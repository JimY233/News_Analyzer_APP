import mysql.connector
#import MySQLdb
#import pymysql

# class db:
    
#     def dbcreate():

if __name__ == '__main__':
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="123456"
    )
        
    mycursor = mydb.cursor()
    
    mycursor.execute("CREATE DATABASE test_db")

    mycursor.execute("SHOW DATABASES")
 
    for x in mycursor:
        print(x)