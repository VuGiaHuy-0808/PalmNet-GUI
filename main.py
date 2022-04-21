import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUi

class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi('PalmNet.ui', self)
        self.setWindowTitle('PalmNet GUI')
        icon = QIcon('Hand.ico')
        self.setWindowIcon(icon)
        self.testPic.setStyleSheet("background-color: gray; border: 1px solid black")
        self.loadImgBtn.clicked.connect(self.browseFiles)
        self.pic1.setPixmap(QPixmap('python.png'))

    def browseFiles(self):
        fname = QFileDialog.getOpenFileName(self, 'Open File', 'C:\PalmNet_Matlab\PalmNet\images\Tongji_Contactless_Palmprint_Dataset', 'Images (*.bmp)')
        self.testPic.setPixmap(QPixmap(fname[0]))
        self.label.setText("label : " + fname[0][-11:-9])


def main():
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
   main()