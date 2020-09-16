import os, sys
import requests
import re
import youtube_dl
import urllib.request

from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap
from run_trheads import DownloadData

from youtubesearchpython import SearchVideos, SearchPlaylists
import json

# Global variables
SAVE_PATH = os.path.expanduser('~/Downloads')

ydl_video = {
    'format': 'best',
    'dumpjson': True,
    'ignore-errors': True,
    'skip-unavailable-fragments': True,
    'continue': True,
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
        #self.tab1.setStyleSheet("background-image: url(./images/captura.png)")

        # Information tab 1
        self.tab1.label = QLabel(self.tab1)
        self.tab1.label.setStyleSheet('color: black')
        self.tab1.label.setFont(QtGui.QFont('Arial', 10))
        self.tab1.label.setText("Insert Video Link or Playlist to download")
        self.tab1.label.setGeometry(50, 20, 300, 20)

        # Download link tab 1
        self.tab1.linktextbox = QLineEdit(self.tab1)
        self.tab1.linktextbox.move(50, 45)
        self.tab1.linktextbox.resize(320, 20)
        self.tab1.linktextbox.returnPressed.connect(self.oh_no)

        # check box playlist
        self.tab1.boxpl = QCheckBox("Download related videos in the list", self.tab1)
        # self.box.stateChanged.connect(self.clickBox)
        self.tab1.boxpl.move(220, 70)
        self.tab1.boxpl.resize(320, 40)

        # Combo choice
        self.tab1.combo_choice = QComboBox(self.tab1)
        self.tab1.combo_choice.addItem("Video & Music")
        self.tab1.combo_choice.addItem("Only Music")
        self.tab1.combo_choice.addItem("Only Video")
        # self.tab1.combo_choice.setStyleSheet("QComboBox"
        #                                "{"
        #                                "background-color: white;"
        #                                "}")
        self.tab1.combo_choice.move(85, 80)
        self.tab1.combo_choice.resize(100, 20)

        # Download button
        self.tab1.dwl = QPushButton('Download', self.tab1)
        self.tab1.dwl.setToolTip('Click here to download your video')
        self.tab1.dwl.setFont(QtGui.QFont('Arial', 9))
        # self.tab1.dwl.setStyleSheet("QPushButton"
        #                       "{"
        #                       "background-color: #C0C0C0; border-radius: 10px;"
        #                       "}")
        self.tab1.dwl.setGeometry(90, 125, 100, 25)
        # self.dwl.move(90, 125)
        self.tab1.dwl.clicked.connect(self.oh_no)

        # Create clear button
        self.tab1.cls = QPushButton('Clear data', self.tab1)
        self.tab1.cls.setToolTip('Click here to claer the data')
        self.tab1.cls.setFont(QtGui.QFont('Arial', 9))
        self.tab1.cls.setGeometry(210, 125, 100, 25)
        # self.tab1.cls.setStyleSheet("QPushButton"
        #                       "{"
        #                       "background-color: #C0C0C0; border-radius: 10px;"
        #                       "}")
        # self.cls.move(210, 125)
        self.tab1.cls.clicked.connect(self.clear_tab1)

        # Message text
        self.tab1.textmessage = QLabel(self.tab1)
        self.tab1.textmessage.setStyleSheet('color: black')
        self.tab1.textmessage.setText("Ready to download")
        self.tab1.textmessage.setGeometry(340, 130, 300, 15)

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
        self.tab1.instructions4.setGeometry(445, 425, 300, 20)

        # photo
        self.tab1.photo_label = QLabel(self.tab1)

        photo_path = './images/Captura.png'

        # Pycharm
        #pixmap = QPixmap(photo_path)

        # Exe
        pixmap = QPixmap(resource_path(photo_path))

        self.tab1.photo_label.setPixmap(pixmap)
        self.tab1.photo_label.setGeometry(330, 350, 111, 89)

        # .exe
        # background_image_path = "./images/istockphoto-1172479732-170667a.jpg"
        # icon_image_path = "./images/totoro.png"

        # pycharm exe
        background_image_path = "C:\Proyectos\phtree\phtree_ydwl\images\\istockphoto-1172479732-170667a.jpg"
        #icon_image_path = "C:\Proyectos\phtree\phtree_ydwl\images\\totoro.png"

        # Icon
        # self.setWindowIcon(QIcon(icon_image_path))
        #self.setWindowIcon(QIcon(resource_path(icon_image_path)))

    def tab2UI(self):
        # Information Search tab 2
        self.tab2.label = QLabel(self.tab2)
        self.tab2.label.setStyleSheet('color: black')
        self.tab2.label.setFont(QtGui.QFont('Arial', 10))
        self.tab2.label.setText("Search your video or music to download")
        self.tab2.label.setGeometry(50, 20, 300, 20)

        # Search tab 2
        self.tab2.searchtextbox = QLineEdit(self.tab2)
        self.tab2.searchtextbox.move(50, 45)
        self.tab2.searchtextbox.resize(320, 20)
        self.tab2.searchtextbox.returnPressed.connect(self.oh_no_search)

        # Combo choice
        self.tab2.combo_choice = QComboBox(self.tab2)
        self.tab2.combo_choice.addItem("Video & Music")
        self.tab2.combo_choice.addItem("Only Music")
        self.tab2.combo_choice.addItem("Only Video")
        # self.tab1.combo_choice.setStyleSheet("QComboBox"
        #                                "{"
        #                                "background-color: white;"
        #                                "}")
        self.tab2.combo_choice.move(85, 80)
        self.tab2.combo_choice.resize(100, 20)

        self._toggle = True

        # check box video
        self.tab2.boxvd = QCheckBox("Search videos", self.tab2)
        # self.tab2.boxvd.setChecked(False)
        # self.tab2.boxvd.stateChanged.connect(self.change_checkbox_video)
        self.tab2.boxvd.setChecked(self._toggle)
        self.tab2.boxvd.clicked.connect(self.toggle)
        self.tab2.boxvd.move(200, 70)
        self.tab2.boxvd.resize(320, 40)

        # check box playlist
        self.tab2.boxpl = QCheckBox("Search playlist", self.tab2)
        # self.tab2.boxpl.setChecked(False)
        # self.tab2.boxpl.stateChanged.connect(self.change_checkbox_pllist)
        self.tab2.boxpl.setChecked(not self._toggle)
        self.tab2.boxpl.clicked.connect(self.toggle)
        self.tab2.boxpl.move(320, 70)
        self.tab2.boxpl.resize(320, 40)

        # Search button
        self.tab2.dwl = QPushButton('Search', self.tab2)
        self.tab2.dwl.setToolTip('Click here to search your videos or playlist')
        self.tab2.dwl.setFont(QtGui.QFont('Arial', 9))
        # self.tab1.dwl.setStyleSheet("QPushButton"
        #                       "{"
        #                       "background-color: #C0C0C0; border-radius: 10px;"
        #                       "}")
        self.tab2.dwl.setGeometry(50, 125, 100, 25)
        # self.dwl.move(90, 125)
        self.tab2.dwl.clicked.connect(self.oh_no_search)

        # Download button
        self.tab2.dwl = QPushButton('Download', self.tab2)
        self.tab2.dwl.setToolTip('Click here to download your video')
        self.tab2.dwl.setFont(QtGui.QFont('Arial', 9))
        # self.tab1.dwl.setStyleSheet("QPushButton"
        #                       "{"
        #                       "background-color: #C0C0C0; border-radius: 10px;"
        #                       "}")
        self.tab2.dwl.setGeometry(160, 125, 100, 25)
        # self.dwl.move(90, 125)
        self.tab2.dwl.clicked.connect(self.download_search_result)

        # Create clear button
        self.tab2.cls = QPushButton('Clear data', self.tab2)
        self.tab2.cls.setToolTip('Click here to claer the data')
        self.tab2.cls.setFont(QtGui.QFont('Arial', 9))
        self.tab2.cls.setGeometry(270, 125, 100, 25)
        # self.tab1.cls.setStyleSheet("QPushButton"
        #                       "{"
        #                       "background-color: #C0C0C0; border-radius: 10px;"
        #                       "}")
        # self.cls.move(210, 125)
        self.tab2.cls.clicked.connect(self.clear_tab2)

        # Message text
        self.tab2.textmessage = QLabel(self.tab2)
        self.tab2.textmessage.setStyleSheet('color: black')
        self.tab2.textmessage.setText("Ready to download")
        self.tab2.textmessage.setGeometry(390, 130, 300, 15)

        # Search result
        self.tab2.tableWidget = QTableWidget(self.tab2)
        self.tab2.tableWidget.setRowCount(20)
        self.tab2.tableWidget.setColumnCount(3)
        self.tab2.tableWidget.setGeometry(20, 170, 535, 270)
        #self.tab2.tableWidget.horizontalHeader().setVisible(False)
        self.tab2.tableWidget.setHorizontalHeaderLabels(['', 'Title', 'Link'])
        self.tab2.tableWidget.horizontalHeader().setStyleSheet("QHeaderView::section { border-bottom: 1px solid green; }")
        self.tab2.tableWidget.verticalHeader().setVisible(False)
        self.tab2.tableWidget.setShowGrid(False)
        self.tab2.tableWidget.setVisible(False)

    def tab3UI(self):
        # Information
        self.tab3.info = QPlainTextEdit(self.tab3)
        self.tab3.info.setGeometry(30, 40, 515, 350)
        self.tab3.info.insertPlainText('Download videos and music from Youtube' + "\n" + "\n" + "\n")
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
            'https://www.youtube.com/watch?v=0_U4D3Wy-7k&list=RDEMDHx1mzcs_wPqWOntgHDScQ&index=5' + "\n" + "\n")
        self.tab3.info.insertPlainText(
            "In this case, if you want to download all of them, mark the check box: 'Download all related videos'" + "\n" + "\n")

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    @QtCore.pyqtSlot()
    def toggle(self):
        self._toggle = not self._toggle
        self.tab2.boxvd.setChecked(self._toggle)
        self.tab2.boxpl.setChecked(not self._toggle)
        self.tab2.tableWidget.setVisible(False)
        self.tab2.searchtextbox.setText('')
        self.tab2.textmessage.setText("Ready to download")

    def finished(self):
        self.tab1.textmessage.setText('Data download completed')
        print('Finito')

    def clear_tab1(self):
        self.tab1.linktextbox.setText('')
        self.tab1.boxpl.setChecked(False)

    def clear_tab2(self):
        self.tab2.searchtextbox.setText('')
        self.tab2.textmessage.setText("Ready to download")
        #self.tab2.title.clear()
        self.tab2.tableWidget.setVisible(False)

    def download_search_result(self):
        # Download Video & Music
        dwl_choice = 'Video & Music'

        # Define the thread
        self.dwnl_thread = DownloadData(video_id_list_search,
                                        dwl_choice)  # Any other args, kwargs are passed to the run function
        self.dwnl_thread.signal.connect(self.finished)

        # Execute the thread
        self.dwnl_thread.start()
        self.tab2.textmessage.setText('Downloading data')

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
            self.tab1.linktextbox.clear()
            return


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
        self.dwnl_thread = DownloadData(video_id_list,
                                        dwl_choice)  # Any other args, kwargs are passed to the run function
        self.dwnl_thread.signal.connect(self.finished)

        # Execute the thread
        self.dwnl_thread.start()
        self.tab1.textmessage.setText('Downloading data')

    def oh_no_search(self):
        # Reset data result list
        # self.tab2.title.clear()

        # Data to search to download
        search_data = self.tab2.searchtextbox.text()

        video = self.tab2.boxvd.checkState()

        playlist = self.tab2.boxpl.checkState()

        print(video, playlist)

        max_results = 20

        if self.tab2.boxvd.checkState() == 2:
            search = SearchVideos(search_data, offset=1, mode="json", max_results=max_results)
        else:
            search = SearchPlaylists(search_data, offset=1, mode="json", max_results=max_results)

        search_data = json.loads(search.result())

        search_result_dict = search_data['search_result']

        print(search_result_dict)

        # id of videos to download
        global video_id_list_search
        video_id_list_search = []

        # help list of labels
        labels_list = []
        for i in range(max_results):
            labels_list.append('lable' + str(i))

        print(labels_list)

        self.tab2.tableWidget.setVisible(True)

        i = 0
        for link in search_result_dict:
            print(link['link'])

            # Load images only for videos and not playlist
            if self.tab2.boxvd.checkState() == 2:
                url = link['thumbnails'][0]
                print(url)

                data = urllib.request.urlopen(url).read()
                image = QtGui.QImage()
                image.loadFromData(data)

                # loading image
                self.pixmap = QPixmap(image)

                pixmap4 = self.pixmap.scaled(70, 100, QtCore.Qt.KeepAspectRatio)

                pippo = labels_list[i]
                self.tab2.pippo = QLabel(self.tab2)
                self.tab2.pippo.setPixmap(pixmap4)
                self.tab2.tableWidget.setCellWidget(i, 0, self.tab2.pippo)
                self.tab2.pippo.show()
            else:
                self.tab2.tableWidget.setItem(i, 0, QTableWidgetItem('Playlist'))

            self.tab2.tableWidget.setItem(i, 1, QTableWidgetItem(link['title']))
            self.tab2.tableWidget.setItem(i, 2, QTableWidgetItem(link['link']))
            self.tab2.tableWidget.resizeColumnsToContents()

            # self.tab2.title.insertPlainText(link['title'] + "\n" + "\n")
            # self.tab2.title.insertPlainText(link['link'] + "\n" + "\n")
            video_id_list_search.append(link['link'])

            i = i + 1
