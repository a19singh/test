#!/usr/bin/env python
# coding: utf-8

# In[3]:


import OCR
import plate_detect
import cv2
from flask import Flask, request, jsonify
import json
import mysql.connector
import base64
from datetime import datetime, timedelta

# In[4]:

def convert_and_save(b64_string):
    with open("detect.jpg", "wb") as fh:
        fh.write(base64.decodebytes(b64_string.encode()))


app = Flask(__name__)

@app.route('/', methods = ['POST','GET'])
def index():
    try:
#        print(request)
        data = dict(request.form)
        time = data['time']
        img = data['file_data']

        convert_and_save(img)
        print(time)

        img_path=r"./detect.jpg"
        img = cv2.imread(img_path)  #cv2.imread(file)
   
        time = 12

        start_time = datetime.now()
        end_time = start_time+ timedelta(hours= int(time))

        print('time fed')

        x = plate_detect.main(img)
    
        print(x)
        tableCreate()

        dataEntry(x, start_time, end_time)
        fetch = extract(x)


        s = {'Receipt No.' : str(fetch),
             'Reg No.': x,
             'Start Time': start_time.strftime("%Y/%m/%d, %H:%M"),
             'End Time': end_time.strftime("%Y/%m/%d, %H:%M")
            }

        return s

    except Exception as e:
        print('Error: ',e)

def tableCreate():

    mydb = mysql.connector.connect(
            host = "54.211.68.179",
            user = "asstit",
            password = "Redhat@123",
            database = "mydatabase"
            )
    mycursor = mydb.cursor()
    try:
        mycursor.execute("""
        CREATE TABLE number(
        SNO INT PRIMARY KEY AUTO_INCREMENT,
        NUMBER TEXT NOT NULL,
        START DATETIME NOT NULL,
        END DATETIME NOT NULL
        );
        """)

    except mysql.connector.Error as e:
        print(e)
        pass


def dataEntry(a, s, e):

    mydb = mysql.connector.connect(
            host = "127.0.0.1",
            user = "root",
            password = "redhat12",
            database = "mydatabase"
            )

    mycursor = mydb.cursor()

   # data = """
   # INSERT INTO number(NUMBER, START, END)
   # VALUES (\'%s, %s, %s\') """, (%a, %s.strftime("%Y-%m-%d %H:%M:%S"), %e.strftime("%Y-%m-%d %H:%M:%S"))

    mycursor.execute("INSERT INTO number(NUMBER, START, END) VALUES (%s, %s, %s)", (a, s.strftime("%Y-%m-%d %H:%M:%S"), e.strftime("%Y-%m-%d %H:%M:%S")))

    mydb.commit()

def extract(a):

    mydb = mysql.connector.connect(
            host = "127.0.0.1",
            user = "root",
            password = "redhat12",
            database = "mydatabase"
            )

    mycursor = mydb.cursor()

    data = """SELECT SNO FROM number
    WHERE NUMBER like (\'%s\') """ %a

    mycursor.execute(data)
    
    return mycursor.fetchone()[0]

    
    
if __name__ == '__main__':
   app.run(host='0.0.0.0', port=8080) 


# In[ ]:




