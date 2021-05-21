from scipy import signal
import json
import librosa as l
import librosa.display
from numpy import ndarray
from PyQt5 import QtWidgets, QtGui
from PIL import Image
from math import floor 
import pydub
from pydub import AudioSegment	
count=0
temp2=[]
# from updateDB import readJson
from scipy import signal
import json
import librosa as l
from numpy import ndarray
from PyQt5 import QtWidgets, QtCore, uic, QtGui
from PyQt5.uic import loadUiType
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QFileDialog, QAction,QTableWidget
import os
import sys
from os import path
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
from scipy.io import wavfile
# for filename in os.listdir("./"):
#     count+=1
#     temp2=temp2+[filename]
    
# if(("tempDir" in temp2)==False):
#     os.mkdir('tempDir')
# if(("back" in temp2)==False):
#     os.mkdir('back')
# from pathlib import Path


MAIN_WINDOW,_=loadUiType(path.join(path.dirname(__file__),"main (1).ui"))

class MainApp(QMainWindow,MAIN_WINDOW):
  
    def __init__(self,parent=None):
        super(MainApp,self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.setGeometry(0, 0, 1350, 690)
        self.Buttons=[self.button_1,self.button_2]
        self.actionsong.triggered.connect(self.loadFile(1))
        self.actionsong2.triggered.connect(self.loadFile(2))
        # self.button_1.clicked.connect(self.spectro)
        # self.button_2.clicked.connect(self.spectro)
        self.audFiles = [None, None]  # List Containing both songs
        self.audRates = [None, None]  # List contains Songs Rates which must be equal
        self.sampleFreqs = None
        self.sampleTime = None
        self.colorMesh = None
        self.features = None
        self.container = None


    #mainui.py folder
    def loadFile(self, indx):
        audFile, audFormat = QtWidgets.QFileDialog.getOpenFileName(None, "Load Audio File %s"%(indx),
                                                                                    filter="*.mp3")
        audData, audRate = self.mp3ToData(audFile, 60000)
        # self.logger.debug("extraction successful")
        self.audFiles[indx-1] = audData
        self.audRates[indx-1] = audRate
        self.lineEdits[indx-1].setText(audFile.split('/')[-1])

    ## helper folder

    # def loadAudioFile(self, filePath: str, fSeconds: float = None) -> dict:
    #     """
    #     Loads any audio file

    #     :param filePath: relative path of the file
    #     :param fSeconds: number of seconds you want to load, if not it will load all the file
    #     :return: Dictionary contains songName, array of the data, sample rate, dataType of the array
    #     """
    #     if fSeconds:
    #         audioFile = AudioSegment.from_mp3(filePath)[:fSeconds]
    #     else:
    #         audioFile = AudioSegment.from_mp3(filePath)
    #     songName = filePath.split('/')[-1].split('.mp3')[0]
    #     songData = np.array(audioFile.get_array_of_samples())
    #     sampleRate = audioFile.frame_rate
    #     songDataType = songData.dtype
    #     songDictionary = {
    #         "name": songName,
    #         "data": songData,
    #         "sRate": sampleRate,
    #         "dType": songDataType,
    #         "spectrogram_Hash": None,
    #         "melspectrogram_Hash": None,
    #         "mfcc_Hash": None,
    #         "chroma_stft_Hash": None,
    #     }
    #     return songDictionary

    # ## loader folder
    # def loadPath(self, folderPath: str) -> tuple:
    #     """
    #     Gets Path for each file in folder

    #     :param folderPath: relative path of the folder
    #     :return: list containing file name and file path
    #     """
    #     basePath = Path(folderPath)
    #     filesInPath = (item for item in basePath.iterdir() if item.is_file())
    #     for item in filesInPath:
    #         yield (item.stem, item.relative_to(basePath.parent))


    def mp3ToData(self, filePaths: str, fMilliSeconds: float = None) -> tuple:
        """
        Loads MP3 audio file 

        :param filePath: relative path of the file
        :param fSeconds: number of millie seconds you want to load, if not it will load all the file
        :return: data of song and frame rate
        """
        if fMilliSeconds:
            audioFile = AudioSegment.from_mp3(filePaths)[:fMilliSeconds]
        else:
            audioFile = AudioSegment.from_mp3(filePaths)
        data = np.array(audioFile.get_array_of_samples())
        rate = audioFile.frame_rate
        return data, rate

    ## spectrogram folder
    # def __call__(self, songData: ndarray, songSR: int, window:str, fileName:str = None,
    #                 path:str = None, compressed: bool = False, featureize:bool = False):
    #     self._spectrogram(songData, songSR, window)
    #     if featureize:
    #         self.features= self.spectralFeatures(None, self.colorMesh, songSR,window)
    #     print("spectrogram created")

    #     if fileName:
    #         if path is None:
    #             self._saveFormat('', fileName, compressed=compressed, featurize=featureize)
    #             print("saved in main directory .. ")
    #         else:
    #             self._saveFormat(path, fileName, compressed=compressed, featurize=featureize)
    #         print("spectrogram saved")

    # def _spectrogram(self, songData: ndarray, songSampleRate:int=22050, windowType: str="hann")->tuple:
    #     if len(songData.shape) == 2:
    #         print("song is stereo")
    #         print("Converting ..")
    #         self.sampleFreqs, self.sampleTime, self.colorMesh = signal.spectrogram(songData[:, 0],
    #                                                                                 fs=songSampleRate, window=windowType)
    #     else:
    #         self.sampleFreqs, self.sampleTime, self.colorMesh = signal.spectrogram(songData,
    #                                                                                 fs=songSampleRate, window=windowType)
    #     return (self.sampleFreqs, self.sampleTime, self.colorMesh)

    # def _saveFormat(self, folder:str, filename:str, featurize : bool = False, compressed: bool = False):
    #     if compressed:
    #         self.container = {"color_mesh": self.colorMesh.tolist()}
    #     else:
    #         self.container = {'sample_frequencies': self.sampleFreqs.tolist(),
    #                             "sample_time": self.sampleTime.tolist(),
    #                             "color_mesh": self.colorMesh.tolist()}
    #     if featurize:
    #         self.container['features'] = self.features

    #     with open(folder+filename+".json", 'w') as outfile:
    #         json.dump(self.container, outfile)

    # def spectralFeatures(self, song: "ndarray"= None, S: "ndarray" = None, sr: int = 22050, window:'str'='hann'):
    #     return (l.feature.melspectrogram(y=song, S=S, sr=sr, window=window),
    #             l.feature.mfcc(y=song.astype('float64'), sr=sr),
    #             l.feature.chroma_stft(y= song, S=S, sr=sr, window=window))


def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())


if __name__=='__main__':
    main()
                
        