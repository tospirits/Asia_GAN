import pandas as pd
from konlpy.tag import Okt
import re

kor_stopwords = pd.read_csv('./datasets/stopwords.csv', index_col=0)

album_stopwords = ['벅스', '앨범', '작품', '순위', '보컬', '참여', '음악', '작사', '작곡',
                   '편곡', '노래', '글', '제공', '필자', '정규앨범', '수록곡', '작사가',
                   '작곡가', '뮤직비디오', '앨범명', 'CD']  # *집 제거 필요
stopwords_list = list(kor_stopwords.stopword) + album_stopwords

# #tfidf_ preprocessing
# df = pd.read_csv('./datasets/album_reviews__.csv', index_col=0)
# print(df.info())
# print(df.head())
#
# #중복 리뷰 삭제
# df.drop(df.index[3082], inplace=True)
# # print(df.duplicated(['album titles', 'artists']).sum())
# df.drop_duplicates(['album titles', 'artists'], keep='first', ignore_index=True, inplace=True)
# # print(df.duplicated(['album titles', 'artists']).sum())
#
# #reviews컬럼에서 벅스선정~ 문장 삭제시키기
# substr = '벅스가'
# nobugs_review = []
# for i in df['reviews']:
#     if i.rfind(substr) is not -1:
#         # print(i)
#         # print(i.rfind(substr))
#         i = i[:i.rfind(substr)] + i[i.rfind(substr)+30:]    #벅스가 선정한~.가 29~30자라서 30자
#         # print('=========================================================')
#         # print(i)
#         nobugs_review.append(i)
#     else:
#         # print('no 벅스가')
#         i = i
#         nobugs_review.append(i)
# print(len(nobugs_review))
#
# #리뷰의 맨 마지막에 (글: 부분 삭제
# substr = '(글:'
# nobugs_review2 = []
# for i in nobugs_review:
#     if i.rfind(substr) is not -1:
#         # print('before no 글=============================', i)
#         i = i[:i.rfind(substr)]
#         # print('no글 ----------------------------------------------------------------', i)
#         nobugs_review2.append(i)
#     else:
#         i = i
#         nobugs_review2.append(i)
# # print(nobugs_review2)
# print(len(nobugs_review2))
# df['textdata'] = df['artists'] + ' ' + df['review titles'] + ' ' + nobugs_review2
#
# count = 0
# cleaned_sentences = []
# for sentence in df.textdata:
#   count += 1
#   if count % 10 == 0:  #10개마다 진행상황 확인
#     print('.', end='')
#   if count % 100 == 0:
#     print('')   #100개마다 줄바꿈하기
#   kor_sentence = re.sub('[^가-힣 | ' ' ]', '', sentence)   #한글, 띄어쓰기만 남기기
#   okt = Okt()
#   token = okt.pos(kor_sentence, stem=True)
#   df_token = pd.DataFrame(token, columns=['word', 'class'])
#   # print(df_token.head())
#
#   df_cleaned_token = df_token[(df_token['class'] == 'Noun') |
#                               (df_token['class'] == 'Adjective')]
#   # print(df_cleaned_token.head(20))
#
#   words = []
#   for word in df_cleaned_token['word']:
#       if len(word) > 1:
#           if word not in stopwords_list:
#               words.append(word)
#
#   #영어
#   eng_sentence = re.sub('[^a-zA-Z]', ' ', sentence)
#   eng_sentence = eng_sentence.replace('CD', '')
#   eng_sentence = eng_sentence.replace('cd', '')
#   eng_word = eng_sentence.split('  ')
#   eng_count = eng_word.count('')
#   for i in range(eng_count):
#       eng_word.remove('')
#   for word in eng_word:
#       words.append(word)
#
# #필요한 숫자
#   num_sentence = re.compile('( \d{2}년대)+').findall(sentence)  #~년대, ~년, 등 숫자 포함 특정 단어 살리기  #4
#   num_sentence += re.compile('( \d{4}년대)+').findall(sentence)  #6
#   num_sentence += re.compile('(\d{4}년 )+').findall(sentence)  #5
#   for i in num_sentence:
#     if len(i) == 5:
#       i = '19'+ i.strip()
#       words.append(i)
#     else:
#       i=i
#       words.append(i)
#   # print(words)
#   cleaned_sentence = ' '.join(words)   #하나의 문자로 이어붙이고
#   cleaned_sentences.append(cleaned_sentence)
#
# df['cleaned_sentences'] = cleaned_sentences
# print(df.head())
# print(df.info())
#
# df = df[['album titles', 'artists', 'cleaned_sentences']]
# print(df.info())
# df.to_csv('./datasets/cleaned_tfidf_ing.csv', encoding='utf-8-sig')


# word2vec_preprocessing
# 영어 지우기, 중복 리뷰 합치기
df = pd.read_csv('./crawling/bugs_album_reviews.csv', index_col=0)
df.drop(df.index[3082], inplace=True)

# reviews컬럼에서 벅스선정~ 문장 삭제시키기
substr = '벅스가'
nobugs_review = []
for i in df['reviews']:
    if i.rfind(substr) != -1:
        i = i[:i.rfind(substr)] + i[i.rfind(substr) + 30:]  # 벅스가 선정한~.가 29~30자라서 30자
        nobugs_review.append(i)
    else:
        print('no 벅스가')
        i = i
        nobugs_review.append(i)
print(len(nobugs_review))

# 리뷰의 맨 마지막에 (글: 부분 삭제
substr = '(글:'
nobugs_review2 = []
for i in nobugs_review:
    if i.rfind(substr) is not -1:
        # print('before no 글=============================', i)
        i = i[:i.rfind(substr)]
        # print('no글 ----------------------------------------------------------------', i)
        nobugs_review2.append(i)
    else:
        i = i
        nobugs_review2.append(i)
# print(nobugs_review2)
print(len(nobugs_review2))
df['textdata'] = df['artists'] + ' ' + df['review titles'] + ' ' + nobugs_review2
print(df.duplicated(['album titles', 'artists'], keep=False).sum())  # 중복 확인

# 중복없는 앨범 데이터 분리
df_unique = df.drop_duplicates(['album titles', 'artists'], keep=False, ignore_index=True)
df_unique = df_unique[['album titles', 'artists', 'textdata']]
print(df_unique.info())

# 중복되는 앨범 데이터분리
df_same = df[df.duplicated(['album titles', 'artists'], keep=False) == True]
df_same = df_same.reset_index()
print(df_same.info())
print(df_same.head())

# 중복 앨범-아티스트 의 리뷰 합치기
one_sentences = []
one_artists = []
for title in df_same['album titles'].unique():  # 중복 앨범 제목 한번씩 뽑
    one_titles = []
    one_titles.append(title)
    title_idx = df_same[df_same['album titles'].isin(one_titles)]  # 중복 앨범의 index값 구해서
    title_idx = title_idx.index[0]
    # print(title_idx)
    temp = df_same[df_same['album titles'] == title]['textdata']  # 중복 앨범의 리뷰들 뽑
    one_sentence = ' '.join(temp)  # 모은 리뷰 붙이기
    one_sentences.append(one_sentence)  # 붙인 리뷰 저장
    one_artists.append(df_same.iloc[title_idx, 2])  # 중복 앨범의 아티스트명 저장

# 개수 맞는지 확인
# print(df_same['album titles'].nunique())
# print(df_same['artists'].nunique())
# print(len(one_artists))
# print(len(one_sentences))

# 중복 앨범의 리뷰 합친 df
df_same = pd.DataFrame(
    {'album titles': df_same['album titles'].unique(), 'artists': one_artists, 'textdata': one_sentences})
print(df_same.info())
print(df_same.head())

# 맨처음에 분리해 놓은 중복 없는 데이터와 있는 데이터 합치기
df_w2v = pd.concat([df_unique, df_same], axis=0, ignore_index=True)
print(df_w2v.info())
print(df_w2v.head())

print('여기까지는 됨')
# 한국어, 숫자 전처리
count = 0
cleaned_sentences = []
for sentence in df_w2v.textdata:
    count += 1
    if count % 10 == 0:  # 10개마다 진행상황 확인
        print('.', end='')
    if count % 100 == 0:
        print('')  # 100개마다 줄바꿈하기
    words = []

    temp = re.sub(r'\b\d{2}년대', ' 19\g<0>', sentence)        # XX년대 => XXXX년대
    temp = re.findall(r"\d{4}년대|\d{4}년|[가-힣 | ' ' ]", temp) # XXXX년대, XXXX년 살리기
    kor_sentence = ''.join(temp)                              # 리스트 => 문자열
    print(kor_sentence)

    okt = Okt()
    token = okt.pos(kor_sentence, stem=True)
    df_token = pd.DataFrame(token, columns=['word', 'class'])
    print(df_token.head(50))

    df_cleaned_token = df_token[(df_token['class'] == 'Noun') |
                                (df_token['class'] == 'Adjective') |
                                (df_token['class'] == 'Number')]  # 숫자포함 특정단어의 class가 Number

    words = []
    for word in df_cleaned_token['word']:
        if len(word) > 1:
            if word not in stopwords_list:
                words.append(word)

    cleaned_sentence = ' '.join(words)  # 하나의 문자로 이어붙이고
    cleaned_sentences.append(cleaned_sentence)

df_w2v['cleaned_sentences'] = cleaned_sentences
print(df_w2v.head())
print(df_w2v.info())

df_w2v = df_w2v[['album titles', 'artists', 'cleaned_sentences']]
print(df.info())
df_w2v.to_csv('./datasets/cleaned_reviews_word2vec.csv', encoding='utf-8-sig')
