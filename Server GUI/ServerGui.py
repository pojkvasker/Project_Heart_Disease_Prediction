import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Login'
        self.top = 100
        self.left = 100
        self.width = 350
        self.height = 700
        self.Log()

    def Log(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.height, self.width)

        btn = QPushButton('Search profile', self)
        btn.move(100, 100)
        
        self.host = QLineEdit(self)
        self.host.setPlaceholderText('id')
        self.host.move(100, 150)
    
        btn = QPushButton('Add to database', self)
        btn.move(250, 100)
        
        btn = QPushButton('Update prediction', self)
        btn.move(400, 100)
        #btn = clicked.connect(self.getModel)

        labelA = QLabel(self)
        labelA.setText('No model info..')
        labelA.move(400, 150)
        
        self.show()
    #def getModel(self):

   
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
