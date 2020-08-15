import sys
import requests
import xml.etree.ElementTree as ET
from PyQt5.QtWidgets import (QWidget, QLabel, QApplication, QComboBox, QPushButton)
from PyQt5.QtGui import QPixmap, QFont
 
class CBR_API(QWidget):
    
    def days(self):

        self.days_combo = QComboBox(self)
        day_label = QLabel("Day", self)
        day_label.move(20, 170)
        for day in range(1, 31):
            self.days_combo.addItem('%d' % day)
        self.days_combo.move(20, 200)
    
    def month(self):

        self.month_combo = QComboBox(self)

        month_label = QLabel("Month", self)
        month_label.move(80, 170)
 
        for month_num in range(1, 13):
            self.month_combo.addItem('%d' % month_num)
 
        self.month_combo.move(80, 200)
        
    def year(self):

        self.year_combo = QComboBox(self)

        month_label = QLabel("Year", self)
        month_label.move(140, 170)
 
        for year_num in range(1998, 2020):

            self.year_combo.addItem('%d' % year_num)
 
        self.year_combo.move(140, 200)
        
    def load_result_image(self):

        font = QFont()
        font.setFamily("Arial")
        font.setPointSize(18)
     
        dollar_label = QLabel(self)
        dollar_label.setPixmap(QPixmap("dollar.png"))
        dollar_label.move(60, 260)
     
        self.dollar_value = QLabel("0 rub", self)
        self.dollar_value.setFont(font)
        self.dollar_value.move(130, 263)
     
        euro_label = QLabel(self)
        euro_label.setPixmap(QPixmap("euro.png"))
        euro_label.move(50, 320)
     
        self.euro_value = QLabel("0 rub", self)
        self.euro_value.setFont(font)
        self.euro_value.move(130, 320)
 
    def __init__(self):
        super().__init__()
        self.initUI()
 
    def initUI(self):
        
        logo_label = QLabel(self)
        logo_label.setPixmap(QPixmap("logo.png"))
        logo_label.move(0, 0)
        
        self.days()
        self.month()
        self.year()
        
        ok_button = QPushButton('OK', self)
        ok_button.resize(50, 25)
        ok_button.move(220, 200)
        
        ok_button.clicked.connect(self.makeRequest)
        
        self.load_result_image()
        
        self.setFixedSize(300, 400)
        self.setWindowTitle('valute rate')
        self.show()
        
    def getResult(self, day, month, year):

        result = {
            'usd': 0,
            'eur': 0,
        }
     
        if int(day) < 10:
            day = '0%s' % day
     
        if int(month) < 10:
            month = '0%s' % month
     
        try:

            get_xml = requests.get(
                'http://www.cbr.ru/scripts/XML_daily.asp?date_req=%s/%s/%s' % (day, month, year)
            )
     
            structure = ET.fromstring(get_xml.content)
        except:
            return result
     
        try:
            dollar = structure.find("./*[@ID='R01235']/Value")
            result['dollar'] = dollar.text.replace(',', '.')
        except:
            result['dollar'] = 'x'
     
        try:
            euro = structure.find("./*[@ID='R01239']/Value")
            result['euro'] = euro.text.replace(',', '.')
        except:
            result['euro'] = 'x'
     
        return result
    
    def makeRequest(self):

        day_value = self.days_combo.currentText()
        month_value = self.month_combo.currentText()
        year_value = self.year_combo.currentText()
     

        result = self.getResult(day_value, month_value, year_value)
     

        self.dollar_value.setText('%s rub' % result['dollar'])
        self.dollar_value.adjustSize()
     

        self.euro_value.setText('%s rub' % result['euro'])
        self.euro_value.adjustSize()
 
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    money = CBR_API()
    sys.exit(app.exec_())
