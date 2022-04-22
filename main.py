import sys
import numpy as np
import time
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUi
from scipy.io import loadmat
import cv2
import csv
from scipy.sparse import load_npz, csr_matrix
from im2double_matlab import im2double_matlab
from Gabor_FeaExt import Gabor_FeaExt
from fastEuclideanDistance import fastEuclideanDistance
import paramsPalmNet as param
from adjustFormat import adjustFormat

class MainWindow(QDialog):


    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi('PalmNet.ui', self)
        self.setWindowTitle('PalmNet GUI')
        icon = QIcon('Hand.ico')
        self.setWindowIcon(icon)
        self.testPic.setStyleSheet("background-color: gray; border: 1px solid black")
        self.refPic.setStyleSheet("background-color: gray; border: 1px solid black")
        self.filepath = 'C:\PalmNet_Matlab\PalmNet\images\Tongji_Contactless_Palmprint_Dataset'
        self.image = None
        self.model = None
        self.featureMap = None
        self.refLabel = []
        self.refFilename = None
        self.clearStatusBtn.clicked.connect(self.clearStatus)
        self.loadImgBtn.clicked.connect(self.browseFiles)
        self.loadModelBtn.clicked.connect(self.loadModel)
        self.pic1.setPixmap(QPixmap('python.png'))
        self.classifyBtn.clicked.connect(self.classify)

    def loadModel(self):

        # load model
        model = loadmat('model.mat')
        bestWaveletsAll = []
        for i in range(model['bestWaveletsAll'][0].shape[0]):
            bestWaveletsAll.append(model['bestWaveletsAll'][0][i])
        self.model = bestWaveletsAll

        #load feature map
        featureMap = load_npz('mapFeature.npz')
        self.featureMap = featureMap

        #load test label
        with open('filenameTest.txt', newline='') as f:
            reader = csv.reader(f)
            self.refFilename = list(reader)
            for i in range(len(self.refFilename)):
                self.refLabel.append(int(self.refFilename[i][0][:4]))

        #enable classify Btn
        self.classifyBtn.setEnabled(True)
        self.loadModelBtn.setEnabled(False)
        self.statusTextEdit.append("Loading model successfully!")


    def clearStatus(self):
        self.statusTextEdit.clear()


    def browseFiles(self):
        fname = QFileDialog.getOpenFileName(self, 'Open File', 'C:\PalmNet_Matlab\PalmNet\images\Tongji_Contactless_Palmprint_Dataset', 'Images (*.bmp)')
        self.testPic.setPixmap(QPixmap(fname[0]))
        im = cv2.imread(fname[0])
        im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        im2double = im2double_matlab(im)
        self.image = adjustFormat(im2double)
        self.testLabel.setText("Label :" + str(int(fname[0][-11:-9])) + "\t" + "Filename :" + fname[0][-13:])
        self.statusTextEdit.append("Loading test image successfully!")


    def classify(self):
        start = time.time()
        # feature extraction
        fTest, _ = Gabor_FeaExt(self.image, param, self.model)
        fTest = csr_matrix(fTest).transpose()

        # compute distMatrix
        distMat = fastEuclideanDistance(self.featureMap, fTest).flatten()
        ind = np.argsort(distMat)
        stop = time.time()
        self.refPic.setPixmap(QPixmap(self.filepath + "\\" + self.refFilename[ind[1]][0]))
        self.outputLabel.setText("Label :" + str(self.refLabel[ind[1]]) + "\t" + "Filename :" + self.refFilename[ind[1]][0])
        self.statusTextEdit.append("Classified!")
        self.statusTextEdit.append("Classify time " + str((stop - start)) + ' seconds')


def main():
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
   main()