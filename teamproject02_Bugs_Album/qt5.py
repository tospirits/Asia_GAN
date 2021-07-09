import datetime
import sys
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtCore import QStringListModel
from PyQt5.QtCore import Qt
import re
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import linear_kernel
from scipy.io import mmread
import pickle
from gensim.models import Word2Vec


form_window = uic.loadUiType('./mainpage.ui')[0] # 파이썬(아나콘다)의 designer로 만든 ui 파일을 클래스 형태로 로드

class MainPage(QWidget, form_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.keywordButton_01.clicked.connect(self.open_recommend_window)
        self.search_album()

    def open_recommend_window(self):
        ResultPage(self)

    def search_album(self):

        df = pd.read_csv('./datasets/cleaned_reviews_tfidf.csv')
        df_album = df.copy()
        df_artist = df.drop_duplicates(['artists'], keep='first', ignore_index=True, inplace=False)
        album_list = list(df_album['album titles'])

        album_list = list(df_album['album titles'])
        artist_list = list(df_artist['artists'])

        model = QStringListModel()
        model.setStringList(artist_list + album_list)

        completer = QCompleter()
        completer.setModel(model)
        self.searchLine.setCompleter(completer)


class ResultPage(QDialog):
    def __init__(self, parent):
        super(ResultPage, self).__init__(parent)

        self.parent = parent
        option_ui = './second.ui'
        uic.loadUi(option_ui, self)
        self.initUI()
        print('DEBUG1')
        self.setWindowTitle("recommend")

        self.exec_()
        print('DEBUG2')

    def initUI(self):

        print('second window')


app = QApplication(sys.argv)
mainWindow = MainPage()
mainWindow.show()
sys.exit(app.exec_())