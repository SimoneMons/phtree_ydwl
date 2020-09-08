import os, sys
import requests
import re
import youtube_dl

from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from run_trheads import DownloadVideo

# Global variables
SAVE_PATH = os.path.expanduser('~/Downloads')

ydl_video = {
    'format': 'best',
    'dumpjson': True,
    'outtmpl': SAVE_PATH + '/_video/%(title)s.%(ext)s',
}

ydl_audio = {
    'format': 'bestaudio/best',
    'outtmpl': SAVE_PATH + '/_audio/%(title)s.%(ext)s',
}


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        print(' ')
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("venv"), relative_path)


class youdwnl_tabs(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        # self.tabs.setFixedSize(600, 400)

        # Add tabs
        self.tabs.addTab(self.tab1, "Tab 1")
        self.tabs.addTab(self.tab2, "Tab 2")

        # Create first tab
        self.tab1.layout = QVBoxLayout(self)
        self.tab1.setLayout(self.tab1.layout)
        # self.tab1.setStyleSheet("background-image: url(./images/istockphoto-1172479732-170667a.jpg)")

        # Information
        self.tab1.label = QLabel(self.tab1)
        self.tab1.label.setStyleSheet('color: black')
        self.tab1.label.setFont(QtGui.QFont('Arial', 10))
        self.tab1.label.setText("Insert the downloading video link or playlist")
        self.tab1.label.setGeometry(50, 20, 300, 20)

        # Download link
        self.tab1.linktextbox = QLineEdit(self.tab1)
        self.tab1.linktextbox.move(50, 40)
        self.tab1.linktextbox.resize(300, 20)
        self.tab1.linktextbox.returnPressed.connect(self.oh_no)

        # Message text
        self.tab1.textmessage = QLabel(self.tab1)
        self.tab1.textmessage.setStyleSheet('color: black')
        self.tab1.textmessage.setText("Ready to download")
        self.tab1.textmessage.setGeometry(100, 165, 300, 15)

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def finished(self):
        self.tab1.textmessage.setText('Video download completed')

    def oh_no(self):
        # link to download
        dwl_link = self.tab1.linktextbox.text()


        # Pass the function to execute
        self.dwnl_thread = DownloadVideo(dwl_link)  # Any other args, kwargs are passed to the run function
        self.dwnl_thread.signal.connect(self.finished)

        # Execute
        self.dwnl_thread.start()

        print(dwl_link)

        self.tab1.textmessage.setText('Downloading video')








