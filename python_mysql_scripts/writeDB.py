#! C:\Users\phil\AppData\Local\Programs\Python\Python38-32\python.exe
import sys
import pymysql
import numpy as np
from datetime import datetime
#from sklearn.gaussian_process import GaussianProcessClassifier
#import this

age = float(sys.argv[1])
sex = float(sys.argv[2])
bp = float(sys.argv[3])
chol = float(sys.argv[4])
ecg = float(sys.argv[5])
exang = float(sys.argv[6])
id = float(sys.argv[7])
pred = float(sys.argv[8])
prob = float(sys.argv[9])
timestamp = str(datetime.now())

print("Content-Type: text/html\n")
print(timestamp)
connection = pymysql.connect(
    host = "localhost",
    user = "root",
    password = "",
    db = "pdp",
)
try:
    with connection.cursor() as cursor:
         sql = "INSERT INTO profiles (`age`, `sex`, `bp`, `chol`, `ecg`, `exang`, `id`, `pred`, `prob`, `timestamp`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
         try:
             cursor.execute(sql,(age,sex,bp,chol,ecg,exang,id,pred,prob,timestamp))
             print("Added values to DB.")
         except:
             print("Did not work!")
    connection.commit()
finally:
    connection.close()