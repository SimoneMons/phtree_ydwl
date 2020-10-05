import os, sys
import requests
import re
import youtube_dl
import urllib.request

from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap
from run_trheads import DownloadData, Progressbar

from youtubesearchpython import SearchVideos, SearchPlaylists
import json

# Global variables
max_results = 20
rows_checked = []
download_type = ''

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
        # self.tabs.addTab(self.tab1, "Link")
        self.tabs.addTab(self.tab2, "Search")
        self.tabs.addTab(self.tab3, "Info")

        # self.tab1UI()
        self.tab2UI()
        self.tab3UI()

    def tab2UI(self):

        # Information Search tab 2
        self.tab2.label = QLabel(self.tab2)
        self.tab2.label.setStyleSheet('color: black')
        self.tab2.label.setFont(QtGui.QFont('Arial', 10))
        self.tab2.label.setText("Search your music or video to download")
        self.tab2.label.setGeometry(50, 20, 300, 20)

        # Search tab 2
        self.tab2.searchtextbox = QLineEdit(self.tab2)
        self.tab2.searchtextbox.setGeometry(50, 45, 330, 20)
        self.tab2.searchtextbox.returnPressed.connect(self.oh_no_search)


        # Combo choice

        self.tab2.combo_choice = QComboBox(self.tab2)
        self.tab2.combo_choice.addItem("Only Music")
        self.tab2.combo_choice.addItem("Only Video")
        self.tab2.combo_choice.addItem("Video & Music")
        # self.tab1.combo_choice.setStyleSheet("QComboBox"
        #                                "{"
        #                                "background-color: white;"
        #                                "}")
        self.tab2.combo_choice.move(1045, 200)
        self.tab2.combo_choice.resize(100, 25)
        self._toggle = True

        '''
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
        '''
        # Search button
        self.tab2.search_button = QPushButton('Search', self.tab2)
        self.tab2.search_button.setToolTip('Click here to search your music and videos')
        self.tab2.search_button.setFont(QtGui.QFont('Arial', 10))
        # self.tab1.dwl.setStyleSheet("QPushButton"
        #                       "{"
        #                       "background-color: #C0C0C0; border-radius: 10px;"
        #                       "}")
        self.tab2.search_button.setGeometry(75, 85, 100, 25)
        self.tab2.search_button.clicked.connect(self.oh_no_search)


        # Clear button
        self.tab2.cls = QPushButton('Clear data', self.tab2)
        self.tab2.cls.setToolTip('Click here to clear the data')
        self.tab2.cls.setFont(QtGui.QFont('Arial', 9))
        self.tab2.cls.setGeometry(200, 85, 100, 25)
        # self.tab1.cls.setStyleSheet("QPushButton"
        #                       "{"
        #                       "background-color: #C0C0C0; border-radius: 10px;"
        #                       "}")
        self.tab2.cls.clicked.connect(self.clear_tab2)

        # Download button
        self.tab2.dwl = QPushButton('Download', self.tab2)
        self.tab2.dwl.setToolTip('Click here to download your music & video')
        self.tab2.dwl.setFont(QtGui.QFont('Arial', 9))
        # self.tab1.dwl.setStyleSheet("QPushButton"
        #                       "{"
        #                       "background-color: #C0C0C0; border-radius: 10px;"
        #                       "}")
        self.tab2.dwl.setGeometry(1045, 250, 100, 25)
        self.tab2.dwl.clicked.connect(self.download_search_result)

        # Message text
        self.tab2.textmessage = QLabel(self.tab2)
        self.tab2.textmessage.setStyleSheet('color: black')
        self.tab2.textmessage.setText("Ready to download")
        self.tab2.textmessage.setFont(QtGui.QFont('Arial', 10))
        self.tab2.textmessage.setGeometry(710, 598, 300, 20)

        # Progress bar
        self.tab2.pbar = QProgressBar(self.tab2)
        self.tab2.pbar.setGeometry(300, 600, 390, 15)
        self.tab2.pbar.setValue(0)


        # Search result
        self.tab2.tableWidget = QTableWidget(self.tab2)
        self.tab2.tableWidget.setRowCount(max_results)
        self.tab2.tableWidget.setColumnCount(6)
        self.tab2.tableWidget.setGeometry(20, 150, 1010, 430)
        self.tab2.tableWidget.setHorizontalHeaderLabels(['Check', 'Photo', 'Title', 'Link', 'Duration', 'Views'])
        self.tab2.tableWidget.horizontalHeader().setStyleSheet(
            "QHeaderView::section { border-bottom: 1px solid green; }")
        self.tab2.tableWidget.verticalHeader().setDefaultSectionSize(120)
        self.tab2.tableWidget.verticalHeader().setVisible(True)
        self.tab2.tableWidget.horizontalHeader().setVisible(True)
        self.tab2.tableWidget.setShowGrid(True)
        #self.tab2.tableWidget.setVisible(False)


        # Information
        self.tab2.instructions4 = QLabel(self.tab2)
        self.tab2.instructions4.setStyleSheet('color: black')
        self.tab2.instructions4.setFont(QtGui.QFont('Arial', 7))
        self.tab2.instructions4.setText("Enjoy, by Mons 2020")
        self.tab2.instructions4.setGeometry(1045, 625, 300, 20)

        # photo
        self.tab2.photo_label = QLabel(self.tab2)
        photo_path = './images/Captura.png'
        # Pycharm
        pixmap = QPixmap(photo_path)
        # Exe
        # pixmap = QPixmap(resource_path(photo_path))
        self.tab2.photo_label.setPixmap(pixmap)
        self.tab2.photo_label.setGeometry(1035, 10, 111, 89)

    def tab3UI(self):
        # Information
        self.tab3.info = QPlainTextEdit(self.tab3)
        self.tab3.info.setGeometry(25, 35, 750, 350)
        self.tab3.info.setFont(QtGui.QFont('Arial', 12))
        self.tab3.info.insertPlainText('Download Music and Videos from Youtube' + "\n" + "\n" + "\n")

        self.tab3.info_details = QPlainTextEdit(self.tab3)
        self.tab3.info_details.setGeometry(25, 80, 750, 350)
        self.tab3.info_details.setFont(QtGui.QFont('Arial', 10))
        self.tab3.info_details.insertPlainText(
            'You can search your music or to introduce the link of your favorite video' + "\n" + "\n")
        self.tab3.info_details.insertPlainText(
            'Examples:' + "\n" + "\n")
        self.tab3.info_details.insertPlainText(
            'https://www.youtube.com/watch?v=RB-RcX5DS5A' + "\n" + "\n" + "\n")
        self.tab3.info_details.insertPlainText(
            'https://www.youtube.com/watch?v=Z9AmPSXAOFw&list=RDRB-RcX5DS5A&index=7' + "\n" + "\n" + "\n")
        self.tab3.info_details.insertPlainText(
            'or a Playlist:' + "\n" + "\n")
        self.tab3.info_details.insertPlainText(
            'https://www.youtube.com/playlist?list=RDEMDHx1mzcs_wPqWOntgHDScQ' + "\n" + "\n" + "\n")
        self.tab3.info_details.insertPlainText(
            'Check your download in:' + "\n" + "\n" + "\n")
        self.tab3.info_details.insertPlainText(
            '       \Downloads\yuhook_music' + "\n" + "\n" + "\n")
        self.tab3.info_details.insertPlainText(
            '       \Downloads\yuhook_videos' + "\n" + "\n" + "\n")

        # photo
        self.tab3.photo_label = QLabel(self.tab3)
        photo_path = './images/Captura.png'
        # Pycharm
        pixmap = QPixmap(photo_path)
        # Exe
        # pixmap = QPixmap(resource_path(photo_path))
        self.tab3.photo_label.setPixmap(pixmap)
        self.tab3.photo_label.setGeometry(1035, 10, 111, 89)

        # Information
        self.tab3.instructions4 = QLabel(self.tab3)
        self.tab3.instructions4.setStyleSheet('color: black')
        self.tab3.instructions4.setFont(QtGui.QFont('Arial', 7))
        self.tab3.instructions4.setText("Enjoy, by Mons 2020")
        self.tab3.instructions4.setGeometry(1045, 625, 300, 20)


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

    def clickBox(self, state):

        row = self.tab2.tableWidget.currentRow()
        print(row)
        if state == QtCore.Qt.Checked:
            print('Checked')
            rows_checked.append(row)
        else:
            print('Unchecked')
            rows_checked.remove(row)


    def finished(self):
        self.tab2.textmessage.setText('Data download completed')
        self.tab2.pbar.setValue(0)
        print('Finito')

    def finished_prgb(self):
        self.tab2.textmessage.setText('Creating mp3 files')
        print('Creating MP3 files')


    def clear_tab1(self):
        self.tab1.linktextbox.setText('')
        self.tab1.boxpl.setChecked(False)

    def clear_tab2(self):
        self.tab2.searchtextbox.setText('')
        self.tab2.textmessage.setText("Ready to download")
        self.tab2.tableWidget.setRowCount(0)
        self.tab2.tableWidget.setColumnCount(0)
        self.tab2.tableWidget.setRowCount(max_results)
        self.tab2.tableWidget.setColumnCount(6)
        self.tab2.tableWidget.setHorizontalHeaderLabels(['Check', 'Photo', 'Title', 'Link', 'Duration', 'Views'])
        self.tab2.pbar.setValue(0)



    def download_search_result(self):
        # Download options: Only Video, Only Music, Video & Music
        dwl_choice = str(self.tab2.combo_choice.currentText())
        check_box_list = []
        print('search:', dwl_choice)

        video_id_list_search = []

        for i in range(max_results):
            if i in rows_checked:
                # self.tab2.tableWidget.setCellWidget(i, 0, QCheckBox('dwl', self.tab2))
                dwl_link_val = self.tab2.tableWidget.item(i, 3).text()  # ok
                video_id_list_search.append(dwl_link_val)


        print(rows_checked)
        print(video_id_list_search)

        # Define the thread for downloading
        self.dwnl_thread = DownloadData(video_id_list_search,
                                        dwl_choice)  # Any other args, kwargs are passed to the run function
        self.dwnl_thread.signal.connect(self.finished)

        # Define the thread for progressbar
        self.progressbar_thread = Progressbar()
        self.progressbar_thread.signal_end.connect(self.finished_prgb)

        # Execute the threads
        self.dwnl_thread.start()
        self.progressbar_thread.start()
        self.progressbar_thread.signal_prgb.connect(self.setProgressVal)

        self.tab2.textmessage.setText('Downloading data')


    def setProgressVal(self, val):
        self.tab2.pbar.setValue(val)


    def oh_no_search(self):
        # Data to search to download
        search_data = self.tab2.searchtextbox.text()

        print('oooooooooooooo', search_data)
        if search_data == '':
            self.tab2.textmessage.setText("Insert a title")
            return 0


        search_data_formatted = search_data

        single_search = 0 #Free text

        chk_playlist = 0

        # Format search_data

        # Single video NO list
        if 'watch?v' in search_data:
            single_search = 1
            search_data_formatted = search_data
            print('search 1 = ', search_data_formatted)

        # Single video with list in link
        if 'watch?v=' and '&list' in search_data:
            print('ññññññññññññññññ')
            single_search = 1
            result = search_data.find('list')
            search_data_formatted = search_data[0:result - 1]
            print('search 2 = ', search_data_formatted)

        # Single video with feature in link
        if 'watch?v=' and '&feature' in search_data:
            print('ññññññññññññññññ')
            single_search = 1
            result = search_data.find('feature')
            search_data_formatted = search_data[0:result - 1]
            print('search 2 = ', search_data_formatted)

        # Single playlist
        if 'playlist?list=' in search_data:
            chk_playlist = 1
            single_search = 1
            search_data_formatted = search_data
            print('search 3 = ', search_data_formatted)

        if chk_playlist == 1:
            search = SearchPlaylists(search_data_formatted, offset=1, mode="json", max_results=max_results)
        else:
            search = SearchVideos(search_data_formatted, offset=1, mode="json", max_results=max_results)


        search_data = json.loads(search.result())

        search_result_dict = search_data['search_result']

        print(search_result_dict)


        # help list of labels
        labels_list = []
        for i in range(max_results):
            labels_list.append('lable' + str(i))

        print(labels_list)

        self.tab2.tableWidget.setVisible(True)

        # Search free text
        if single_search == 0:
            self.tab2.tableWidget.setRowCount(0)
            self.tab2.tableWidget.setColumnCount(0)
            self.tab2.tableWidget.setRowCount(max_results)
            self.tab2.tableWidget.setColumnCount(6)
            self.tab2.tableWidget.setHorizontalHeaderLabels(['Check', 'Photo', 'Title', 'Link', 'Duration', 'Views'])
            check_box_list = []
            check_box_in_table = ''
            for i in range(max_results):
                check_box_list.append('checkbox' + str(i))
                check_box_in_table = check_box_list[i]
                self.tab2.check_box_in_table = QCheckBox("dwl", self.tab2)
                self.tab2.tableWidget.setCellWidget(i, 0, self.tab2.check_box_in_table)
                self.tab2.check_box_in_table.stateChanged.connect(self.clickBox)


            # Regular search
            i = 0
            for link in search_result_dict:
                print('kkkkkk', len(search_result_dict))
                print(link['link'])
                print('llll',link['views'])

                # Load images only for videos and not playlist
                # if self.tab2.boxvd.checkState() == 2:
                if chk_playlist == 0:
                    url = link['thumbnails'][0]
                    print(url)

                    data = urllib.request.urlopen(url).read()
                    image = QtGui.QImage()
                    image.loadFromData(data)

                    # loading image
                    self.pixmap = QPixmap(image)

                    pixmap4 = self.pixmap.scaled(120, 90, QtCore.Qt.KeepAspectRatio)

                    pippo = labels_list[i]
                    self.tab2.pippo = QLabel(self.tab2)
                    self.tab2.pippo.setPixmap(pixmap4)
                    self.tab2.tableWidget.setCellWidget(i, 1, self.tab2.pippo)
                    self.tab2.pippo.show()
                else:
                    # if playlist no photo
                    newitem = QTableWidgetItem('')
                    self.tab2.tableWidget.setItem(i, 1, newitem)

                self.tab2.tableWidget.setItem(i, 2, QTableWidgetItem(link['title']))
                self.tab2.tableWidget.setItem(i, 3, QTableWidgetItem(link['link']))
                self.tab2.tableWidget.setItem(i, 4, QTableWidgetItem(link['duration']))
                self.tab2.tableWidget.setItem(i, 5, QTableWidgetItem(str(link['views'])))
                self.tab2.tableWidget.resizeColumnsToContents()

                i += 1

        else:
            self.tab2.tableWidget.setRowCount(0)
            self.tab2.tableWidget.setColumnCount(0)
            self.tab2.tableWidget.setRowCount(1)
            self.tab2.tableWidget.setColumnCount(6)
            self.tab2.tableWidget.setHorizontalHeaderLabels(['Check', 'Photo', 'Title', 'Link', 'Duration', 'Views'])
            link = search_result_dict[0]
            print(link['link'])

            # Load images only for videos and not playlist
            # if self.tab2.boxvd.checkState() == 2:
            if chk_playlist == 0:
                url = link['thumbnails'][0]
                print(url)

                data = urllib.request.urlopen(url).read()
                image = QtGui.QImage()
                image.loadFromData(data)

                # loading image
                self.pixmap = QPixmap(image)

                pixmap4 = self.pixmap.scaled(120, 90, QtCore.Qt.KeepAspectRatio)

                pippo = labels_list[0]
                self.tab2.pippo = QLabel(self.tab2)
                self.tab2.pippo.setPixmap(pixmap4)
                self.tab2.tableWidget.setCellWidget(0, 1, self.tab2.pippo)
                self.tab2.pippo.show()
            else:
                # if playlist no photo
                newitem = QTableWidgetItem('')
                self.tab2.tableWidget.setItem(0, 1, newitem)

            check_box_in_table = 'checkbox1'
            self.tab2.check_box_in_table = QCheckBox("dwl", self.tab2)
            self.tab2.tableWidget.setCellWidget(0, 0, self.tab2.check_box_in_table)
            self.tab2.check_box_in_table.stateChanged.connect(self.clickBox)


            self.tab2.tableWidget.setItem(0, 2, QTableWidgetItem(link['title']))
            self.tab2.tableWidget.setItem(0, 3, QTableWidgetItem(link['link']))
            self.tab2.tableWidget.setItem(0, 4, QTableWidgetItem(link['duration']))
            self.tab2.tableWidget.setItem(0, 5, QTableWidgetItem(link['views']))
            self.tab2.tableWidget.resizeColumnsToContents()

