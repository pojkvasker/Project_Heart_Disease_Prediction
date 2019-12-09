import sys
import os
import numpy as np
import pandas as pd
import pymysql
from PyQt5.QtWidgets import *

class App(QWidget):

    fileName = ""

    #connection = pymysql.connect(
    #    host = "https://f9415641.ngrok.io/dashboard/",
    #    user = "root",
    #    password = "",
    #    db = "pdp",
    #)

    def __init__(self):
        super().__init__()
        self.title = 'help me'
        self.top = 700
        self.left = 200
        self.width = 400
        self.height = 400
        self.Log()

    def Log(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.height, self.width)

        btnTrain = QPushButton('Train model', self)
        btnTrain.move(10, 200)

        btnAdd = QPushButton('Add data', self)
        btnAdd.move(110, 200)

        btnRead = QPushButton('Read data', self)
        btnRead.move(210, 200)

        btnAdd.clicked.connect(self.openFileNameDialog)
        btnRead.clicked.connect(self.getID)

        self.show()

    def getID(self):
        id, okPressed = QInputDialog.getInt(self, "Get integer","Percentage:", 0, 0, 1000000, 1)
        if okPressed:
            print(id)
            self.readDataID(id)

    def readDataID(self,id):
        # Read specific profile from db
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT `age`, `sex`, `bp`, `chol`, `ecg`, `exang`, `pred`, `prob`, `timestamp` FROM `profiles` WHERE `id`=%s"
            try:
                cursor.executemany(sql, (str(id),))
                db_data = cursor.fetchone()
                print("Profile read.")
            except:
                print("Did not work!")
            self.connection.commit()
        finally:
            self.connection.close()

        # Import into separate vectors
        age = [i[0] for i in db_data]
        sex = [i[1] for i in db_data]
        bp = [i[2] for i in db_data]
        chol = [i[3] for i in db_data]
        ecg = [i[4] for i in db_data]
        pred = [i[5] for i in db_data]
        prob = [i[6] for i in db_data]
        timestamp = [i[7] for i in db_data]

        print(age)

    def openFileNameDialog(self):
        #options = QFileDialog.Options()
        #options |= QFileDialog.DontUseNativeDialog
        #fileName_tmp, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)

        fileName_tmp = 'C:/Users/David/Desktop/test2.txt'
        
        if fileName_tmp:
            # Find extension of file.
            _, fileExtension = os.path.splitext(fileName_tmp)
            print(fileName_tmp)
            print(fileExtension)
            # Only continue if extension is csv
            if fileExtension == ".txt":
                print("txt")
                # Use that filename
                self.fileName = fileName_tmp
                # Start adding data to training db
                self.addData()
            else:
                print("Not txt!")

    def addData(self):
        # Read from txt file
        data_tmp = pd.read_csv(self.fileName, sep = ",", header=None)
        data_tmp.columns = ['age', 'sex','cp','trestbps','chol','fbs','restecg',\
                'thalach','exang','oldpeak','slope','ca','thal','num']
        print(data_tmp)
        print(data_tmp.shape)

        rows, cols = data_tmp.shape
        
        if cols != 14:
            print("Wrong numbers of columns")
        else:

            data = data_tmp.astype('float64')

            tuple_ = [tuple(x) for x in data.values]        
            print(tuple_)
            print((tuple_[0][0]))
            print(type(tuple_[0][0]))

            #data = np.empty((rows,1))

            #for i in range(cols):
            #    data = (float(tuple_[i][0]), float(tuple_[i][1]), float(tuple_[i][2]), float(tuple_[i][3]), \
            #        float(tuple_[i][4]), float(tuple_[i][5]), float(tuple_[i][6]), float(tuple_[i][7]), \
            #        float(tuple_[i][8]), float(tuple_[i][9]), float(tuple_[i][10]), float(tuple_[i][11]), \
            #        float(tuple_[i][12]), float(tuple_[i][13]))
                
            #print(data)

            # (data_tmp[0]['age'], data_tmp[0]['sex'], data_tmp[0]['cp'], data_tmp[0]['trestbps'], data_tmp[0]['chol'], data_tmp[0]['fbs'], data_tmp[0]['restecg'], data_tmp[0]['thalach'], data_tmp[0]['exang'], data_tmp[0]['oldpeak'], data_tmp[0]['slope'], data_tmp[0]['ca'], data_tmp[0]['thal'], data_tmp[0]['num'])
            # sql = "INSERT INTO profiles (age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal, num) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

            #try:
            #    with self.connection.cursor() as cursor:
            #        sql = "INSERT INTO heart disease detection (age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal, num) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            #    try:
            #        cursor.executemany(sql,tuple_)
            #        print("Added values to DB.")
            #    except:
            #        print("Did not work!")
            #    self.connection.commit()
            #finally:
            #   self.connection.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())