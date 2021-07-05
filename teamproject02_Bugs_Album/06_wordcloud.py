# -*- coding: utf-8 -*-
"""Untitled21.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/18_jHsIWKJM1Q3V4ddOrfTRBh8t5cgdVA
"""

import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import collections
from konlpy.tag import Okt
import matplotlib as mpl
from matplotlib import font_manager, rc
import re

# 한글 폰트 안 깨지도록 설정
#fontpath = '/content/malgun.ttf'
#font_name = font_manager.FontProperties(fname=fontpath).get_name()
#rc('font', family=font_name)
#mpl.font_manager._rebuild()

df = pd.read_csv('/content/album_reviews.csv', index_col=0)
df.dropna(inplace=True)


#stopwords_list = pd.read_csv('/content/stopwords.csv',index_col=0)
okt = Okt()


count = 0
cleaned_sentences = []
for sentence in df.reviews:
    count += 1
    if count % 10 == 0:
        print('.', end='')
    if count % 100 == 0:
        print('')
    sentence = re.sub('[^가-힣 ]', '', sentence)
    token = okt.pos(sentence, stem=True)
    df_token = pd.DataFrame(token, columns=['word', 'class'])
    df_cleaned_token = df_token[(df_token['class'] == 'Noun') | 
                                (df_token['class'] == 'Verb') |
                            (df_token['class'] == 'Adjective')]
    words = []
    for word in df_cleaned_token['word']:
        if len(word) > 1:
            #if word not in stopwords_list:
            words.append(word)
    cleaned_sentence = ' '.join(words)
    cleaned_sentences.append(cleaned_sentence)
df['reviews'] = cleaned_sentences
print(df.head())

print(df.head(20))



#print(df.info())

#print(df.head(20))

album_index = df[df['album titles'] == 'Rainbow Sign'].index[0]        # 영화의 첫 번재 인덱스 확인
print(album_index)
print(df.reviews[album_index])
words = df.reviews[album_index].split(' ')        # 문장을 띄어쓰기 기준으로 잘라 문자열 리스트로 반환
print(words)

worddict = collections.Counter(words)       # 유니크한 단어를 뽑아 몇 번 나오는지 빈도 표시
worddict = dict(worddict)
print(worddict)
#워드클라우드 stopwords는 워드클라우드에서 안보고 싶은거 추가하면 됨. 형태소 분리에는 영향없음.
stopwords = ['벅스', '앨범', '작품', '순위', '보컬', '참여', '음악', '작사', '작곡', '편곡', '노래', '글', '제공', '필자', '정규앨범', '수록곡', '작사가', '작곡가', '뮤직비디오', '앨범명', 'CD', '*집','엘범','앨범을','있다','연주','연주자','연주가','모두','모든']
# wordcloud_img = WordCloud(background_color = 'white', max_words = 2000,
#                           font_path = fontpath, stopwords=stopwords).generate_from_frequencies(worddict)
wordcloud_img = WordCloud(background_color = 'white', max_words = 2000,
                          font_path = fontpath, stopwords=stopwords).generate(df.reviews[album_index])
plt.figure(figsize=(8,8))
plt.imshow(wordcloud_img, interpolation='bilinear')
plt.axis('off')     # 눈금 끄기
plt.title(df.iloc[album_index, 0], size=25)
plt.rc('font', family='NanumBarunGothic') 
plt.show()
print(df.iloc[album_index,0])

!sudo apt-get install -y fonts-nanum
!sudo fc-cache -fv
!rm ~/.cache/matplotlib -rf

!pip install konlpy

import numpy as np
import random
from PIL import Image
from wordcloud import WordCloud, STOPWORDS
from palettable.colorbrewer.qualitative import Dark2_8

album_index = df[df['album titles'] == 'Rainbow Sign'].index[0]        # 영화의 첫 번재 인덱스 확인
print(album_index)
print(df.reviews[album_index])
words = df.reviews[album_index].split(' ')        # 문장을 띄어쓰기 기준으로 잘라 문자열 리스트로 반환
print(words)
def color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    return tuple(Dark2_8.colors[random.randint(0,7)])
font = "malgun"
font_path = "/content/%s.ttf" % font

icon = "bird"
icon_path = "/content/%s.png" % icon

wordcloud_img = WordCloud(background_color = 'white', max_words = 2000,mask=mask,
                          font_path = font_path).generate(df.reviews[album_index])
plt.figure(figsize=(8,8))
plt.imshow(wordcloud_img, interpolation='bilinear')
plt.axis('off')     # 눈금 끄기
plt.title(df.iloc[album_index, 0], size=25)
plt.rc('font', family='NanumBarunGothic') 
plt.show()
print(df.iloc[album_index,0])

