from PyQt5 import QtWidgets, QtCore, uic, QtGui
from PyQt5.uic import loadUiType
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QFileDialog, QAction,QTableWidget
from PyQt5 import QtWidgets
from PIL import Image
import cv2
from PyQt5.QtWidgets import QFileDialog,QMessageBox
import sys
from pyqtgraph import PlotWidget
import pyqtgraph as pg
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout,QTableWidgetItem
from PyQt5 import QtCore, QtWidgets, QtMultimedia
import logging
import numpy as np
import matplotlib.pyplot as plt
from numpy import genfromtxt
import pandas as pd
import librosa
import librosa.display
#from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from PIL import Image
# from imagededup.methods import PHash
# phasher = PHash()
import os
import csv
from PyQt5.uic.properties import QtCore
from os.path import dirname, realpath,join
from math import floor 
from pydub import AudioSegment	
count=0
temp2=[]
for filename in os.listdir("./"):
    count+=1
    temp2=temp2+[filename]
    
if(("tempDir" in temp2)==False):
    os.mkdir('tempDir')
if(("back" in temp2)==False):
    os.mkdir('back')
from os import path
import sys


MAIN_WINDOW,_=loadUiType(path.join(path.dirname(__file__),"main (1).ui"))

class MainApp(QMainWindow,MAIN_WINDOW):

    # data = pd.read_csv('hash.csv',encoding='latin-1')
    song=[0,0,0]
    same=[0,0,0]
    # similarity_arr=np.zeros(len(data))
    songs_out=["" for x in range(11)]
    similarity_out=np.zeros(11)
    j=0
    path1=""
    path2=""
    w=0
    
    
    def __init__(self,parent=None):
        super(MainApp,self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.setGeometry(0, 0, 1350, 690)
        self.Buttons=[self.button_1,self.button_2]
        self.actionsong.triggered.connect(self.loaddata(1))
        self.actionsong2.triggered.connect(self.loaddata(2))
          

    def load_arr(self,path):
        if path.endswith(".mp3"):
            sound = AudioSegment.from_mp3(path)
            sound.export("back/new.wav", format="wav")
            path = "back/new.wav"
        ###############################
        t1 = 0 #Works in milliseconds
        t2 = 60*1000
        newAudio = AudioSegment.from_wav(path)
        newAudio = newAudio[t1:t2]
        newAudio.export("back/new.wav", format="wav")
        audio_name = "back/new.wav"
        y, sr = librosa.load(audio_name)
        return(y)

    def loaddata(self,index):
        filename = QFileDialog.getOpenFileName(self)
        if filename[0]:
            self.path1 = filename[0]
        
            
    def song_name(self):
        
        if (self.path1==""):
            data2 =self.load_arr(self.path2)
            new_song = self.w*data2
        elif(self.path2==""):
            data1 = self.load_arr(self.path1)
            new_song = self.w*data1
        else:
            data1 = self.load_arr(self.path1)
            data2 =self.load_arr(self.path2)
            new_song = (self.w*data1)+((1-self.w)*data2)
        
        hop_length = 512
        window_size = 1024
        window = np.hanning(window_size)
        new_song = np.abs(librosa.core.spectrum.stft(new_song, n_fft = window_size, hop_length = hop_length, 
        window=window))
     
        fig = plt.Figure()
        #canvas = FigureCanvas(fig)
        ax = fig.add_subplot(111)
        p=librosa.display.specshow(librosa.amplitude_to_db(new_song, ref=np.max), ax=ax,  y_axis='log', x_axis='time')
        fig.savefig('tempDir/temp.png')
        img = pg.QtGui.QGraphicsPixmapItem(pg.QtGui.QPixmap('tempDir/temp.png'))
        self.ui.widget1.addItem(img)
        self.ui.widget1.invertY(True)
        # Hash = phasher.encode_image(image_array=new_song)
        for i in range(len(self.data)):
            s1= self.data.iloc[i,0]
            # s2=Hash
            self.similarity_arr[i]= self.similarity_check(s1,s2)
        index_max = np.sort(np.argpartition(self.similarity_arr, -11)[-11:])
        for i in index_max:
            self.similarity_out[self.j]=self.similarity_arr[i]
            self.songs_out[self.j]=self.data.iloc[i,1]
            self.j+=1
        self.j=0
        self.loadTable(self.songs_out,self.similarity_out)
        self.ui.label7.setText("{}%".format(round(np.max(self.similarity_out)*100,2)))

def main():
    app = QtWidgets.QApplication(sys.argv)
    application = MainApp()
    application.show()
    app.exec_()


if __name__ == "__main__":
	main()
