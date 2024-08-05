# USAGE : python3 web_render.py

import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
# use the QtWebEngineWidgets
from PyQt5.QtWebEngineWidgets import *
# start my_app
my_app = QApplication(sys.argv)
# open webpage
my_web = QWebEngineView()
my_web.load(QUrl("http://192.168.2.80/v.html"))
my_web.show()


widget = QLabel("Hello")
widget.show()
# sys exit function
sys.exit(my_app.exec_())
