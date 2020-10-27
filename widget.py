import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow,QDesktopWidget,QWidget,QVBoxLayout,QGridLayout,QLayout
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
        self.width=QDesktopWidget().availableGeometry().width()
        self.height=QDesktopWidget().screenGeometry().height()
        self.setFixedWidth(self.width)
        self.setFixedHeight(self.height)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background:transparent;")
        if(sys.platform=='win32'):
            flags = Qt.WindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnBottomHint|Qt.Tool|Qt.X11BypassWindowManagerHint)
        else:
            flags = Qt.WindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnBottomHint|Qt.WindowTransparentForInput)
        self.setWindowFlags(flags)

        #Load Configuration json file
        self.loadConf()
        self.betas=[]
        self.day()
        self.greeting()
        self.time()
        print(self.betas)
        # self.cpu_usage()

        # self.setLayout(QGridLayout())
        # self.layout().addWidget(self.dayLabel,0,0)
        # self.layout().addWidget(self.timeLabel,1,0)
        # self.layout().addWidget(self.cpuLabel)
        # self.center()
        # self.layout().setSizeConstraint(QLayout.SetMinimumSize)
        # self.customPostition()
        
        #Works with X11 enable system like linux and macOS
        # self.setAttribute(Qt.WindowTransparentForInput)
        self.setAttribute(Qt.WA_X11NetWmWindowTypeDesktop)
        #Qt.WA_NoSystemBackground|Qt.AA_EnableHighDpiScaling
        
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

    # Find QLabel dimensions    
    def labelWidth(self,label):
        return label.fontMetrics().boundingRect(label.text()).width()
    def labelHeight(self,label):
        return label.fontMetrics().boundingRect(label.text()).height()

    def customPostition(self,label,beta=0):
        ag = QDesktopWidget().availableGeometry()
        sg = QDesktopWidget().screenGeometry()
        widgetWidth=self.labelWidth(label)
        widgetHeight=self.labelHeight(label)
    
        x = ag.width()//2-(widgetWidth//2)
        y = (sg.height()-widgetHeight)//2-beta
        label.move(x,y)

    # Function for Styling the labels
    def labelStyles(self,label,id):
        color=self.confData[id]["color"]
        fontSize=self.confData[id]["fontSize"]
        fontSize=int(fontSize)
        label.setStyleSheet("""
        QLabel#%s{
            background-color: transparent;
            color:%s;
            font-size:%dpx;
            alignment:center;
            }
        """%(id,color,fontSize))
        font_db=QtGui.QFontDatabase()
        if self.confData[id]["customFont"]==True:
            font_id=font_db.addApplicationFont(self.confData[id]["fontPath"])
        your_ttf_font = QtGui.QFont(self.confData[id]["fontName"],fontSize)
        label.setFont(your_ttf_font)
        label.adjustSize()

    def greeting(self):
        greeting=""
        if now.hour < 12:
            greeting='Good morning.'
        elif 12 <= now.hour < 18:
            greeting='Good afternoon.'
        else:
            greeting='Good evening.'
        self.greetingLabel=QLabel(greeting,self)
        self.greetingLabel.setObjectName("greeting")
        self.labelStyles(self.greetingLabel,"greeting")
        height=self.labelHeight(self.greetingLabel)
        beta=self.betas[-1]+20
        self.customPostition(self.greetingLabel,-beta)
        self.betas.append(height/2+beta)
    
    def day(self):
        self.dayLabel = QLabel(now.strftime("%A"),self)
        self.dayLabel.setObjectName("day")
        self.labelStyles(self.dayLabel,"day")
        
        self.customPostition(self.dayLabel)
        self.betas.append(self.labelHeight(self.dayLabel)/2)
        # self.dayLabel.move((self.width//2)-200,self.height//2)
    def time(self):
        self.timeLabel=QLabel(now.strftime("%I:%M:%S"),self)
        self.timeLabel.setObjectName("time")
        self.labelStyles(self.timeLabel,"time")
        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.setTime)
        self.timer.start()
        height=self.labelHeight(self.timeLabel)
        beta=self.betas[-1]+30
        self.customPostition(self.timeLabel,-beta)
        self.betas.append(height/2+beta)
    def cpu_usage(self):
        self.cpuLabel=QLabel(str(psutil.cpu_percent())+"%",self)
        self.cpuLabel.setObjectName("cpu")
        self.labelStyles(self.cpuLabel,"cpu")
        # self.customPostition(self.cpuLabel,-200)
        
    def setTime(self):
        self.timeLabel.setText(now.strftime("%I:%M %p"))
        self.timeLabel.adjustSize()
        # self.cpuLabel.setText(str(psutil.cpu_percent())+"%")
        # self.timeLabel.setText(sys.argv[1])

app = QApplication(sys.argv)

window = MainWindow()
window.show()
sys.exit(app.exec_())