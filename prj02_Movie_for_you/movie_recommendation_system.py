import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from scipy.io import mmwrite, mmread
import pickle
from gensim.models import Word2Vec

df_review_one_sentence = pd.read_csv('./crawling/one_sentence_review_2017_2021.csv', index_col=0)       # 리뷰 읽어 df 생성

Tfidf_matrix = mmread('./models/tfidf_movie_review.mtx').tocsr()        # matrix 불러오기
with open('./models/tfidf.pickle', 'rb') as f:      # tfidf 불러오기
    Tfidf = pickle.load(f)

def getRecommendation(cosine_sim):      # 코사인 유사도롤 활용하여 유사한 영화 추천하는 함수
    simScore = list(enumerate(cosine_sim[-1]))      # 각 코사인 유사도 값에 인덱스 붙임
    simScore = sorted(simScore, key=lambda x:x[1], reverse=True)        # simScore(코사인 유사도, x[1])가 큰 것부터 정렬. reverse=True 내림차순 정렬.
    simScore = simScore[1:11]       # 유사한 영화 10개 리스트. 0번 값은 자기 자신이므로 배제.
    movieidx = [i[0] for i in simScore]     # 인덱스(i[0]) 뽑아서 리스트 생성
    recMovieList = df_review_one_sentence.iloc[movieidx]        # df에서 해당 영화 리스트 추출
    return recMovieList

movie_idx = df_review_one_sentence[df_review_one_sentence['titles']=='기생충 (PARASITE)'].index[0]      # 영화 제목으로 인덱스 값 찾기
# movie_idx = 127
# print(df_review_one_sentence.iloc[movie_idx, 0])

cosine_sim = linear_kernel(Tfidf_matrix[movie_idx], Tfidf_matrix)      # linear_kernel은 각 Tfidf 값을 다차원 공간에 벡터(방향과 거리를 가짐)로 배치한 뒤, 코사인 유사도를 구해줌. cosine = 삼각형의 밑변 / 윗변
                                                                       # 비슷한 영화는 유사한 위치에 배치됨. 유사할수록 각이 줄어드므로 코사인 값이 1에 가까워짐. -1에 가까울수록 반대, 0에 가까울수록 무관
recommendation = getRecommendation(cosine_sim)
# print(recommendation)
print(recommendation.iloc[:, 0])

embedding_model = Word2Vec.load('./models/word2VecModel_2017_2021.model')
key_word = '토르'

sim_word = embedding_model.wv.most_similar(key_word, topn=10)
labels = []
sentence = []
for label, _ in sim_word:
    labels.append(label)
print(labels)
for i, word in enumerate(labels):
    sentence += [word] * (9-i)
sentence = ' '.join(sentence)
#sentence = [key_word] * 10      # tf에서 높은 값을 가지도록 리스트 복사
print(sentence)

sentence_vec = Tfidf.transform([sentence])
cosine_sim = linear_kernel(sentence_vec, Tfidf_matrix)
recommendation = getRecommendation(cosine_sim)
print(recommendation)