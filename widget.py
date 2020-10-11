import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow,QDesktopWidget,QWidget,QVBoxLayout
from PyQt5.QtCore import Qt,QTimer,QDateTime,QTime,QDate
from PyQt5 import QtGui
import datetime
import json
now = datetime.datetime.now()
print(now)
class MainWindow(QWidget):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("funkyD Widget")

        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background:transparent")
        if(sys.platform=='win32'):
            flags = Qt.WindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnBottomHint|Qt.Tool|Qt.X11BypassWindowManagerHint)
        else:
            flags = Qt.WindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnBottomHint)
        self.setWindowFlags(flags)

        #Load Configuration json file
        self.loadConf()

        self.day()
        self.time()
        
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.label)
        self.layout().addWidget(self.label1)
        # self.center()
        self.customPostition()
        
        #Works with X11 enable system like linux and macOS
        self.setAttribute(Qt.WA_X11NetWmWindowTypeDesktop)
        self.setAttribute(Qt.WA_ShowWithoutActivating)

    def loadConf(self):
        file=open("package.json")
        conf=json.load(file)
        print(conf)
        print(sys.argv)
    def center(self):
        ag = QDesktopWidget().availableGeometry()
        sg = QDesktopWidget().screenGeometry()

        widget = self.geometry()
        print(widget.width()/2)
        x = ag.width()//2 -(widget.width()/4)
        y = ag.height()//2 -(widget.height()/4)
        self.move(x, y)
    def customPostition(self):
        ag = QDesktopWidget().availableGeometry()
        sg = QDesktopWidget().screenGeometry()

        widget = self.geometry()
        print(widget.width()/2)
        x = ag.width()//2 -(widget.width()/4)
        y = ag.height()//2 -(widget.height()/4)
        self.move(x,y-200)
    def day(self):
        self.label = QLabel(now.strftime("%A"))
        self.label.setObjectName("date")
        self.label.setStyleSheet("""
        QLabel#date {
            background-color: transparent;
            color:white;
            }
        """)
        font_db=QtGui.QFontDatabase()
        font_id=font_db.addApplicationFont("./assets/fonts/Aquatico.otf")
        your_ttf_font = QtGui.QFont("Aquatico",50)
        self.label.setFont(your_ttf_font)
    def time(self):
        self.label1=QLabel(now.strftime("%H:%M:%S"))
        self.label1.setObjectName("day")
        self.label1.setStyleSheet("""
        QLabel#day{
            background-color: transparent;
            color:white;
            font-size:50px
        }""")
        self.label1.setAlignment(Qt.AlignCenter)

        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.setTime)
        self.timer.start()
    def setTime(self):
        self.label1.setText(QTime.currentTime().toString())
        # self.label1.setText(sys.argv)
app = QApplication(sys.argv)

window = MainWindow()
window.show()
sys.exit(app.exec_())