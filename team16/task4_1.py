from PyQt5 import QtWidgets, QtCore, uic, QtGui
from PyQt5.uic import loadUiType
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QFileDialog, QAction,QTableWidget
# from gui import Ui_MainWindow
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





# #read audio file
# def load_arr(self,path):
#     if path.endswith(".mp3"):
#         sound = AudioSegment.from_mp3(path)
#         sound.export("back/new.wav", format="wav")
#         path = "back/new.wav"
#     ###############################
#     t1 = 0 #Works in milliseconds
#     t2 = 60*1000
#     newAudio = AudioSegment.from_wav(path)
#     newAudio = newAudio[t1:t2]
#     newAudio.export("back/new.wav", format="wav")
#     audio_name = "back/new.wav"
#     y, sr = librosa.load(audio_name)
#     return(y)

scriptDir=dirname(realpath(__file__))
From_Main,_= loadUiType(join(dirname(__file__),"main.ui"))


class MainApp(QtWidgets.QMainWindow,From_Main):
    def __init__(self):
        super(MainApp, self).__init__()
        self.setupUi(self)
        self.setGeometry(0, 0, 1350, 690)
   
    def init_UI(self):     
        self.actionsong.triggered.connect(lambda: self.mp3converter(1))
        self.actionsong2.triggered.connect(lambda: self.mp3converter(2))
        self.button_1.clicked.connect(lambda: self.spectro())
        self.button_2.clicked.connect(lambda: self.spectro())


def mp3Converter(self,songNumber):
    fname= QFileDialog.getOpenFileName( self, 'choose the signal', os.getenv('HOME') ,"mp3(*.mp3)" ) 
    self.path = fname[0] 
    if self.path =="" :
        return
    mp3_audio = AudioSegment.from_file( self.path , format="mp3")[:60000]  # read mp3
    wname = mktemp('.wav')  # use temporary file
    mp3_audio.export(wname, format="wav")  # convert to wav
    if 1 == songNumber :
        self.ui.label_2.setText(os.path.splitext(os.path.basename(self.path))[0])
        self.Buttons[1].setDisabled(False) 
        self.wavsong1,self.samplingFrequency1 =librosa.load(wname)
        self.OpenAgain_flag1  =  True


        print("file1 read ")

    elif 2 == songNumber :
        self.ui.label_3.setText(os.path.splitext(os.path.basename(self.path))[0])
        #self.Buttons[2].setDisabled(False) 
        
        self.ui.horizontalSlider.setDisabled(False)  
        self.wavsong2,self.samplingFrequency2 =librosa.load(wname)
        self.OpenAgain_flag2  = True

        print("file2 read")
    self.ui.tableWidget.clearContents()

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
    app = QtWidgets.QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

