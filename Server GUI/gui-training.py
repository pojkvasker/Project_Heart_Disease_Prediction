import sys
import os
import numpy as np
import pandas as pd
#import pymysql
from PyQt5.QtWidgets import *

class App(QWidget):

    fileName = ""

    #connection = pymysql.connect(
    #    host = "localhost",
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

        self.show()

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName_tmp, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        
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

            tuple_ = [tuple(x) for x in data_tmp.values]        
            print(tuple_)

            #try:
            #    with self.connection.cursor() as cursor:
            #        sql = "INSERT INTO profiles (`age`, `sex`, `cp`, `trestbps`, `chol`, `fbs`, `restecg`, `thalach`, `exang`, `oldpeak`, `slope`, `ca`, `thal`, `num`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            #    try:
            #        cursor.executemany(sql,(age,sex,bp,chol,ecg,exang,id,pred,prob,timestamp))
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