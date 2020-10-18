import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow,QDesktopWidget,QWidget,QVBoxLayout
from PyQt5.QtCore import Qt,QTimer,QDateTime,QTime,QDate,QRectF
from PyQt5 import QtGui
import datetime
import json
import os
import psutil
now = datetime.datetime.now()
class MainWindow(QWidget):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("funkyD Widget")
        # self.width=QDesktopWidget().availableGeometry().width()
        # self.height=QDesktopWidget().screenGeometry().height()
        # self.setFixedWidth(self.width)
        # self.setFixedHeight(self.height)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background:transparent")
        if(sys.platform=='win32'):
            flags = Qt.WindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnBottomHint|Qt.Tool|Qt.X11BypassWindowManagerHint)
        else:
            flags = Qt.WindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnBottomHint|Qt.WindowTransparentForInput)
        self.setWindowFlags(flags)

        #Load Configuration json file
        self.loadConf()

        self.day()
        self.time()
        self.cpu_usage()

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.dayLabel)
        self.layout().addWidget(self.timeLabel)
        self.layout().addWidget(self.cpuLabel)
        self.center()
        # self.customPostition()
        
        #Works with X11 enable system like linux and macOS
        # self.setAttribute(Qt.WindowTransparentForInput)
        self.setAttribute(Qt.WA_X11NetWmWindowTypeDesktop)
        
        # self.setAttribute(Qt.WA_ShowWithoutActivating)

    def loadConf(self):
        with open(os.path.join(sys.argv[1],"config.json")) as f:
            self.confData=json.load(f)
    def center(self):
        ag = QDesktopWidget().availableGeometry()
        sg = QDesktopWidget().screenGeometry()

        widget = self.geometry()
        print(widget.width()/2)
        x = ag.width()//2 -(widget.width()//2)
        y = ag.height()//2 -(widget.height()//2)
        self.move(x, y)
    def customPostition(self,label,beta=0):
        ag = QDesktopWidget().availableGeometry()
        sg = QDesktopWidget().screenGeometry()
        widgetWidth=label.fontMetrics().boundingRect(label.text()).width()
        widgetHeight=label.fontMetrics().boundingRect(label.text()).height()
        print(widgetWidth)
        x = ag.width()//2-widgetWidth//2
        y = (sg.height()-widgetHeight)//2-beta
        label.move(x,y)
    def day(self):
        self.dayLabel = QLabel(now.strftime("%A"),self)
        self.dayLabel.setObjectName("day")
        color=self.confData["day"]["color"]
        fontSize=self.confData["day"]["fontSize"]
        fontSize=int(fontSize)
        self.dayLabel.setStyleSheet("""
        QLabel#day{
            background-color: transparent;
            color:%s;
            font-size:%dpx;
            alignment:center;
            }
        """%(color,fontSize))
        font_db=QtGui.QFontDatabase()
        if self.confData["day"]["customFont"]==True:
            font_id=font_db.addApplicationFont(self.confData["day"]["fontPath"])
        your_ttf_font = QtGui.QFont(self.confData["day"]["fontName"],fontSize)
        self.dayLabel.setFont(your_ttf_font)
        # self.dayLabel.setGeometry(1000,1000,30,80)
        self.dayLabel.setAlignment(Qt.AlignCenter)
        print(self.dayLabel.fontMetrics().boundingRect(self.dayLabel.text()).width())
        # self.customPostition(self.dayLabel)
        # self.dayLabel.move((self.width//2)-200,self.height//2)
    def time(self):
        self.timeLabel=QLabel(now.strftime("%H:%M:%S"),self)
        self.timeLabel.setObjectName("time")
        color=self.confData["time"]["color"]
        fontSize=self.confData["time"]["fontSize"]
        fontSize=int(fontSize)
        self.timeLabel.setStyleSheet("""
        QLabel#time{
            background-color: transparent;
            color:%s;
            font-size:%dpx;
        }"""%(color,fontSize))
        self.timeLabel.setAlignment(Qt.AlignCenter)
        font_db=QtGui.QFontDatabase()
        if self.confData["time"]["customFont"]==True:
            font_id=font_db.addApplicationFont(self.confData["time"]["fontPath"])
        your_ttf_font = QtGui.QFont(self.confData["time"]["fontName"],fontSize)
        self.timeLabel.setFont(your_ttf_font)
        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.setTime)
        self.timer.start()
        # self.customPostition(self.timeLabel,-100)
    def cpu_usage(self):
        self.cpuLabel=QLabel(str(psutil.cpu_percent())+"%",self)
        self.cpuLabel.setObjectName("cpu")
        color=self.confData["cpu"]["color"]
        fontSize=self.confData["cpu"]["fontSize"]
        fontSize=int(fontSize)
        print(fontSize)
        self.cpuLabel.setStyleSheet("""
        QLabel#cpu{
            background-color: transparent;
            color:%s;
            font-size:%dpx;
        }"""%(color,fontSize))
        self.cpuLabel.setAlignment(Qt.AlignCenter)
        font_db=QtGui.QFontDatabase()
        if self.confData["cpu"]["customFont"]==True:
            font_id=font_db.addApplicationFont(self.confData["cpu"]["fontPath"])
        your_ttf_font = QtGui.QFont(self.confData["cpu"]["fontName"],fontSize)
        self.cpuLabel.setFont(your_ttf_font)
        # self.customPostition(self.cpuLabel,-200)
        
    def setTime(self):
        self.timeLabel.setText(QTime.currentTime().toString())
        self.cpuLabel.setText(str(psutil.cpu_percent())+"%")
        # self.timeLabel.setText(sys.argv[1])

app = QApplication(sys.argv)

window = MainWindow()
window.show()
sys.exit(app.exec_())