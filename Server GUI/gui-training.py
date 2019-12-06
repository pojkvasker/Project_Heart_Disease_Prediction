import sys
import os
import numpy as np
import pandas as pd
from PyQt5.QtWidgets import *

class App(QWidget):

    fileName = ""

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
            if fileExtension == ".csv":
                print("CSV")
                self.fileName = fileName_tmp
                self.parseCSV_()
            else:
                print("Not CSV!")

    def parseCSV_(self):
        print(self.fileName)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())