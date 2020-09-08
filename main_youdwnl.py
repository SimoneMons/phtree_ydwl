import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from tabs import youdwnl_tabs

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        # window size and Title
        self.setFixedSize(600, 500)
        self.setWindowTitle('YouDwl')

        self.table_widget = youdwnl_tabs(self)
        self.setCentralWidget(self.table_widget)

        self.show()



    @pyqtSlot()
    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())