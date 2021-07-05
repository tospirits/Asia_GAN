import pandas as pd
from konlpy.tag import Okt
import re
from nltk.corpus import stopwords

df = pd.read_csv('./crawling/album_reviews.csv', index_col=0)
print(df.head())
print(df.info())

df['textdata'] = df['artists'] + ' ' + df['review titles'] + ' ' + df['reviews']
print(df.head())
print(df.info())

sentence = re.sub('[^A-Za-z0-9가-힣| ' ']', ' ', df.iloc[0, 4])
print(sentence)

okt = Okt()
token = okt.pos(sentence, stem=True)
print(token)

df_token = pd.DataFrame(token, columns=['word', 'class'])
print(df_token.head())

df_cleaned_token = df_token[(df_token['class'] == 'Noun') |
                            (df_token['class'] == 'Verb') |
                            (df_token['class'] == 'Adjective') |
                            (df_token['class'] == 'Alpha')]
print(df_cleaned_token.head(20))

kor_stopwords = pd.read_csv('./datasets/stopwords.csv', index_col=0)
eng_stopwords = set(stopwords.words('english'))

album_stopwords = ['벅스', '앨범', '작품', '순위', '보컬', '참여', '음악', '작사', '작곡',
                   '편곡', '노래', '글', '제공', '필자', '정규앨범', '수록곡', '작사가',
                   '작곡가', '뮤직비디오', '앨범명', 'CD']     # *집 제거 필요
stopwords_list = list(kor_stopwords.stopword) + list(eng_stopwords) + album_stopwords

words = []
for word in df_cleaned_token['word']:
    if len(word) > 1:
        if word not in stopwords_list:
            words.append(word)
print(words)

cleaned_sentence = ' '.join(words)
