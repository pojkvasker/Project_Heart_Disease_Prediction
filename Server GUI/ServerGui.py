import sys
import pymysql.cursors
from PyQt5 import QtCore, QtWidgets, QtGui

class Ui(object):

    def sql_stuff(self):
        connection = pymysql.connect(
            host = "localhost",
            user = "root",
            password = "",
            db = "pdp",)
        cursor = connection.cursor() 

        query1 = ("""SELECT age, sex, bp, chol, ecg, id, pred, prob, timestamp FROM profiles""")
        
        cursor.execute(query1)
        self.result = []
        fetchq = cursor.fetchall()
        print(fetchq)
        self.result.append(fetchq)
        return self.result

        self.listWidget.addItem(self.result)
    
    
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(889, 692)
        Form.setStyleSheet("background-color: rgb(255, 255, 255);")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
