import os
import sys
import time
import traceback
import youtube_dl
import re
import requests


from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QImage, QPalette, QBrush
from PyQt5.QtWidgets import (QApplication, QDialog,
                             QProgressBar, QLineEdit, QWidget, QPushButton, QMessageBox, QLabel, QProgressDialog)

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


TIME_LIMIT = 100

SAVE_PATH = os.path.expanduser('~/Downloads')

dwl_link = ''
rate = 12

ydl_video = {
    'format': 'best',
    'dumpjson': True,
    'outtmpl': SAVE_PATH + '/_video/%(title)s.%(ext)s',
}

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        print()
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("venv"), relative_path)


class Showbar(QThread):
    """
    Runs a counter thread.
    """
    global rate
    countChanged = pyqtSignal(int)

    aaaa = pyqtSignal(str)

    bbbb = pyqtSignal(str)

    global dwl_link


    def run(self):
        count = 0

        filesize_list = []

        with youtube_dl.YoutubeDL(ydl_video) as ydlvideo:
            result = ydlvideo.extract_info(dwl_link, download=False)
            print('dddddddd')
            #parsed = json.loads(result)
            print(result)
            for key in result:
                if key == 'formats':
                    for i in range(0, len(key)):
                        filesize_list.append(result[key][i]['filesize'])
                        #print(result[key][i]['filesize'])

            #print(result)
            #print(result['filesize'])
            #print(result['duration'])
            #filesize = result['filesize']

        #print(result['filesize'])

        filesize = max(filesize_list)
        print(filesize)

        dwl_time = int(((filesize / 1000000) / rate) * 1.5)

        time_sleep = int((dwl_time / 10) + 1)

        print('Time sleep', time_sleep)


        while count < TIME_LIMIT:
            count += 10
            msg = "downloading"
            #self.counter = count
            time.sleep(time_sleep)
            self.countChanged.emit(count)
            self.aaaa.emit(msg)

        self.bbbb.emit(msg)

class WorkerSignals(QObject):
    '''
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

    '''
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)


class Worker(QRunnable):
    '''
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    '''

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
        '''
        Initialise the runner function with passed args, kwargs.
        '''

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

        #window size and Title
        self.setFixedSize(400, 300)
        self.setWindowTitle('YouDwl')

        self.msg = 'bla bla'

        self.l = QLabel(self)
        self.l.setStyleSheet('color: black')
        self.l.setText(" ")
        self.l.setGeometry(100, 150, 300, 15)

        #window background image

        image_path = "./images/chest-805006__340.webp"

        oImage = QImage(resource_path(image_path))
        #oImage = QImage(image_path)
        sImage = oImage.scaled(QSize(400, 300))  # resize Image to widgets size
        palette = QPalette()
        palette.setBrush(QPalette.Window, QBrush(sImage))
        self.setPalette(palette)


        #self.setStyleSheet("background-color: white;")

        #Information
        self.label = QLabel(self)
        self.label.setStyleSheet('color: black')
        self.label.setFont(QtGui.QFont('SansSerif', 10))
        self.label.setText("Insert the link of the video to download")
        self.label.setGeometry(30, 10, 300, 15)

        #Download link
        self.linktextbox = QLineEdit(self)
        self.linktextbox.move(50, 40)
        self.linktextbox.resize(300, 20)


        # Create dwl button
        self.dwl = QPushButton('Download', self)
        self.dwl.setToolTip('Click here to download your video')
        self.dwl.move(90, 80)
        self.dwl.clicked.connect(self.oh_no)

        # Create close button
        self.cls = QPushButton('Close', self)
        self.cls.setToolTip('Click here to close the window')
        self.cls.move(210, 80)
        self.cls.clicked.connect(self.close)

        #Progress Bar
        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(60, 130, 300, 15)
        self.pbar.setValue(0)

        # Information
        self.instructions1 = QLabel(self)
        self.instructions1.setStyleSheet('color: black')
        self.instructions1.setText("Check your files in:")
        self.instructions1.setGeometry(30, 160, 300, 15)

        # Information
        self.instructions1 = QLabel(self)
        self.instructions1.setStyleSheet('color: black')
        self.instructions1.setFont(QtGui.QFont('SansSerif', 10))
        self.instructions1.setText("\Downloads\_video (MP4)")
        self.instructions1.setGeometry(30, 190, 300, 15)

        # Information
        self.instructions2 = QLabel(self)
        self.instructions2.setStyleSheet('color: black')
        self.instructions2.setFont(QtGui.QFont('SansSerif', 10))
        self.instructions2.setText("\Downloads\_audio (MP3)")
        self.instructions2.setGeometry(30, 215, 300, 15)

        # Information
        self.instructions3 = QLabel(self)
        self.instructions3.setStyleSheet('color: black')
        self.instructions3.setFont(QtGui.QFont('SansSerif', 12))
        self.instructions3.setText("Enjoy!")
        self.instructions3.setGeometry(135, 250, 300, 20)

        self.show()

        self.threadpool = QThreadPool()
        #print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

        '''
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.recurring_timer)
        self.timer.start()
        '''

    def progress_fn(self, n):
        print("%d%% done" % n)

    def execute_this_fn(self, progress_callback):

        global dwl_link

        #Download videos
        with youtube_dl.YoutubeDL(ydl_video) as ydlvideo:
            result = ydlvideo.extract_info(dwl_link, download=False)
            ydlvideo.download([dwl_link])

        # Create audio files
        video_path = os.path.expanduser('~\Downloads\_video')
        audio_path = os.path.expanduser('~\Downloads\_audio')

        for file in os.listdir(video_path):
            if file.endswith(".mp4"):
                filename = file
                filename_new = re.sub(r"\s+", '_', filename)
                # Rename file
                print('jjjjj', filename_new)
                filename_new_mp3 = filename_new[:-4] + '.mp3'
                print('kkkkk', filename_new_mp3)
                old_file = os.path.join(video_path, filename)
                print('old file', old_file)
                new_file = os.path.join(video_path, filename_new)
                print('new file', filename_new)
                print('ttttttttttt', os.listdir(video_path))
                if filename_new not in os.listdir(video_path):
                    os.rename(old_file, new_file)

                ffmpeg_path = "./ffmpeg/ffmpeg.exe"

                #ffmpeg_path = ".\\ffmpeg\\ffmpeg.exe"

                video_name = '\\' + filename_new
                audio_name = '\\' + os.path.splitext(video_name)[0] + '.mp3'

                print(video_name)
                print(audio_name)

                # Generate audio

                print('vvvvvv', os.listdir(audio_path))

                print('llll1', resource_path(ffmpeg_path))
                print('llll2', resource_path(video_path + video_name))
                print('llll3', resource_path(audio_path + audio_name))

                '''
                if filename_new_mp3 not in os.listdir(audio_path):
                    os.system(ffmpeg_path + ' -i ' + resource_path(video_path + video_name) +
                              ' -vn -ar 44100 -ac 2 -ab 192k -f mp3 ' + resource_path(audio_path + audio_name))
                '''

                if filename_new_mp3 not in os.listdir(audio_path):
                    os.system(resource_path(ffmpeg_path) + ' -i ' + resource_path(video_path + video_name) +
                              ' -vn -ar 44100 -ac 2 -ab 192k -f mp3 ' + resource_path(audio_path + audio_name))

    def print_output(self, s):
        print(s)

    def thread_complete(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Download completed and audio file created, check your folders")
        # msg.setInformativeText('More information')
        msg.setWindowTitle("Ready")
        msg.exec_()


        self.pbar.setValue(0)
        self.linktextbox.clear()
        self.l.setText(" ")

        print("THREAD COMPLETE!")

    def oh_no(self):

        global dwl_link

        dwl_link = self.linktextbox.text()

        print('kkkdddddddddddddddddd', dwl_link)


        if 'list' in dwl_link:
            print('this is a list')
            result = dwl_link.find('list')
            print("Substring 'for ' found at index:", result - 1)
            print(dwl_link[0:result])
            dwl_link = dwl_link[0:result]
            print('hgjgjgglgl',dwl_link)

        try:
            request = requests.get(dwl_link)
            print('sssssssssssssss')
            print(request.status_code)
            print('Web site exists')
        except:
            print('Web site does not exist')
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Not valid link")
            # msg.setInformativeText('More information')
            msg.setWindowTitle("Warning")
            msg.exec_()
            self.pbar.setValue(0)
            self.linktextbox.clear()
            self.l.setText(" ")
            return

        #create directories
        video_directory = os.path.join(SAVE_PATH, '_video')

        if not os.path.isdir(video_directory):
            os.mkdir(video_directory)

        audio_directory = os.path.join(SAVE_PATH, '_audio')

        if not os.path.isdir(audio_directory):
            os.mkdir(audio_directory)

        self.calc = Showbar()
        self.calc.countChanged.connect(self.onCountChanged)
        self.calc.aaaa.connect(self.messageSend)
        self.calc.bbbb.connect(self.messageSend1)
        self.calc.start()

        # Pass the function to execute
        worker = Worker(self.execute_this_fn)  # Any other args, kwargs are passed to the run function
        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.progress.connect(self.progress_fn)

        # Execute
        self.threadpool.start(worker)

    def onCountChanged(self, value):
        self.pbar.setValue(value)

    def messageSend(self, msg):
        self.msg = 'downloading'
        print(self.msg)
        self.l.setText("Dowloading the video")

    def messageSend1(self, msg):
        self.msg = 'creating'
        print(self.msg)
        self.l.setText("Creating audio file")


    def recurring_timer(self):

        '''
        s = speedtest.Speedtest()
        s.get_servers()
        #s.get_best_server()
        s.download()
        res = s.results.dict()

        rate = res["download"] * 0.125 / 1000000
        print(res["download"] * 0.125 / 1000000)

        self.timer.stop()
        '''

        self.counter += 1
        self.l.setText("Counter: %d" % self.counter)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
