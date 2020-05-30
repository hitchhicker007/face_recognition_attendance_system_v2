# import os,cv2,csv,time
# single = []
# tt = []
# with open('test.csv','r') as file:
#     reader = csv.reader(file)
#     for row in reader:
#         tt.append(row)
#
# i = 0
# while i<len(tt):
#     print("sub"+tt[i][0])
#     print("st"+tt[i][1])
#     print("et"+tt[i][2])
#     i+=1
#
# import random
# import string
#
# def randomString(stringLength=10):
#     """Generate a random string of fixed length """
#     letters = string.ascii_lowercase
#     return ''.join(random.choice(letters) for i in range(stringLength))
#
# print ("Random String is ", ''.join(random.choice(string.ascii_lowercase) for i in range(10)) )
# print ("Random String is ", randomString(10) )
# print ("Random String is ", randomString(10) )

from requests import Ui_MainWindow
from PyQt5 import QtWidgets,QtGui

class main_win(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self, parent=None):
        super(, self).__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('icon48.png'))
        self.listWidget.item(0).s
