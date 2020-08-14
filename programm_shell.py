import sys
from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit,
    QInputDialog, QApplication, QLabel)
import requests
import xml.etree.ElementTree as ET
import datetime

#today_date = datetime.datetime.today().strftime("%d/%m/%Y")


def get_date_from_xml(tree):
    return tree.attrib['Date']



class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.today_date = datetime.datetime.today().strftime("%d/%m/%Y")
        self.rate = 0
        self.url = "http://www.cbr.ru/scripts/XML_daily.asp?date_req="
        self.initUI()
        
    def showDialog(self, today_date):

        text, ok = QInputDialog.getText(self, 'Input Dialog',
            'Enter your name:')

        if ok:
            print(self.today_date)
            self.today_date = text
            print(text)
            self.request(text)
            
    def request(self, data):
        url = self.url + str(data)
        print(url)
        response = self.get_response(url)
        response = self.check_the_answer(response)
        tree = self.get_xml(response)
        value = self.get_attrib_by_xml(tree)
        print(value)
        self.le.setText(value)
        
    def get_response(self, url):
        response = requests.get(url)
        return response

    def check_the_answer(self, response):
        if response.status_code == 200:
            return response

    def get_xml(self, response):
        tree = ET.fromstring(response.content)
        return tree
    
    def get_attrib_by_xml(self, tree):
        for value in tree.findall('Valute'):
            charcode = value.find('CharCode').text
            rate = value.find('Value').text
            if charcode == 'USD':
                return rate   
            
    def initUI(self):
        
        self.btn = QPushButton('Dialog', self)
        self.btn.move(20, 20)
        self.btn.clicked.connect(self.showDialog)
        
        self.le = QLineEdit(self)
        self.le.move(130, 22)
        
        self.setGeometry(300, 300, 290, 150)
        self.setWindowTitle('Input dialog')
        #self.show()

        lbl1 = QLabel("Dollars's rate: " + str(self.rate), self)
        lbl1.move(15, 10)

        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Absolute')
        self.show()

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Example()
    
    sys.exit(app.exec_())
