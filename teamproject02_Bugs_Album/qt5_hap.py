import datetime
import sys
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
from PyQt5 import uic, QtCore
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtCore import QStringListModel
from PyQt5.QtCore import Qt
import re
import pandas as pd
import numpy as np
import random
from sklearn.metrics.pairwise import linear_kernel
from scipy.io import mmread
import pickle
from gensim.models import Word2Vec
import webbrowser



form_window = uic.loadUiType('./mainpage.ui')[0] # 파이썬(아나콘다)의 designer로 만든 ui 파일을 클래스 형태로 로드

class MainPage(QWidget, form_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.search_album()     # 검색창 자동완성 함수
        # csv에서 데이터 로드
        self.df_bugs = pd.read_csv('./crawling/bugs_album_reviews.csv', index_col=0)
        self.df_tfidf = pd.read_csv('./datasets/cleaned_reviews_tfidf.csv', index_col=0)  # clean data load

        # tfidf 매트릭스, 피클, word2vec 모델 로드
        self.Tfidf_matrix = mmread('./models/tfidf_album_review.mtx').tocsr()  # tfidf matrix load
        with open('./models/tfidf.pickle', 'rb') as f:  # tfidf pickle load
            self.Tfidf = pickle.load(f)
        self.embedding_model = Word2Vec.load('./models/VS_200_W_8_MC_10_E_100_SG_1.model')

        global keywords
        keyword_list = ['클래식', '빌보드', '댄스', '힙합', '알앤비', '영화', '애니메이션', '드라마', '크리스마스',
                        '겨울', '여름', '여행', '이별', '사랑', '결혼', '우울', '행복', '배경음악', '아이돌', '걸그룹']   # 20개
        random_keyword_list = random.sample(keyword_list, 15)


        keywords = [self.keywordButton_01, self.keywordButton_02, self.keywordButton_03, self.keywordButton_04, self.keywordButton_05,
                    self.keywordButton_06, self.keywordButton_07, self.keywordButton_08, self.keywordButton_09, self.keywordButton_10,
                    self.keywordButton_11, self.keywordButton_12, self.keywordButton_13, self.keywordButton_14, self.keywordButton_15]

        for r in range(15):
            keywords[r].setText(random_keyword_list[r])

        for r in range(15):
            keywords[r].clicked.connect(self.open_recommend_window)

        ### 하단 랜덤 앨범 3개 띄우기 ###
        df2 = self.df_bugs

        global random_img_list

        img_list = list(df2['album links'])
        random_img_list = random.sample(img_list, 3)

        random_album_list = []
        for m in range(3):
            random_img = self.df_bugs[self.df_bugs['album links'] == random_img_list[m]].iloc[0, 1]
            random_album_list.append(random_img)

        random_artist_list = []
        for m in range(3):
            random_artist = df2[df2['album links']==random_img_list[m]].iloc[0, 2]
            random_artist_list.append(random_artist)

        albumtitleLabel = [self.albumtitleLabel_01, self.albumtitleLabel_02,self.albumtitleLabel_03]
        artistLabel = [self.artistLabel_01, self.artistLabel_02,self.artistLabel_03]
        imgs = [self.albumartLabel_01,self.albumartLabel_02,self.albumartLabel_03]
        for m in range(3):
            path = './images/' + str(random_img_list[m]) + '.jpg'
            pixmap = QPixmap(path)
            imgs[m].setPixmap(pixmap)
        for m in range(3):
            albumtitleLabel[m].setText(random_album_list[m])
        for m in range(3):
            artistLabel[m].setText(random_artist_list[m])

        for i in range(3):
            if len(albumtitleLabel[i].text()) > 24 :
                albumtitleLabel[i].move(180+i*250, 820)
                artistLabel[i].move(180 + i * 250, 850)

        for i in range(3):
            if len(artistLabel[i].text()) > 25 :
                artistLabel[i].move(180 + i * 250, 860)

        self.linkbuttons = [self.linkButton_1, self.linkButton_2, self.linkButton_3]

        for r in range(3):
            self.linkbuttons[r].clicked.connect(self.gotoURL)

        self.searchLine.cursorPositionChanged.connect(self.popimage)
        self.searchDial.sliderReleased.connect(self.activate_dial)


    def gotoURL(self):
        try:
            main_url = 'https://music.bugs.co.kr/album/'

            self.object_name = self.sender().objectName()

            for i in range(3):
                if self.object_name == f'linkButton_{i+1}':
                    imgnum = i

            url = main_url + str(random_img_list[imgnum])
            webbrowser.open(url)
        except Exception as e:
            print(e)

    def popimage(self):
        try:
            searchdata = self.searchLine.text()
            if searchdata.find('(ARTIST)') != -1:       # 앨범이면
                album_title = searchdata.split('(ARTIST)')[0].rstrip()
                main_album_art = self.df_bugs[self.df_bugs['album titles'] == album_title].iloc[0, 0]
                path = './images/' + str(main_album_art) + '.jpg'
                pixmap = QPixmap(path)
                self.mainalbumartLabel.setPixmap(pixmap)

            else:       # 아티스트면
                if len(self.df_bugs[self.df_bugs['artists']==searchdata]) != 0 :
                    artist = searchdata
                    main_album_art_list = list(self.df_bugs[self.df_bugs['artists'] == artist]['album links'])
                    main_album_art = random.sample(main_album_art_list, 1).pop()
                    path = './images/' + str(main_album_art) + '.jpg'
                    pixmap = QPixmap(path)
                    self.mainalbumartLabel.setPixmap(pixmap)


        except Exception as e:
            print(e)




    def activate_dial(self):
        if self.searchDial.value() >= 50:
            self.searchDial.setValue(0)         # 다이얼 초기화
            self.dial_recommend_window()
            return      # return으로 종료해줘야 반복 실행 안 됨
        else:           # 없으면 함수 계속 실행돼서 멈춤
            self.searchDial.setValue(0)  # 다이얼 초기화
            return


    def search_album(self):     # 검색창 자동완성 함수

        df = pd.read_csv('./datasets/cleaned_reviews_tfidf.csv')
        df_album = df.copy()
        df_artist = df.drop_duplicates(['artists'], keep='first', ignore_index=True, inplace=False)
        album_list = list(df_album['album titles'])

        album_list = list(df_album['album titles'] + '      (ARTIST)  ' + df_album['artists'])
        artist_list = list(df_artist['artists'])

        model = QStringListModel()
        model.setStringList(artist_list + album_list)

        completer = QCompleter()
        completer.setModel(model)
        completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)     # 대소문자 구분 없이
        self.searchLine.setCompleter(completer)



    def open_recommend_window(self):
        global nums, contents

        self.errorLabel.setText('')        # 에러표기창 초기화

        self.object_name = self.sender().objectName()

        if self.object_name == 'keywordButton_01':
            key_word = self.keywordButton_01.text()
        if self.object_name == 'keywordButton_02':
            key_word = self.keywordButton_02.text()
        if self.object_name == 'keywordButton_03':
            key_word = self.keywordButton_03.text()
        if self.object_name == 'keywordButton_04':
            key_word = self.keywordButton_04.text()
        if self.object_name == 'keywordButton_05':
            key_word = self.keywordButton_05.text()
        if self.object_name == 'keywordButton_06':
            key_word = self.keywordButton_06.text()
        if self.object_name == 'keywordButton_07':
            key_word = self.keywordButton_07.text()
        if self.object_name == 'keywordButton_08':
            key_word = self.keywordButton_08.text()
        if self.object_name == 'keywordButton_09':
            key_word = self.keywordButton_09.text()
        if self.object_name == 'keywordButton_10':
            key_word = self.keywordButton_10.text()
        if self.object_name == 'keywordButton_11':
            key_word = self.keywordButton_11.text()
        if self.object_name == 'keywordButton_12':
            key_word = self.keywordButton_12.text()
        if self.object_name == 'keywordButton_13':
            key_word = self.keywordButton_13.text()
        if self.object_name == 'keywordButton_14':
            key_word = self.keywordButton_14.text()
        if self.object_name == 'keywordButton_15':
            key_word = self.keywordButton_15.text()


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
                contents.append(title + '\n - ' + artist)

            print(nums)
            print(contents)


        except:
            print('ERROR : 일치하는 키워드가 존재하지 않습니다.')

        print('open window')
        ResultPage(self)

    def dial_recommend_window(self):
        global nums, contents

        self.errorLabel.setText('')  # 에러표기창 초기화

        title = self.searchLine.text()

        if title.find('(ARTIST)') != -1:
            album_title = title.split('(ARTIST)')[0].rstrip()

            try:
                if self.df_tfidf[self.df_tfidf['album titles'] == album_title]['album titles'].count() == 0:  # 일치 앨범 없을 때
                    self.errorLabel.setText('일치하는 앨범 또는 아티스트가 없습니다.')

                elif self.df_tfidf[self.df_tfidf['album titles'] == album_title]['album titles'].count() == 1:  # 일치 앨범 1개일 때

                    album_idx = self.df_tfidf[self.df_tfidf['album titles'] == album_title].index[0]


                cosine_sim = linear_kernel(self.Tfidf_matrix[album_idx], self.Tfidf_matrix)  # 코사인 유사도
                recommendation = self.getRecommendation(cosine_sim)  # 추천 함수 실행
                recommend_df = recommendation.iloc[1:11, 0:2]
                nums = []
                contents = []
                for i in range(8):
                    num = self.df_bugs[self.df_bugs['album titles'] == recommend_df.iloc[i, 0]].iloc[0, 0]
                    nums.append(num)
                    title = self.df_bugs[self.df_bugs['album titles'] == recommend_df.iloc[i, 0]].iloc[0, 1]
                    artist = self.df_bugs[self.df_bugs['album titles'] == recommend_df.iloc[i, 0]].iloc[0, 2]
                    contents.append(title + '\n - ' + artist)

                ResultPage(self)
            except Exception as e:
                print(e)


        else:
            artist = title
            artist_album_count = self.df_tfidf[self.df_tfidf['artists'] == artist]['album titles'].count()
            try:
                if artist_album_count == 0:
                    self.errorLabel.setText('일치하는 앨범 또는 아티스트가 없습니다.')

                else:
                    total_cosine_sim = []  # 각 앨범마다 코사인 유사도를 합친 값 미리 지정
                    for i in range(artist_album_count):
                        album_idx = self.df_tfidf[self.df_tfidf['artists'] == artist].index[i]
                        cosine_sim = linear_kernel(self.Tfidf_matrix[album_idx], self.Tfidf_matrix)
                        if total_cosine_sim == []:  # 첫 번째는
                            total_cosine_sim = cosine_sim  # 0번 인덱스 값 대입
                        else:  # 그 이후는
                            total_cosine_sim = total_cosine_sim + cosine_sim  # 합치기

                    recommendation = self.getRecommendation(total_cosine_sim)
                    recommendation = recommendation[recommendation.artists != artist]  # 해당 아티스트의 앨범 제거

                    recommend_df = recommendation.iloc[0:8, 0:2]
                    nums = []
                    contents = []
                    for i in range(8):
                        num = self.df_bugs[self.df_bugs['album titles'] == recommend_df.iloc[i, 0]].iloc[0, 0]
                        nums.append(num)
                        title = self.df_bugs[self.df_bugs['album titles'] == recommend_df.iloc[i, 0]].iloc[0, 1]
                        artist = self.df_bugs[self.df_bugs['album titles'] == recommend_df.iloc[i, 0]].iloc[0, 2]
                        contents.append(title + '\n - ' + artist)

                    ResultPage(self)

            except Exception as e:
                print(e)



    def getRecommendation(self, cosine_sim):      # 코사인 유사도를 높은 순으로 정렬하여 유사한 앨범의 인덱스 구하는 함수
        simScore = list(enumerate(cosine_sim[0]))
        simScore = sorted(simScore, key=lambda x:x[1], reverse=True)
        simScore = simScore[0:30]
        albumidx = [i[0] for i in simScore]
        recAlbumList = self.df_tfidf.iloc[albumidx]
        return recAlbumList


class ResultPage(QDialog):
    def __init__(self, parent):

        super(ResultPage, self).__init__(parent)

        self.parent = parent
        option_ui = './result.ui'
        uic.loadUi(option_ui, self)

        self.initUI()

        self.linkbuttons = [self.linkButton_1, self.linkButton_2, self.linkButton_3, self.linkButton_4,
                       self.linkButton_5, self.linkButton_6, self.linkButton_7, self.linkButton_8]

        for r in range(8):
            self.linkbuttons[r].clicked.connect(self.gotoURL)


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



    def gotoURL(self):
        try:
            main_url = 'https://music.bugs.co.kr/album/'

            self.object_name = self.sender().objectName()

            for i in range(8):
                if self.object_name == f'linkButton_{i+1}':
                    imgnum = i

            url = main_url + str(nums[imgnum])
            webbrowser.open(url)
        except Exception as e:
            print(e)




    def initUI(self):

        print('second window')
        self.move(500, 500)  # 좌상단 위치


app = QApplication(sys.argv)
mainWindow = MainPage()
mainWindow.show()
sys.exit(app.exec_())