import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow,QDesktopWidget,QWidget,QVBoxLayout
from PyQt5.QtCore import Qt,QTimer,QDateTime,QTime,QDate
from PyQt5 import QtGui
import datetime
now = datetime.datetime.now()
print(now)
class MainWindow(QWidget):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("My Awesome App")
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background:transparent")
        flags = Qt.WindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setWindowFlags(flags)
        
        self.day()
        self.time()
        # The `Qt` namespace has a lot of attributes to customise
        # widgets. See: http://doc.qt.io/qt-5/qt.html
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.label)
        self.layout().addWidget(self.label1)
        self.center()
        # Set the central widget of the Window. Widget will expand
        # to take up all the space in the window by default.
        # self.setCentralWidget(label)
        # self.setAttribute(Qt.WA_X11NetWmWindowTypeDesktop)
    def center(self):
        qr=self.frameGeometry()
        cp=QDesktopWidget().availableGeometry().center()
        print(cp)
        qr.moveCenter(cp)
        print(QDesktopWidget().availableGeometry().center())
        self.move(QDesktopWidget().availableGeometry().center())
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
app = QApplication(sys.argv)

window = MainWindow()
window.show()
sys.exit(app.exec_())