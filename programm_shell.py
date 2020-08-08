import sys
from PyQt5.QtWidgets import QWidget, QLabel, QApplication
import requests
import xml.etree.ElementTree as ET
import datetime

today_date = datetime.datetime.today().strftime("%d/%m/%Y")

url = "http://www.cbr.ru/scripts/XML_daily.asp?date_req="+str(today_date)

def get_response(url):
    response = requests.get(url)
    return response

def check_the_answer(response):
    if response.status_code == 200:
        return response

def get_xml(response):
    tree = ET.fromstring(response.content)
    return tree

def get_date_from_xml(tree):
    return tree.attrib['Date']

def get_attrib_by_xml(tree):
    for value in tree.findall('Valute'):
        charcode = value.find('CharCode').text
        rate = value.find('Value').text
        if charcode == 'USD':
            return rate
        
def print_rate(rate):
    print(rate)


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        lbl1 = QLabel("Dollars's rate: " + str(rate), self)
        lbl1.move(15, 10)

        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Absolute')
        self.show()


if __name__ == '__main__':
    
    
    response = get_response(url)
    response = check_the_answer(response)
    tree = get_xml(response)
    rate = get_attrib_by_xml(tree)

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())