from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebKitWidgets import *
from PyQt5.QtGui import *
import sip
import sys
import os
app = QApplication([])
 
# And a window
win = QWidget()
win.setWindowTitle('QWebView Interactive Demo')
 
# And give it a layout
layout = QVBoxLayout()
win.setLayout(layout)
 
# Create and fill a QWebView
view = QWebView()
file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "index.html"))
local_url = QUrl.fromLocalFile(file_path)
view.load(local_url)
 
# A button to call our JavaScript
button = QPushButton('Set Full Name')
 
# Interact with the HTML page by calling the completeAndReturnName
# function; print its return value to the console
def complete_name():
    frame = view.page().mainFrame()
    print(frame.evaluateJavaScript('completeAndReturnName();'))
 
# Connect 'complete_name' to the button's 'clicked' signal
button.clicked.connect(complete_name)
 
# Add the QWebView and button to the layout
layout.addWidget(view)
layout.addWidget(button)
 
# Show the window and run the app
win.show()
app.exec_()