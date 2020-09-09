import os, sys
import requests
import re
import youtube_dl

from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from run_trheads import DownloadData

from youtubesearchpython import SearchVideos, SearchPlaylists
import json

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
        self.tab3 = QWidget()
        # self.tabs.setFixedSize(600, 400)

        # Add tabs
        self.tabs.addTab(self.tab1, "Link")
        self.tabs.addTab(self.tab2, "Search")
        self.tabs.addTab(self.tab3, "Info")

        self.tab1UI()
        self.tab2UI()
        self.tab3UI()


    def tab1UI(self):
        # Create first tab
        self.tab1.layout = QVBoxLayout(self)
        self.tab1.setLayout(self.tab1.layout)
        # self.tab1.setStyleSheet("background-image: url(./images/istockphoto-1172479732-170667a.jpg)")

        # Information tab 1
        self.tab1.label = QLabel(self.tab1)
        self.tab1.label.setStyleSheet('color: black')
        self.tab1.label.setFont(QtGui.QFont('Arial', 10))
        self.tab1.label.setText("Insert the downloading video link or playlist")
        self.tab1.label.setGeometry(50, 20, 300, 20)

        # Download link tab 1
        self.tab1.linktextbox = QLineEdit(self.tab1)
        self.tab1.linktextbox.move(50, 40)
        self.tab1.linktextbox.resize(300, 20)
        self.tab1.linktextbox.returnPressed.connect(self.oh_no)


        # check box playlist
        self.tab1.boxpl = QCheckBox("Download related videos", self.tab1)
        # self.box.stateChanged.connect(self.clickBox)
        self.tab1.boxpl.move(200, 70)
        self.tab1.boxpl.resize(320, 40)

        # combo choice
        self.tab1.combo_choice = QComboBox(self.tab1)
        self.tab1.combo_choice.addItem("Video & Music")
        self.tab1.combo_choice.addItem("Only Music")
        self.tab1.combo_choice.addItem("Only Video")
        #self.tab1.combo_choice.setStyleSheet("QComboBox"
        #                                "{"
        #                                "background-color: white;"
        #                                "}")
        self.tab1.combo_choice.move(70, 80)
        self.tab1.combo_choice.resize(100, 20)

        # Create dwl button
        self.tab1.dwl = QPushButton('Download', self.tab1)
        self.tab1.dwl.setToolTip('Click here to download your video')
        self.tab1.dwl.setFont(QtGui.QFont('Arial', 9))
        #self.tab1.dwl.setStyleSheet("QPushButton"
        #                       "{"
        #                       "background-color: #C0C0C0; border-radius: 10px;"
        #                       "}")
        self.tab1.dwl.setGeometry(90, 125, 100, 25)
        # self.dwl.move(90, 125)
        self.tab1.dwl.clicked.connect(self.oh_no)


        # Create close button
        self.tab1.cls = QPushButton('Clear data', self.tab1)
        self.tab1.cls.setToolTip('Click here to claer the data')
        self.tab1.cls.setFont(QtGui.QFont('Arial', 9))
        self.tab1.cls.setGeometry(210, 125, 100, 25)
        #self.tab1.cls.setStyleSheet("QPushButton"
        #                       "{"
        #                       "background-color: #C0C0C0; border-radius: 10px;"
        #                       "}")
        # self.cls.move(210, 125)
        self.tab1.cls.clicked.connect(self.clear_fn)


        # Message text
        self.tab1.textmessage = QLabel(self.tab1)
        self.tab1.textmessage.setStyleSheet('color: black')
        self.tab1.textmessage.setText("Ready to download")
        self.tab1.textmessage.setGeometry(100, 165, 300, 15)

        # Information
        self.tab1.instructions1 = QLabel(self.tab1)
        self.tab1.instructions1.setStyleSheet('color: black')
        self.tab1.instructions1.setText("Check your files in:")
        self.tab1.instructions1.setFont(QtGui.QFont('Arial', 10))
        self.tab1.instructions1.setGeometry(30, 210, 300, 20)

        # Information
        self.tab1.instructions2 = QLabel(self.tab1)
        self.tab1.instructions2.setStyleSheet('color: black')
        self.tab1.instructions2.setFont(QtGui.QFont('Arial', 10))
        self.tab1.instructions2.setText("\Downloads\_video (MP4)")
        self.tab1.instructions2.setGeometry(30, 240, 300, 20)

        # Information
        self.tab1.instructions3 = QLabel(self.tab1)
        self.tab1.instructions3.setStyleSheet('color: black')
        self.tab1.instructions3.setFont(QtGui.QFont('Arial', 10))
        self.tab1.instructions3.setText("\Downloads\_audio (MP3)")
        self.tab1.instructions3.setGeometry(30, 270, 300, 20)

        # Information
        self.tab1.instructions4 = QLabel(self.tab1)
        self.tab1.instructions4.setStyleSheet('color: black')
        self.tab1.instructions4.setFont(QtGui.QFont('Arial', 7))
        self.tab1.instructions4.setText("Enjoy, by Mons 2020")
        self.tab1.instructions4.setGeometry(385, 380, 300, 20)

        # Information Search tab 2
        self.tab2.label = QLabel(self.tab2)
        self.tab2.label.setStyleSheet('color: black')
        self.tab2.label.setFont(QtGui.QFont('Arial', 10))
        self.tab2.label.setText("Search your music to download")
        self.tab2.label.setGeometry(50, 20, 300, 20)

    def tab2UI(self):
        # Search tab 2
        self.tab2.searchtextbox = QLineEdit(self.tab2)
        self.tab2.searchtextbox.move(50, 40)
        self.tab2.searchtextbox.resize(300, 20)
        self.tab2.searchtextbox.returnPressed.connect(self.oh_no_search)

        # Play list or single videos
        self.tab2.dwnl_choice = QComboBox(self.tab2)
        self.tab2.dwnl_choice.addItem("Single Videos")
        self.tab2.dwnl_choice.addItem("Playlist")
        # self.tab1.combo_choice.setStyleSheet("QComboBox"
        #                                "{"
        #                                "background-color: white;"
        #                                "}")
        self.tab2.dwnl_choice.move(390, 40)
        self.tab2.dwnl_choice.resize(100, 20)

        # Search result
        self.tab2.title = QPlainTextEdit(self.tab2)
        self.tab2.title.setGeometry(50, 70, 300, 350)

    def tab3UI(self):
        # Information
        self.tab3.info = QPlainTextEdit(self.tab3)
        self.tab3.info.setGeometry(50, 70, 470, 350)
        self.tab3.info.insertPlainText('With this program you can download videos and music from Youtube' + "\n" + "\n")
        self.tab3.info.insertPlainText(
            'Simple link example:' + "\n" + "\n")
        self.tab3.info.insertPlainText(
            'https://www.youtube.com/watch?v=UojBaKX5Vz4' + "\n" + "\n" + "\n")
        self.tab3.info.insertPlainText(
            'Playlist link example:' + "\n" + "\n")
        self.tab3.info.insertPlainText(
            'https://www.youtube.com/playlist?list=RDEMDHx1mzcs_wPqWOntgHDScQ' + "\n" + "\n" + "\n")
        self.tab3.info.insertPlainText(
            'List of video link example:' + "\n" + "\n")
        self.tab3.info.insertPlainText(
            'https://www.youtube.com/watch?v=0_U4D3Wy-7k&list=RDEMDHx1mzcs_wPqWOntgHDScQ&index=5' + "\n" + "\n" )
        self.tab3.info.insertPlainText(
            "In this case, if you want to download all of them, mark the check box: 'Download all related videos'" + "\n" + "\n")

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def finished(self):
        self.tab1.textmessage.setText('Data download completed')
        print('Finito')

    def clear_fn(self):
        self.tab1.linktextbox.setText('')
        self.tab1.boxpl.setChecked(False)

    def oh_no(self):
        # Link to download
        dwl_ini_link = self.tab1.linktextbox.text()

        # Download options: Only Video, Only Music, Video & Music
        dwl_choice = str(self.tab1.combo_choice.currentText())

        # Related files of a list
        dwl_related = self.tab1.boxpl.checkState()

        print(dwl_ini_link, '\n', dwl_related, '\n', dwl_choice)

        # Validate the link
        try:
            request = requests.get(dwl_ini_link)
            print('Web site exists')
        except:
            print('Web site does not exist')

        # id of videos to download
        video_id_list = []

        if 'playlist' in dwl_ini_link:
            video_id_list.append(dwl_ini_link)
            print('It is a playlist')

        # validate if the link is a list of videos
        elif 'watch?v=' and '&list' in dwl_ini_link:
            if dwl_related == 2:
                # Related videos to download
                r = requests.get(dwl_ini_link)
                page_source = r.text
                for m in re.finditer('":{"url":"/watch?', page_source):
                    video_id = page_source[m.start() + 19:m.end() + 90]
                    print('videossssss', video_id)
                    if 'index=' in video_id:
                        video_id = video_id.split('\\')[0]
                        if 'https://www.youtube.com/watch?v=' + video_id not in video_id_list:
                            video_id_list.append('https://www.youtube.com/watch?v=' + video_id)
            elif dwl_related == 0:
                # Format link to download
                result = dwl_ini_link.find('list')
                # print('link result', result)
                dwl_end_link = dwl_ini_link[0:result - 1]
                print('linkkk0 ', dwl_end_link)
                video_id_list.append(dwl_end_link)
        else:
            video_id_list.append(dwl_ini_link)

        print(video_id_list)


        # Define the thread
        self.dwnl_thread = DownloadData(video_id_list, dwl_choice)  # Any other args, kwargs are passed to the run function
        self.dwnl_thread.signal.connect(self.finished)


        # Execute the thread
        self.dwnl_thread.start()
        self.tab1.textmessage.setText('Downloading data')


    def oh_no_search(self):
        # Reset data result list
        self.tab2.title.clear()

        # Data to search to download
        search_data = self.tab2.searchtextbox.text()

        download_choice = str(self.tab2.dwnl_choice.currentText())

        if download_choice == 'Single Videos':
            search = SearchVideos(search_data, offset=1, mode="json", max_results=20)
        elif download_choice == 'Playlist':
            search = SearchPlaylists("cold play", offset = 1, mode = "json", max_results = 20)
        else:
            search = SearchVideos(search_data, offset=1, mode="json", max_results=20)

        # print(search.result())

        aaa = json.loads(search.result())

        bbb = aaa['search_result']

        for d in bbb:
            print(d['id'])
            self.tab2.title.insertPlainText(d['title'] + "\n" + "\n")

        print(bbb)











