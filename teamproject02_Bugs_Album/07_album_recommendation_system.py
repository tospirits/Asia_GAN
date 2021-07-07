import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from scipy.io import mmread
import pickle
from gensim.models import Word2Vec

def getRecommendation(cosine_sim):      # 코사인 유사도를 높은 순으로 정렬하여 유사한 앨범의 인덱스 구하는 함수
    simScore = list(enumerate(cosine_sim[0]))
    simScore = sorted(simScore, key=lambda x:x[1], reverse=True)
    simScore = simScore[0:30]
    albumidx = [i[0] for i in simScore]
    recAlbumList = df.iloc[albumidx]
    return recAlbumList


### tfidf를 활용한 앨범 검색 시 유사 앨범 찾기 ###
df = pd.read_csv('./datasets/cleaned_reviews_tfidf.csv', index_col=0)       # clean data load

Tfidf_matrix = mmread('./models/tfidf_album_review.mtx').tocsr()        # tfidf matrix load
with open('./models/tfidf.pickle', 'rb') as f:                          # tfidf pickle load
    Tfidf = pickle.load(f)

got_album = False       # 앨범을 찾을 경우 반복문에서 빠져나올 수 있도록 하는 값
while True:
    album_title = str(input('앨범명을 입력해주세요.'))

    if df[df['album titles']==album_title]['album titles'].count() == 0:        # 일치 앨범 없을 때
        print('ERROR : 일치하는 앨범이 존재하지 않습니다.')
        continue

    elif df[df['album titles']==album_title]['album titles'].count() == 1:      # 일치 앨범 1개일 때
        album_idx = df[df['album titles']==album_title].index[0]
        got_album = True

    else:                                                                       # 일치 앨범 2개 이상일 때
        while True:
            artist_for_album = str(input("앨범명이 중복됩니다. 아티스트명을 입력해주세요. 이전 화면으로 가시려면 '이전으로'를 입력해주세요."))
            if artist_for_album == '이전으로':      # 이전 화면으로 가는 기능
                break
            try:                                  # 올바른 아티스트명을 입력할 경우 변수 지정 및 종료
                album_idx = df[(df['album titles']==album_title) & (df['artists']==artist_for_album)].index[0]
                got_album = True
                break
            except:                               # 실패할 경우 에러 창과 함께 반복문으로 복귀
                print('ERROR : 아티스트가 존재하지 않습니다.')
    if got_album == True:       # 찾았으면 종료
        break

cosine_sim = linear_kernel(Tfidf_matrix[album_idx], Tfidf_matrix)       # 코사인 유사도
recommendation = getRecommendation(cosine_sim)      # 추천 함수 실행
print(recommendation.iloc[1:11, 0:2])      # 0번 컬럼(앨범명)과 1번 컬럼(아티스트명)만 출력

#####################################

### tfidf를 활용한 아티스트 검색 시 비슷한 가수 찾기 ###
df = pd.read_csv('./datasets/cleaned_reviews_tfidf.csv', index_col=0)

Tfidf_matrix = mmread('./models/tfidf_album_review.mtx').tocsr()
with open('./models/tfidf.pickle', 'rb') as f:
    Tfidf = pickle.load(f)

while True:
    artist = str(input('찾으시는 아티스트명을 입력해주세요.'))
    artist_album_count = df[df['artists']==artist]['album titles'].count()

    if artist_album_count == 0:
        print('ERROR : 일치하는 아티스트가 존재하지 않습니다.')
        continue

    else:
        total_cosine_sim = []       # 각 앨범마다 코사인 유사도를 합친 값 미리 지정
        for i in range(artist_album_count):
            album_idx = df[df['artists'] == artist].index[i]
            cosine_sim = linear_kernel(Tfidf_matrix[album_idx], Tfidf_matrix)
            if total_cosine_sim == []:      # 첫 번째는
                total_cosine_sim = cosine_sim   # 0번 인덱스 값 대입
            else:       # 그 이후는
                total_cosine_sim = total_cosine_sim + cosine_sim    # 합치기
        break

recommendation = getRecommendation(total_cosine_sim)

recommendation = recommendation[recommendation.artists != artist]       # 해당 아티스트의 앨범 제거

print(recommendation.iloc[1:11, 0:2])


#####################################

### word2vec을 활용한 키워드 검색 시 관련 앨범 찾기 ###
embedding_model = Word2Vec.load('./models/VS_50_W_2_MC_5_E_50_SG_1.model')

while True:
    key_word = str(input('키워드를 입력해주세요.'))

    try:
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
        print(recommendation.iloc[0:10, 0:2])
        break

    except:
        print('ERROR : 일치하는 키워드가 존재하지 않습니다.')