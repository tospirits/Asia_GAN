import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.io import mmwrite
import pickle
import os

df = pd.read_csv('./datasets/cleaned_reviews_tfidf.csv', index_col=0)
print(df.info())


Tfidf = TfidfVectorizer(sublinear_tf=True)
Tfidf_matrix = Tfidf.fit_transform(df['cleaned_sentences'])

path = './models/'
picklename = 'tfidf.pickle'
matrixname = 'tfidf_album_review.mtx'
os.makedirs(path, exist_ok=True)
with open(path+picklename, 'wb') as f:      # Tfidf 저장
    pickle.dump(Tfidf, f)

mmwrite(path+matrixname, Tfidf_matrix)      # Tfidf matrix 저장