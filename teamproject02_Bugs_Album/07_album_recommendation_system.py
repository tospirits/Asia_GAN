import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from scipy.io import mmread
import pickle
from gensim.models import Word2Vec

### tfidf를 활용한 앨범 검색 시 유사 앨범 찾기 ###
df = pd.read_csv('./crawling/album_reviews.csv', index_col=0)

Tfidf_matrix = mmread('./models/tfidf_album_review.mtx').tocsr()
with open('./models/tfidf.pickle', 'rb') as f:
    Tfidf = pickle.load(f)

def getRecommendation(cosine_sim):
    simScore = list(enumerate(cosine_sim[0]))
    simScore = sorted(simScore, key=lambda x:x[1], reverse=True)
    simScore = simScore[1:11]
    albumidx = [i[0] for i in simScore]
    recAlbumList = df.iloc[albumidx]
    return recAlbumList

album_idx = df[df['album titles']=='Red Diary Page.1'].index[0]

cosine_sim = linear_kernel(Tfidf_matrix[album_idx], Tfidf_matrix)

recommendation = getRecommendation(cosine_sim)
print(recommendation.iloc[:, 0])



### word2vec을 활용한 키워드 검색 시 관련 앨범 찾기 ###
embedding_model = Word2Vec.load('./models/albumWord2VecModel.model')
key_word = '클래식'

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

sentence_vec = Tfidf.transform([sentence])
cosine_sim = linear_kernel(sentence_vec, Tfidf_matrix)
recommendation = getRecommendation(cosine_sim)
print(recommendation)