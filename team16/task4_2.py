from PyQt5 import QtWidgets, QtCore, uic, QtGui
from PyQt5.uic import loadUiType
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QFileDialog, QAction,QTableWidget
import os
import sys
import matplotlib.pyplot as plot
import librosa 
from pydub import AudioSegment
from tempfile import mktemp
import sklearn
import librosa.display
import numpy as np
from PIL import Image
import imagehash
import pylab
from PyQt5.uic.properties import QtCore
from os.path import dirname, realpath,join
import os
from os import path
import sys



MAIN_WINDOW,_=loadUiType(path.join(path.dirname(__file__),"main (1).ui"))

class MainApp(QMainWindow,MAIN_WINDOW):
  
    def __init__(self,parent=None):
        super(MainApp,self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.setGeometry(0, 0, 1350, 690)
        self.Buttons=[self.button_1,self.button_2]
        # self.actionsong.triggered.connect(lambda: self.mp3Converter(1))
        # self.actionsong2.triggered.connect(lambda: self.mp3Converter(2))
        self.button_1.clicked.connect(self.spectro)
        self.button_2.clicked.connect(self.spectro)

    # def mp3Converter(self,songNumber):
    #     fname= QFileDialog.getOpenFileName( self, 'choose the signal', os.getenv('HOME') ,"mp3(*.mp3)" ) 
    #     self.path = fname[0] 
    #     if self.path =="" :
    #         return
    #     # mp3_audio = AudioSegment.from_file( self.path , format="mp3")[:60000]  # read mp3
    #     wname = mktemp('.wav')  # use temporary file
    #     mp3_audio.export(wname, format="wav")  # convert to wav
    #     if 1 == songNumber :
    #         self.label_2.setText(os.path.splitext(os.path.basename(self.path))[0])
    #         self.Buttons[1].setDisabled(False) 
    #         self.wavsong1,self.samplingFrequency1 =librosa.load(wname)
    #         self.OpenAgain_flag1  =  True


    #         print("file1 read ")

    #     elif 2 == songNumber :
    #         self.label_3.setText(os.path.splitext(os.path.basename(self.path))[0])
    #         #self.Buttons[2].setDisabled(False) 
            
    #         self.horizontalSlider.setDisabled(False)  
    #         self.wavsong2,self.samplingFrequency2 =librosa.load(wname)
    #         self.OpenAgain_flag2  = True

    #         print("file2 read")
    #     # self.tableWidget.clearContents()

    def spectro(self):
        #plotting the spectrogram for .wav####
        if self.fname.endswith(".wav"):
            fig = plot.figure()
            plot.subplot(111)
            self.powerSpectrum, self.freqenciesFound, self.time, self.imageAxis = plot.specgram(self.audio2, Fs=self.samplingrate, cmap=self.cmap)
            plot.colorbar()
            # plot.ylim(self.min_freq_slider.value(),self.max_freq_slider.value())
            plot.xlabel('Time')
            plot.ylabel('Frequency')
            fig.savefig('plot.png')
            plot.close()
            self.upload()
   

    

def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())


if __name__=='__main__':
    main()