import pandas as pd
from konlpy.tag import Okt
import re
# from nltk.corpus import stopwords

df = pd.read_csv('./crawling/album_reviews.csv', index_col=0)
print(df.head())
print(df.info())

df['textdata'] = df['artists'] + ' ' + df['review titles'] + ' ' + df['reviews']
print(df.head())
print(df.info())

# #한국어만 남겨서 처리
# sentence = re.sub('[^가-힣| ' ']', '', df.iloc[0, 4])
# print(sentence)
#
# okt = Okt()
# token = okt.pos(sentence, stem=True)
# print(token)
#
# df_token = pd.DataFrame(token, columns=['word', 'class'])
# print(df_token.head())
#
# df_cleaned_token = df_token[(df_token['class'] == 'Noun') |
#                             (df_token['class'] == 'Verb') |
#                             (df_token['class'] == 'Adjective')]
# print(df_cleaned_token.head(20))
#
# kor_stopwords = pd.read_csv('./datasets/stopwords.csv', index_col=0)
#
# album_stopwords = ['벅스', '앨범', '작품', '순위', '보컬', '참여', '음악', '작사', '작곡',
#                    '편곡', '노래', '글', '제공', '필자', '정규앨범', '수록곡', '작사가',
#                    '작곡가', '뮤직비디오', '앨범명', 'CD']     # *집 제거 필요
# stopwords_list = list(kor_stopwords.stopword) + album_stopwords
#
# words = []
# for word in df_cleaned_token['word']:
#     if len(word) > 1:
#         if word not in stopwords_list:
#             words.append(word)
# print(words)  #한국어
# #
# # #영어만 남기고
# # eng_sentence = re.sub('[^a-zA-Z]', ' ', df.iloc[0, 4])
# # eng_word = eng_sentence.split('  ')
# # eng_count = eng_word.count('')
# # for i in range(eng_count):
# #     eng_word.remove('')
# # print(eng_word)   #영어
#
# #cleaned_sentence = ' '.join(words)
# #숫자 ~집, ~년,recompile-띄어쓰기기준 ~년대, ~년 살려라.-
# text = df.iloc[2,4]
# num_sentence = re.compile(r'\d\d\d\d년 | \d\d\d\d년대 |\d집')
# num = num_sentence.search(text)
# nums = num.group()
# print(num)
# print(nums)
# #
# # for i in range(len(df['textdata'])):
# #     test = df.iloc[i,4]
# #     num_sentence = re.compile(r'\d\d\d\d년 | \d\d\d\d년대 |\d집')
# #     num = num_sentence.search(text)
# #     nums = num.group()

#전체 preprocess
#리뷰 모든 문장에 적용
count = 0
cleaned_sentences = []
for sentence in df.textdata:
  count += 1
  if count % 10 == 0:  #10개마다 진행상황 확인
    print('.', end='')
  if count % 100 == 0:
    print('')   #100개마다 줄바꿈하기
  kor_sentence = re.sub('[^가-힣 | ' ']', '', sentence)   #한글, 띄어쓰기만 남기기
  okt = Okt()
  token = okt.pos(kor_sentence, stem=True)
  df_token = pd.DataFrame(token, columns=['word', 'class'])
  # print(df_token.head())

  df_cleaned_token = df_token[(df_token['class'] == 'Noun') |
                              (df_token['class'] == 'Verb') |
                              (df_token['class'] == 'Adjective')]
  # print(df_cleaned_token.head(20))

  kor_stopwords = pd.read_csv('./datasets/stopwords.csv', index_col=0)

  album_stopwords = ['벅스', '앨범', '작품', '순위', '보컬', '참여', '음악', '작사', '작곡',
                     '편곡', '노래', '글', '제공', '필자', '정규앨범', '수록곡', '작사가',
                     '작곡가', '뮤직비디오', '앨범명', 'CD']  # *집 제거 필요
  stopwords_list = list(kor_stopwords.stopword) + album_stopwords

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
      words.append(eng_word)

  text = sentence
  num_sentence = re.compile(r'\d\d\d\d년 | \d\d\d\d년대 |\d집')
  num_sentence = num_sentence.search(text)
  num = num_sentence.group()
  words.append(num)

  cleaned_sentence = ' '.join(words)   #하나의 문자로 이어붙이고
  cleaned_sentences.append(cleaned_sentence)
df['cleaned_sentences'] = cleaned_sentences
print(df.head())

print(df.info())

df = df[['album titles', 'cleaned_sentences']]
print(df.info())
df.to_csv('./datasets/cleaned_album_reviews.csv')