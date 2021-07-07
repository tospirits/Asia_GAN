import pandas as pd
from konlpy.tag import Okt
import re
# from nltk.corpus import stopwords

kor_stopwords = pd.read_csv('./datasets/stopwords.csv', index_col=0)

album_stopwords = ['벅스', '앨범', '작품', '순위', '보컬', '참여', '음악', '작사', '작곡',
                   '편곡', '노래', '글', '제공', '필자', '정규앨범', '수록곡', '작사가',
                   '작곡가', '뮤직비디오', '앨범명', 'CD']  # *집 제거 필요
stopwords_list = list(kor_stopwords.stopword) + album_stopwords

#tfidf_ preprocessing
df = pd.read_csv('./crawling/bugs_album_reviews.csv', index_col=0)
print(df.info())

#중복 리뷰 삭제
print(df.duplicated(['album titles', 'artists']).sum())
df.drop_duplicates(['album titles', 'artists'], keep='first', ignore_index=True, inplace=True)
print(df.duplicated(['album titles', 'artists']).sum())

df['textdata'] = df['artists'] + ' ' + df['review titles'] + ' ' + df['reviews']
print(df.head())
print(df.info())

count = 0
cleaned_sentences = []
for sentence in df.textdata:
  count += 1
  if count % 10 == 0:  #10개마다 진행상황 확인
    print('.', end='')
  if count % 100 == 0:
    print('')   #100개마다 줄바꿈하기
  kor_sentence = re.sub('[^가-힣 | ' ' ]', '', sentence)   #한글, 띄어쓰기만 남기기
  okt = Okt()
  token = okt.pos(kor_sentence, stem=True)
  df_token = pd.DataFrame(token, columns=['word', 'class'])
  # print(df_token.head())

  df_cleaned_token = df_token[(df_token['class'] == 'Noun') |
                              (df_token['class'] == 'Verb') |
                              (df_token['class'] == 'Adjective')]
  # print(df_cleaned_token.head(20))

  words = []
  for word in df_cleaned_token['word']:
      if len(word) > 1:
          if word not in stopwords_list:
              words.append(word)

  #영어
  eng_sentence = re.sub('[^a-zA-Z]', ' ', sentence)
  eng_word = eng_sentence.split('  ')
  eng_count = eng_word.count('')
  for i in range(eng_count):
      eng_word.remove('')
  for word in eng_word:
      words.append(word)

  #필요한 숫자
  num_sentence = re.compile(r' \d*년대 | \d*년 | \d*집 ')  #~년대, ~년, ~집 등 숫자 포함 특정 단어 살리기
  num_sentence = num_sentence.search(sentence)
  if num_sentence is not None:
      num = num_sentence.group()
      words.append(num)

  cleaned_sentence = ' '.join(words)   #하나의 문자로 이어붙이고
  cleaned_sentences.append(cleaned_sentence)

df['cleaned_sentences'] = cleaned_sentences
print(df.head())
print(df.info())

df = df[['album titles', 'artists', 'cleaned_sentences']]
print(df.info())
df.to_csv('./datasets/cleaned_reviews_tfidf.csv', encoding='utf-8-sig')


#word2vec_preprocessing
#영어 지우기, 중복 리뷰 합치기
df = pd.read_csv('./crawling/album_reviews.csv', index_col=0)
df['textdata'] = df['artists'] + ' ' + df['review titles'] + ' ' + df['reviews']
print(df.duplicated(['album titles', 'artists'], keep=False).sum())  #중복 확인
#중복없는 앨범 데이터 분리
df_unique = df.drop_duplicates(['album titles', 'artists'], keep=False, ignore_index=True)
df_unique = df_unique[['album titles', 'artists', 'textdata']]
print(df_unique.info())

#중복되는 앨범 데이터분리
df_same = df[df.duplicated(['album titles', 'artists'], keep=False)==True]
df_same= df_same.reset_index()
print(df_same.info())
print(df_same.head())

#중복 앨범-아티스트 의 리뷰 합치기
one_sentences = []
one_artists = []
for title in df_same['album titles'].unique():  #중복 앨범 제목 한번씩 뽑
    one_titles = []
    one_titles.append(title)
    title_idx = df_same[df_same['album titles'].isin(one_titles)]  #중복 앨범의 index값 구해서
    title_idx = title_idx.index[0]
    # print(title_idx)
    temp = df_same[df_same['album titles']==title]['textdata']  #중복 앨범의 리뷰들 뽑
    one_sentence = ' '.join(temp)  #모은 리뷰 붙이기
    one_sentences.append(one_sentence)  #붙인 리뷰 저장
    one_artists.append(df_same.iloc[title_idx, 2])  #중복 앨범의 아티스트명 저장

#개수 맞는지 확인
# print(df_same['album titles'].nunique())
# print(df_same['artists'].nunique())
# print(len(one_artists))
# print(len(one_sentences))

#중복 앨범의 리뷰 합친 df
df_same = pd.DataFrame({'album titles':df_same['album titles'].unique(), 'artists':one_artists, 'textdata':one_sentences})
print(df_same.info())
print(df_same.head())

#맨처음에 분리해 놓은 중복 없는 데이터와 있는 데이터 합치기
df_w2v = pd.concat([df_unique, df_same], axis=0, ignore_index=True)
print(df_w2v.info())
print(df_w2v.head())

#한국어, 숫자 전처리
count = 0
cleaned_sentences = []
for sentence in df_w2v.textdata:
  count += 1
  if count % 10 == 0:  #10개마다 진행상황 확인
    print('.', end='')
  if count % 100 == 0:
    print('')   #100개마다 줄바꿈하기
  kor_sentence = re.sub('[^가-힣 | ' ' | \d*년대 | \d*년 | \d*집 ]', '', sentence)   #한글, 띄어쓰기, 숫자포함 특정단어만 남기기
  okt = Okt()
  token = okt.pos(kor_sentence, stem=True)
  df_token = pd.DataFrame(token, columns=['word', 'class'])
  # print(df_token.head())

  df_cleaned_token = df_token[(df_token['class'] == 'Noun') |
                              (df_token['class'] == 'Verb') |
                              (df_token['class'] == 'Adjective') |
                              (df_token['class'] == 'Number')]     #숫자포함 특정단어의 class가 Number

  words = []
  for word in df_cleaned_token['word']:
      if len(word) > 1:
          if word not in stopwords_list:
              words.append(word)

  cleaned_sentence = ' '.join(words)   #하나의 문자로 이어붙이고
  cleaned_sentences.append(cleaned_sentence)

df_w2v['cleaned_sentences'] = cleaned_sentences
print(df_w2v.head())
print(df_w2v.info())

df_w2v = df_w2v[['album titles', 'artists', 'cleaned_sentences']]
print(df.info())
df_w2v.to_csv('./datasets/cleaned_reviews_word2vec.csv', encoding='utf-8-sig')