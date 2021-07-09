import datetime
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
#from PyQt5.QtCore import QCoreApplication
from tkinter import messagebox as msg
from tkinter import Tk
import pickle
import re
from konlpy.tag import Okt
import pandas as pd
import numpy as np

from PyQt5.QtCore import QStringListModel
from PyQt5.QtCore import Qt


class recommend_window(QDialog):
    def __init__(self, parent):

        super(recommend_window, self).__init__(parent)

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

form_window = uic.loadUiType('./first.ui')[0] # 파이썬(아나콘다)의 designer로 만든 ui 파일을 클래스 형태로 로드
form_window2 = uic.loadUiType('./second.ui')[0]
class Word(QWidget, form_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.keyword_1.clicked.connect(self.open_recommend_window)

        self.init_widget()
        '''self.writeButton.clicked.connect(self.saveFile)     # 글쓰기 버튼을 누르면 SaveFile 함수 실행
        self.titleBox.selectionChanged.connect(self.titleInput)     # 제목을 입력할 때 '제목을 입력하세요.' 없애는 titleInput 함수 실행
        self.titleBox.editingFinished.connect(self.titleNotInput)       # 제목을 다 썼을 때 빈칸일 경우 '제목을 입력하세요.'를 띄우는 titleNotInput 함수 실행
        self.catButton1.clicked.connect(self.recommendCategory)     # 카테고리 1번 버튼을 누르면 카테고리 추천 함수 실행
        self.catButton2.clicked.connect(self.recommendCategory)     # 카테고리 2번 버튼을 누르면 카테고리 추천 함수 실행
        self.catButton3.clicked.connect(self.recommendCategory)     # 카테고리 3번 버튼을 누르면 카테고리 추천 함수 실행
        self.catDirectBox.clicked.connect(self.defineCategory)      # 카테고리 직접 선택 박스를 누르면 카테고리 지정 함수 실행
        self.catBox.currentIndexChanged.connect(self.defineCategory)    # 카테고리 콤보 박스를 변경하면 카테고리 지정 함수 실행'''

        '''global wordCategory, model, token, encoder      # not defined 오류 방지를 위해 해당 값 전역함수로 지정
        wordCategory = ''
        model = load_model('./models/news_classification_0.5515461564064026.h5')
        with open('./datasets/nonum_withspcl_morphs_token.pickle', 'rb') as f:
            token = pickle.load(f)
        with open('./datasets/category_5000_withnum_encoder.pickle', 'rb') as f:
            encoder = pickle.load(f)'''

    def init_widget(self):

        df = pd.read_csv('./datasets/cleaned_reviews_tfidf.csv')
        df_album = df.copy()
        df_artist = df.drop_duplicates(['artists'], keep='first', ignore_index=True, inplace=False)
        album_list = list(df_album['album titles'] + '\t(앨범)')
        artist_list = list(df_artist['artists'] + '\t(아티스트)')

        model = QStringListModel()
        model.setStringList(artist_list + album_list)

        completer = QCompleter()
        completer.setModel(model)
        self.search.setCompleter(completer)


    def open_recommend_window(self):
        print('open window')
        recommend_window(self)




app = QApplication(sys.argv)
mainWindow = Word()
mainWindow.show()
sys.exit(app.exec_())