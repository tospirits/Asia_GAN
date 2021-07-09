import datetime
import sys
from PIL import Image
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
from PyQt5 import uic
#from PyQt5.QtCore import QCoreApplication
from tkinter import messagebox as msg
from tkinter import Tk
import re
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import linear_kernel
from scipy.io import mmread
import pickle
from gensim.models import Word2Vec



class recommend_window(QDialog):
    def __init__(self, parent):

        super(recommend_window, self).__init__(parent)

        self.parent = parent
        option_ui = './second2.ui'
        uic.loadUi(option_ui, self)

        self.initUI()

        self.setWindowTitle("recommend")
        images = [self.image_1, self.image_2, self.image_3, self.image_4,
                  self.image_5, self.image_6, self.image_7, self.image_8]
        names = [self.name_1, self.name_2, self.name_3, self.name_4,
                  self.name_5, self.name_6, self.name_7, self.name_8]

        try:
            for k, num in enumerate(nums):
                path = './images/' + str(num) + '.jpg'
                pixmap = QPixmap(path)
                images[k].setPixmap(pixmap)
            for l, content in enumerate(contents):
                names[l].setText(content)
            self.exec_()
        except Exception as e:
            print(e)

    def initUI(self):

        print('second window')

form_window = uic.loadUiType('./first.ui')[0] # 파이썬(아나콘다)의 designer로 만든 ui 파일을 클래스 형태로 로드


class Word(QWidget, form_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.df = pd.read_csv('./cleaned_reviews_tfidf.csv', index_col=0)  # clean data load
        self.df_bugs = pd.read_csv('./bugs_album_reviews.csv', index_col=0)
        self.Tfidf_matrix = mmread('./tfidf_album_review.mtx').tocsr()  # tfidf matrix load
        with open('./tfidf.pickle', 'rb') as f:  # tfidf pickle load
            self.Tfidf = pickle.load(f)
        self.embedding_model = Word2Vec.load('./VS_200_W_8_MC_10_E_100_SG_1.model')

        global keywords
        keywords = [self.keyword_1, self.keyword_2, self.keyword_3, self.keyword_4, self.keyword_5,
                    self.keyword_6, self.keyword_7, self.keyword_8, self.keyword_9]
        for r in range(9):
            keywords[r].clicked.connect(self.open_recommend_window)


    def open_recommend_window(self):
        global nums, contents

        self.object_name = self.sender().objectName()
        if self.object_name == 'keyword_1':
            key_word = '여름'
        if self.object_name == 'keyword_2':
            key_word = '감성'
        if self.object_name == 'keyword_3':
            key_word = '사랑'
        if self.object_name == 'keyword_4':
            key_word = '크리스마스'
        if self.object_name == 'keyword_5':
            key_word = '이별'
        if self.object_name == 'keyword_6':
            key_word = '가을'
        if self.object_name == 'keyword_7':
            key_word = '공부'
        if self.object_name == 'keyword_8':
            key_word = 'OST'
        if self.object_name == 'keyword_9':
            key_word = '여행'


        try:
            sim_word = self.embedding_model.wv.most_similar(key_word, topn=10)
            labels = []
            sentence = []
            for label, _ in sim_word:
                labels.append(label)
            print(labels)
            for i, word in enumerate(labels):
                sentence += [word] * (9 - i)
            # sentence = ' '.join(sentence)
            print(sentence)

            sentence_vec = self.Tfidf.transform(sentence)
            cosine_sim = linear_kernel(sentence_vec, self.Tfidf_matrix)
            recommendation = self.getRecommendation(cosine_sim)
            recommend_df = recommendation.iloc[0:10, 0:2]
            print(recommend_df.head(8))
            print(recommend_df.iloc[0, 0])
            nums = []
            contents = []
            for i in range(8):
                num = self.df_bugs[self.df_bugs['album titles'] == recommend_df.iloc[i, 0]].iloc[0, 0]
                nums.append(num)
                title = self.df_bugs[self.df_bugs['album titles'] == recommend_df.iloc[i, 0]].iloc[0, 1]
                artist = self.df_bugs[self.df_bugs['album titles'] == recommend_df.iloc[i, 0]].iloc[0, 2]
                contents.append(title + ' ' + artist)

            print(nums)
            print(contents)


        except:
            print('ERROR : 일치하는 키워드가 존재하지 않습니다.')

        print('open window')
        recommend_window(self)

    def getRecommendation(self, cosine_sim):      # 코사인 유사도를 높은 순으로 정렬하여 유사한 앨범의 인덱스 구하는 함수
        simScore = list(enumerate(cosine_sim[0]))
        simScore = sorted(simScore, key=lambda x:x[1], reverse=True)
        simScore = simScore[0:30]
        albumidx = [i[0] for i in simScore]
        recAlbumList = self.df.iloc[albumidx]
        return recAlbumList






app = QApplication(sys.argv)
mainWindow = Word()
mainWindow.show()
sys.exit(app.exec_())