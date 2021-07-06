import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from scipy.io import mmread
import pickle
from gensim.models import Word2Vec

def getRecommendation(cosine_sim):
    simScore = list(enumerate(cosine_sim[0]))
    simScore = sorted(simScore, key=lambda x:x[1], reverse=True)
    simScore = simScore[1:11]
    albumidx = [i[0] for i in simScore]
    recAlbumList = df.iloc[albumidx]
    return recAlbumList

### tfidf를 활용한 앨범 검색 시 유사 앨범 찾기 ###
df = pd.read_csv('./datasets/cleaned_reviews_tfidf.csv', index_col=0)

Tfidf_matrix = mmread('./models/tfidf_album_review.mtx').tocsr()
with open('./models/tfidf.pickle', 'rb') as f:
    Tfidf = pickle.load(f)
"""
got_album = False
while True:
    album_title = str(input('앨범명을 입력해주세요.'))

    if df[df['album titles']==album_title]['album titles'].count() == 0:
        print('ERROR : 일치하는 앨범이 존재하지 않습니다.')
        continue

    elif df[df['album titles']==album_title]['album titles'].count() == 1:
        album_idx = df[df['album titles']==album_title].index[0]
        got_album = True

    else:
        while True:
            artist_for_album = str(input("앨범명이 중복됩니다. 아티스트명을 입력해주세요. 이전 화면으로 가시려면 '이전으로'를 입력해주세요."))
            if artist_for_album == '이전으로':
                break
            try:
                album_idx = df[(df['album titles']==album_title) & (df['artists']==artist_for_album)].index[0]
                got_album = True
                break
            except:
                print('ERROR : 아티스트가 존재하지 않습니다.')
    if got_album == True:
        break


cosine_sim = linear_kernel(Tfidf_matrix[album_idx], Tfidf_matrix)

recommendation = getRecommendation(cosine_sim)
print(recommendation.iloc[:, 0:2])

#####################################
#가수를 이용한 비슷한 가수 찾기#

### tfidf를 활용한 앨범 검색 시 유사 앨범 찾기 ###
df = pd.read_csv('./datasets/cleaned_reviews_tfidf.csv', index_col=0)

Tfidf_matrix = mmread('./models/tfidf_album_review.mtx').tocsr()
with open('./models/tfidf.pickle', 'rb') as f:
    Tfidf = pickle.load(f)


artist = str(input('찾으시는 가수명을 입력해주세요.'))

artist_album_count = df[df['artists']==artist]['album titles'].count()

total_cosine_sim = []
for i in range(artist_album_count):
    album_idx = df[df['artists']==artist].index[i]
    cosine_sim = linear_kernel(Tfidf_matrix[album_idx], Tfidf_matrix)
    if total_cosine_sim == []:
        total_cosine_sim = cosine_sim
    else:
        total_cosine_sim = total_cosine_sim + cosine_sim

recommendation = getRecommendation(total_cosine_sim)
print(recommendation.iloc[:, 0:2])
"""


### word2vec을 활용한 키워드 검색 시 관련 앨범 찾기 ###
embedding_model = Word2Vec.load('./models/VS_100_W_4_MC_5_E_100_SG_1_210706_161315.model')
key_word = '신나다'

sim_word = embedding_model.wv.most_similar(key_word, topn=10)
labels = []
sentence = []
for label, _ in sim_word:
    labels.append(label)
print(labels)
for i, word in enumerate(labels):
    sentence += [word] * (9-i)
#sentence = ' '.join(sentence)
print(sentence)

sentence_vec = Tfidf.transform(sentence)
cosine_sim = linear_kernel(sentence_vec, Tfidf_matrix)
recommendation = getRecommendation(cosine_sim)
print(recommendation.iloc[:, 0:2])