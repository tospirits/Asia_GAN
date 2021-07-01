import pandas as pd
from konlpy.tag import Okt
import re

year = input(str('연도를 입력하세요'))

df = pd.read_csv(f'./crawling/reviews_{year}.csv', index_col=0)
print(df.head())

a = '1a25ds94kl가나다라마'
s = re.sub('[^가-힣]', '', a)    # a의 한글 제외 문자는 null 문자로 채우기
print(s)

print(df.iloc[0,1])    # 0행의 리뷰(1번) 컬럼
print('=======================================')
sentence = re.sub('[^가-힣| ' ']', '', df.iloc[0, 1])       # 한글과 띄어쓰기만 남기고 전부 제거
print(sentence)

okt = Okt()
token = okt.pos(sentence, stem=True)        # 동사 원형으로
print(token)

df_token = pd.DataFrame(token, columns=['word', 'class'])
print(df_token.head())

df_cleaned_token = df_token[(df_token['class'] == 'Noun') |
                            (df_token['class'] == 'Verb') |
                            (df_token['class'] == 'Adjective')]     # 명사, 동사, 형용사만
print(df_cleaned_token.head(20))

stopwords = pd.read_csv('./crawling/stopwords.csv', index_col=0)
print(stopwords.head())

movie_stopwords = ['영화', '배우', '감독']        # 유사도 분석하는데 도움 안 되는 단어
stopwords_list = list(stopwords.stopword) + movie_stopwords

words = []
for word in df_cleaned_token['word']:
    if len(word) > 1:       # 한글자 제외
           if word not in stopwords_list:       # 불용어 제외
               words.append(word)
print(words)

cleaned_sentence = ' '.join(words)
print(cleaned_sentence)

count = 0
cleaned_sentences = []
for sentence in df.reviews:
    count += 1
    if count % 10 == 0:
        print('.', end='')
    if count % 100 == 0:
        print('')
    sentence = re.sub('[^가-힣 | ' ']', '', sentence)
    token = okt.pos(sentence, stem=True)
    df_token = pd.DataFrame(token, columns=['word', 'class'])
    df_cleaned_token = df_token[(df_token['class'] == 'Noun') |
                                (df_token['class'] == 'Verb') |
                                (df_token['class'] == 'Adjective')]
    words = []
    for word in df_cleaned_token['word']:
        if len(word) > 1:
            if word not in stopwords_list:
                words.append(word)
    cleaned_sentence = ' '.join(words)
    cleaned_sentences.append(cleaned_sentence)
df['cleaned_sentences'] = cleaned_sentences
print(df.head())

print(df.info())

df = df[['titles', 'cleaned_sentences']]
print(df.info())
df.to_csv(f'./crawling/cleaned_review_{year}.csv')