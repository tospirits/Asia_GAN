import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import collections
from konlpy.tag import Okt
import matplotlib as mpl
from matplotlib import font_manager, rc

# 한글 폰트 안 깨지도록 설정
fontpath = './malgun.ttf'
font_name = font_manager.FontProperties(fname=fontpath).get_name()
rc('font', family=font_name)
mpl.font_manager._rebuild()

df = pd.read_csv('./crawling/one_sentence_review_2020.csv', index_col=0)
df.dropna(inplace=True)
#print(df.info())

#print(df.head(20))

movie_index = df[df['titles'] == '16세의 사운드트랙 (Soundtrack to Sixteen)'].index[0]        # 영화의 첫 번재 인덱스 확인
#print(movie_index)
print(df.reviews[movie_index])
words = df.reviews[movie_index].split(' ')        # 문장을 띄어쓰기 기준으로 잘라 문자열 리스트로 반환
print(words)

worddict = collections.Counter(words)       # 유니크한 단어를 뽑아 몇 번 나오는지 빈도 표시
worddict = dict(worddict)
print(worddict)
stopwords = ['관객', '작품', '주인공', '개봉', '촬영']

# wordcloud_img = WordCloud(background_color = 'white', max_words = 2000,
#                           font_path = fontpath, stopwords=stopwords).generate_from_frequencies(worddict)
wordcloud_img = WordCloud(background_color = 'white', max_words = 2000,
                          font_path = fontpath, stopwords=stopwords).generate(df.reviews[movie_index])
plt.figure(figsize=(8,8))
plt.imshow(wordcloud_img, interpolation='bilinear')
plt.axis('off')     # 눈금 끄기
plt.title(df.titles[movie_index], size=25)
plt.show()