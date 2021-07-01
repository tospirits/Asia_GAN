import pandas as pd

df = pd.read_csv('./crawling/movie_review_2017_2021.csv', index_col=0)
df.dropna(inplace=True)

one_sentences = []
for title in df['titles'].unique():
    temp = df[df['titles']==title]['cleaned_reviews']
    one_sentence = ' '.join(temp)       # 여러 리뷰 한 문장으로 이어붙이기
    one_sentences.append(one_sentence)      # 영화별 리뷰 리스트에 넣기
df_one_sentences = pd.DataFrame({'titles':df['titles'].unique(), 'reviews':one_sentences})
print(df_one_sentences.head())
print(df_one_sentences.info())
df_one_sentences.to_csv('./crawling/movie_review_one_2017_2021.csv', encoding='utf-8-sig')