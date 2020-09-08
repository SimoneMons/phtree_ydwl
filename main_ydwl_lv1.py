import os
import sys
import traceback
import youtube_dl
import re
import requests
import json

from youtubesearchpython import SearchVideos

from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtGui import QImage, QPalette, QBrush, QIcon
from PyQt5.QtWidgets import QProgressBar, QLineEdit, QPushButton, QMessageBox, QLabel, QCheckBox, QTabWidget

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from download_fn import helper

import showbar

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


class WorkerSignals(QObject):
    """
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data

    error
        `tuple` (exctype, value, traceback.format_exc() )

    result
        `object` data returned from processing, anything

    progress
        `int` indicating % progress

    """
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)


class Worker(QRunnable):
    """
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    """

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        # Add the callback to our kwargs
        self.kwargs['progress_callback'] = self.signals.progress

    @pyqtSlot()
    def run(self):
        """
        Initialise the runner function with passed args, kwargs.
        """

        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # window size and Title
        self.setFixedSize(500, 400)
        self.setWindowTitle('YouDwl')

        # self.msg = 'bla bla'

        self.l = QLabel(self)
        self.l.setStyleSheet('color: black')
        self.l.setText("Ready to download")
        self.l.setGeometry(100, 165, 300, 15)

        # .exe
        # background_image_path = "./images/istockphoto-1172479732-170667a.jpg"
        # icon_image_path = "./images/totoro.png"

        # pycharm exe
        background_image_path = "C:\Proyectos\phtree\phtree_ydwl\images\\istockphoto-1172479732-170667a.jpg"
        icon_image_path = "C:\Proyectos\phtree\phtree_ydwl\images\\totoro.png"

        # Icon
        # self.setWindowIcon(QIcon(icon_image_path))
        self.setWindowIcon(QIcon(resource_path(icon_image_path)))

        # window background image
        oImage = QImage(resource_path(background_image_path))
        sImage = oImage.scaled(QSize(500, 400))  # resize Image to widgets size
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))
        self.setPalette(palette)

        # self.setStyleSheet("background-color: white;")

        # Information
        self.label = QLabel(self)
        self.label.setStyleSheet('color: black')
        self.label.setFont(QtGui.QFont('Arial', 10))
        self.label.setText("Insert the downloading video link or playlist")
        self.label.setGeometry(50, 10, 300, 20)

        # Download link
        self.linktextbox = QLineEdit(self)
        self.linktextbox.move(50, 40)
        self.linktextbox.resize(300, 20)
        self.linktextbox.returnPressed.connect(self.oh_no)

        # check box playlist
        self.boxpl = QCheckBox("Download related videos", self)
        # self.box.stateChanged.connect(self.clickBox)
        self.boxpl.move(200, 70)
        self.boxpl.resize(320, 40)

        # combo choice
        self.combo_choice = QComboBox(self)
        self.combo_choice.addItem("Video & Music")
        self.combo_choice.addItem("Only Music")
        self.combo_choice.addItem("Only Video")
        self.combo_choice.setStyleSheet("QComboBox"
                                        "{"
                                        "background-color: white;"
                                        "}")
        self.combo_choice.move(70, 80)
        self.combo_choice.resize(100, 20)

        # Create dwl button
        self.dwl = QPushButton('Download', self)
        self.dwl.setToolTip('Click here to download your video')
        self.dwl.setFont(QtGui.QFont('Arial', 9))
        self.dwl.setStyleSheet("QPushButton"
                               "{"
                               "background-color: #C0C0C0; border-radius: 10px;"
                               "}")
        self.dwl.setGeometry(90, 125, 100, 25)
        # self.dwl.move(90, 125)
        self.dwl.clicked.connect(self.oh_no)

        # Create info button
        self.info = QPushButton('Help', self)
        self.info.setStyleSheet("QPushButton"
                                "{"
                                "background-color: #C0C0C0; border-radius: 10px;"
                                "}")

        self.info.setToolTip('Help')
        self.info.setFont(QtGui.QFont('Arial', 9))
        self.info.setGeometry(395, 10, 70, 25)
        # self.dwl.move(90, 125)
        self.info.clicked.connect(self.helper)

        # Create close button
        self.cls = QPushButton('Close', self)
        self.cls.setToolTip('Click here to close the window')
        self.cls.setFont(QtGui.QFont('Arial', 9))
        self.cls.setGeometry(210, 125, 100, 25)
        self.cls.setStyleSheet("QPushButton"
                                "{"
                                "background-color: #C0C0C0; border-radius: 10px;"
                                "}")
        # self.cls.move(210, 125)
        self.cls.clicked.connect(self.close)

        # Progress Bar
        # self.pbar = QProgressBar(self)
        # self.pbar.setGeometry(65, 175, 300, 15)
        # self.pbar.setValue(0)

        # Information
        self.instructions1 = QLabel(self)
        self.instructions1.setStyleSheet('color: black')
        self.instructions1.setText("Check your files in:")
        self.instructions1.setFont(QtGui.QFont('Arial', 10))
        self.instructions1.setGeometry(30, 210, 300, 20)

        # Information
        self.instructions2 = QLabel(self)
        self.instructions2.setStyleSheet('color: black')
        self.instructions2.setFont(QtGui.QFont('Arial', 10))
        self.instructions2.setText("\Downloads\_video (MP4)")
        self.instructions2.setGeometry(30, 240, 300, 20)

        # Information
        self.instructions3 = QLabel(self)
        self.instructions3.setStyleSheet('color: black')
        self.instructions3.setFont(QtGui.QFont('Arial', 10))
        self.instructions3.setText("\Downloads\_audio (MP3)")
        self.instructions3.setGeometry(30, 270, 300, 20)

        # Information
        self.instructions4 = QLabel(self)
        self.instructions4.setStyleSheet('color: black')
        self.instructions4.setFont(QtGui.QFont('Arial', 7))
        self.instructions4.setText("Enjoy, by Mons 2020")
        self.instructions4.setGeometry(385, 380, 300, 20)

        self.show()

        self.threadpool = QThreadPool()

    '''
    
    def clickBox(self, state):

        if state == QtCore.Qt.Checked:
            print('Checked')

        else:
            print('Unchecked')
            print(state)
    '''

    def helper(self):
        """Display help."""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)

        msg.setText("With this program you can download videos and music from Youtube")
        msg.setInformativeText("You have to introduce a valid link: see examples clicking on Show Details")
        msg.setWindowTitle("Help")
        msg.setDetailedText("Simple link:"
                            "\r\n"
                            "https://www.youtube.com/watch?v=UojBaKX5Vz4"
                            "\r\n"
                            "\n"
                            "Valid Playlist link:"
                            "\r\n"
                            "https://www.youtube.com/playlist?list=RDEMDHx1mzcs_wPqWOntgHDScQ"
                            "\r\n"
                            "\n"
                            "List of related videos:"
                            "\r\n"
                            "In this case if you want to download all of them mark the check box: 'Download all related videos'"
                            "\r\n"
                            "https://www.youtube.com/watch?v=0_U4D3Wy-7k&list=RDEMDHx1mzcs_wPqWOntgHDScQ&index=5"
                            )
        msg.exec_()

    def progress_fn(self, n):
        print("%d%% done" % n)

    def execute_this_fn(self, progress_callback):

        # Download videos
        dwl_list = self.boxpl.checkState()

        download_choice = text = str(self.combo_choice.currentText())

        print(download_choice)

        print('Single link: ', dwl_link)

        print('List of videos: ', video_id_list)

        # .exe
        # ffmpeg_path = "./ffmpeg/ffmpeg.exe"

        # pycharm exe
        ffmpeg_path = ".\\ffmpeg\\ffmpeg.exe"

        video_path = os.path.expanduser('~\Downloads\_video')
        audio_path = os.path.expanduser('~\Downloads\_audio')

        # Only music
        if download_choice == 'Only Music':
            self.l.setText("Downloading Music")
            if dwl_list == 2:
                with youtube_dl.YoutubeDL(ydl_audio) as ydlaudio:
                    for id_video in video_id_list:
                        ydlaudio.download(['https://www.youtube.com/watch?v=' + id_video])

            else:
                with youtube_dl.YoutubeDL(ydl_audio) as ydlaudio:
                    ydlaudio.download([dwl_link])

            # convert to webm to mp3
            arr_webm = [x for x in os.listdir(audio_path) if x.endswith(".webm") or x.endswith(".m4a")]
            print(arr_webm)

            self.l.setText("Creating MP3 files")

            for file in arr_webm:
                filename_old = file
                # filename_new_ap = re.sub(r"\s+", '_', filename_old)
                # filename_new = re.sub(r"&+", '_', filename_new_ap)

                filename_new = filename_old.replace("&", "_")

                filename_new = filename_new.replace(" ", "_")

                os.rename(audio_path + '\\' + filename_old, audio_path + '\\' + filename_new)
                print('old ', filename_old)
                print('new ', filename_new)
                # pycharm exe
                os.system(ffmpeg_path + ' -i ' + audio_path + '\\' + filename_new +
                          ' -vn -ar 44100 -ac 2 -ab 192k -f mp3 ' + audio_path + '\\' + filename_new[:-5] + '.mp3')

                # exe
                # os.system(resource_path(ffmpeg_path) + ' -i ' + audio_path + '\\' + filename_new +
                #          ' -vn -ar 44100 -ac 2 -ab 192k -f mp3 ' + audio_path + '\\' + filename_new[:-5] + '.mp3')

                os.remove(audio_path + '\\' + filename_new)

        # Only video
        elif download_choice == 'Only Video':
            self.l.setText("Downloading Videos")
            with youtube_dl.YoutubeDL(ydl_video) as ydlvideo:
                if dwl_list == 2:
                    # print('downloading all files', video_id_list)
                    for id_video in video_id_list:
                        ydlvideo.download(['https://www.youtube.com/watch?v=' + id_video])
                else:
                    ydlvideo.download([dwl_link])

        else:
            self.l.setText("Downloading Videos")
            with youtube_dl.YoutubeDL(ydl_video) as ydlvideo:
                if dwl_list == 2:
                    # print('downloading all files', video_id_list)
                    for id_video in video_id_list:
                        ydlvideo.download(['https://www.youtube.com/watch?v=' + id_video])
                else:
                    ydlvideo.download([dwl_link])

            # Create audio files
            self.l.setText("Creating MP3 files")

            for file in os.listdir(video_path):
                if file.endswith(".mp4"):
                    filename = file
                    filename_new = re.sub(r"\s+", '_', filename)
                    # Rename file

                    filename_new_mp3 = filename_new[:-4] + '.mp3'

                    old_file = os.path.join(video_path, filename)

                    new_file = os.path.join(video_path, filename_new)

                    if filename_new not in os.listdir(video_path):
                        os.rename(old_file, new_file)

                    video_name = '\\' + filename_new
                    audio_name = '\\' + os.path.splitext(video_name)[0] + '.mp3'

                    # print(video_name)
                    # print(audio_name)

                    # Generate audio
                    # pycharm exe
                    if filename_new_mp3 not in os.listdir(audio_path):
                        os.system(ffmpeg_path + ' -i ' + resource_path(video_path + video_name) +
                                  ' -vn -ar 44100 -ac 2 -ab 192k -f mp3 ' + resource_path(audio_path + audio_name))

                    # .exe
                    # if filename_new_mp3 not in os.listdir(audio_path):
                    #    os.system(resource_path(ffmpeg_path) + ' -i ' + resource_path(video_path + video_name) +
                    #              ' -vn -ar 44100 -ac 2 -ab 192k -f mp3 ' + resource_path(audio_path + audio_name))

    def print_output(self, s):
        print('')

    def thread_complete(self):
        # print('aquioooooooooooooooooo')
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Download completed, check your folders")
        # msg.setInformativeText('More information')
        msg.setWindowTitle('Ready')
        msg.exec_()

        # self.pbar.setValue(0)
        self.linktextbox.clear()
        self.l.setText(" ")

        print("DOWNLOAD ENDED")

    def oh_no(self):

        # link to download
        global dwl_link
        global video_id_list

        dwl_link = ''
        video_id_list = []

        dwl_link = self.linktextbox.text()

        # Check link
        try:
            request = requests.get(dwl_link)
            print('Web site exists')
        except:
            print('Web site does not exist')

            aaa = 'yeye'
            buttonReply = QMessageBox.question(self, 'PyQt5 message', "Do you like PyQt5?" + "\n" + aaa,
                                               QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if buttonReply == QMessageBox.Yes:
                print('Yes clicked.')
            else:
                print('No clicked.')

            '''
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Not valid link")
            # msg.setInformativeText('More information')
            msg.setWindowTitle("Warning")
            msg.exec_()
            self.pbar.setValue(0)
            self.linktextbox.clear()
            self.l.setText(" ")
            '''
            return

        # create directories
        video_directory = os.path.join(SAVE_PATH, '_video')

        if not os.path.isdir(video_directory):
            os.mkdir(video_directory)

        audio_directory = os.path.join(SAVE_PATH, '_audio')

        if not os.path.isdir(audio_directory):
            os.mkdir(audio_directory)

        dwl_link = self.linktextbox.text()

        #

        if 'playlist' in dwl_link:
            print('It is a playlist')

        # validate if the link is a list of videos
        elif 'watch?v=' and '&list' in dwl_link:
            # Related videos to download
            r = requests.get(dwl_link)
            page_source = r.text
            for m in re.finditer('":{"url":"/watch?', page_source):
                video_id = page_source[m.start() + 19:m.end() + 90]
                print('videossssss', video_id)
                if 'index=' in video_id:
                    video_id = video_id.split('\\')[0]
                    if video_id not in video_id_list:
                        video_id_list.append(video_id)

            # Original link
            result = dwl_link.find('list')
            # print('link result', result)
            dwl_link = dwl_link[0:result]
            print('linkkk0 ', dwl_link)

        '''
        self.calc = showbar.Showbar(dwl_link)
        self.calc.countChanged.connect(self.onCountChanged)
        self.calc.aaaa.connect(self.messageSend)
        self.calc.bbbb.connect(self.messageSend1)
        self.calc.start()
        '''

        # Pass the function to execute
        worker = Worker(self.execute_this_fn)  # Any other args, kwargs are passed to the run function
        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.progress.connect(self.progress_fn)

        # Execute
        self.threadpool.start(worker)

    def onCountChanged(self, value):
        self.pbar.setValue(value)

    def messageSend(self):
        self.l.setText("Dowloading the video")

    def messageSend1(self):
        self.l.setText("Creating audio file")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
