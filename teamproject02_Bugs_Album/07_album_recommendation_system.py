import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from scipy.io import mmread
import pickle
from gensim.models import Word2Vec

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