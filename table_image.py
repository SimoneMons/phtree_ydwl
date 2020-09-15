from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui
import sys
import urllib.request


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.acceptDrops()
        # set the title
        self.setWindowTitle("Image")

        # setting  the geometry of window
        self.setGeometry(0, 0, 400, 300)


        # Image
        urls =['https://img.youtube.com/vi/tO7CCP7liwI/default.jpg', 'https://img.youtube.com/vi/QtXby3twMmI/default.jpg']

        app = ['lba1', 'lbb2']

        i = 0
        x = 0
        for url in urls:
            data = urllib.request.urlopen(url).read()
            image = QtGui.QImage()
            image.loadFromData(data)

            # loading image
            label_image = 'label_image1'
            pippo = app[i]
            print(pippo)
            self.pippo = QLabel(self)
            self.pixmap = QPixmap(image)

            # adding image to label
            self.pippo.setPixmap(self.pixmap)

            self.pippo.move(70 + x, 200)

            i = i+1

            x = x + 300

        # show all the widgets
        self.show()

    # create pyqt5 app


App = QApplication(sys.argv)

# create the instance of our Window
window = Window()

# start the app
sys.exit(App.exec())