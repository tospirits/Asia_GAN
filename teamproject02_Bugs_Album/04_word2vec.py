import os
import pickle
import pandas as pd
from gensim.models import Word2Vec

def visualize_process(current, total):
    if (current % 25 == 0) and (current>1):
        print('▇', end='')
    if current % 1000 == 0:
        print(' {}|{}'.format(current, total))

def makeWord2VecModel(model_save_path, key_save_path, vector_size, window, min_count, workers, epochs, sg):
    csv_path = './datasets/cleaned_reviews_word2vec.csv'
    model_pram = '_'.join(list(map(str, ['VS', vector_size, 'W', window, 'MC', min_count, 'E', epochs, 'SG', sg])))

    print('\n{:@^50}'.format(model_pram))
    review_word = pd.read_csv(csv_path, index_col=0)
    # print('{:-^50}'.format('review_word info'))
    # print(review_word.info())
    cleaned_token_review = list(review_word['cleaned_sentences'])
    # print('{:-^50}\n'.format('len of cleaned_token_review', len(cleaned_token_review)))
    cleaned_tokens = []
    print('{:-^50}'.format('Tokenize'))
    data_len = len(cleaned_token_review)
    for i in range(data_len):
        sentence = cleaned_token_review[i]
        token = sentence.split(' ')  # 띄어쓰기 기준으로 각 단어 토큰화
        cleaned_tokens.append(token)
        visualize_process(i+1, data_len)
    print(' '*((data_len%1000)//25-1), ' {}|{}'.format(data_len, data_len))

    model = Word2Vec(cleaned_tokens,
                     vector_size=vector_size,   # vector_size는 몇차원으로 줄일지 지정,
                     window=window,             # window는 CNN의 kernel_size 개념, 앞뒤로 고려하는 단어의 개수를 나타냄
                     min_count=min_count,       # min_count는 출현 빈도가 20번 이상인 경우만 word track에 추가하라는 의미(즉, 자주 안 나오는 단어는 제외)
                     workers=workers,           # workers는 cpu 스레드 몇개 써서 작업할 건지 지정,
                     epochs=epochs,             #
                     sg=sg)                     # skip_gram 알고리즘 적용

    model_nameNpath = model_save_path+model_pram+'.model'
    model.save(model_nameNpath)
    # print('{:-^50}\n'.format('index_to_key head(10)'), model.wv.index_to_key[:10])
    with open(key_save_path+model_pram+'.pickle', 'wb') as f:
        pickle.dump(model.wv.index_to_key, f, pickle.HIGHEST_PROTOCOL)
    # print('{:-^50}\n{:^50}'.format('len of index', len(model.wv.index_to_key)))

model_save_path = './models/'                       # 모델 저장 경로
os.makedirs(model_save_path, exist_ok=True)         # path 경로가 없으면 생성, 있으면 그대로 진행
key_save_path = './key_index/'                      # key index 저장 경로
os.makedirs(key_save_path, exist_ok=True)           # path 경로가 없으면 생성, 있으면 그대로 진행

vector_sizes = [200, 400, 800]
windows = [4, 8, 16]
min_count = 10
workers = 4
epochs = 100
sg = 1

# 총 3*3 = 9개 모델 생성

for vector_size in vector_sizes:
    for window in windows:
        makeWord2VecModel(model_save_path, key_save_path, vector_size, window, min_count, workers, epochs, sg)
#
# vector_sizes = [50, 100, 200]
# windows = [2, 4]
# min_counts = [5, 10, 20]
# workers = 4
# epochses = list(range(50, 151, 50))         # 50, 100, 150
# sg = 1
#
# # 총 3*2*3*3 = 54개 모델 생성
#
# for vector_size in vector_sizes:
#     for window in windows:
#         for min_count in min_counts:
#             for epochs in epochses:
#                 makeWord2VecModel(model_save_path, key_save_path, vector_size, window, min_count, workers, epochs, sg)