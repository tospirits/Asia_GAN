import os
import datetime
import pandas as pd
from gensim.models import Word2Vec

def saveDirectory(model_pram):              # model 파일 저장 경로 지정 함수
    path = './models/'
    os.makedirs(path, exist_ok=True)        # path 경로가 없으면 생성, 있으면 그대로 진행
    now = datetime.datetime.now()           # 현재 시간
    now = now.strftime('%y%m%d_%H%M%S')     # 표현방식 YYMMDD_HHMMSS
    saveFileName = '{}_{}.model'.format(model_pram, now)
    return path+saveFileName

vector_size = 100
window = 4
min_count = 20
workers = 4
epochs = 100
sg = 1

model_pram = '_'.join(list(map(str, ['VS', vector_size, 'W', window, 'MC', min_count, 'E', epochs, 'SG', sg])))

review_word = pd.read_csv('@@@@@@@@_경로_입력_@@@@@@@@', index_col=0)
print(review_word.info())
cleaned_token_review = list(review_word['cleaned_reviews'])
print(len(cleaned_token_review))
cleaned_tokens = []
count = 0
for sentence in cleaned_token_review:
    token = sentence.split(' ')  # 띄어쓰기 기준으로 각 단어 토큰화
    cleaned_tokens.append(token)
# print(len(cleaned_tokens))
# print(cleaned_token_review[0])
# print(cleaned_tokens[0])
model = Word2Vec(cleaned_tokens,
                 vector_size=vector_size,   # vector_size는 몇차원으로 줄일지 지정,
                 window=window,             # window는 CNN의 kernel_size 개념, 앞뒤로 고려하는 단어의 개수를 나타냄
                 min_count=min_count,       # min_count는 출현 빈도가 20번 이상인 경우만 word track에 추가하라는 의미(즉, 자주 안 나오는 단어는 제외)
                 workers=workers,           # workers는 cpu 스레드 몇개 써서 작업할 건지 지정,
                 epochs=epochs,             #
                 sg=sg)                     # skip_gram 알고리즘 적용

model.save(saveDirectory(model_pram))
print(model.wv.vocab.keys())
print(len(model.wv.vocab.keys()))
