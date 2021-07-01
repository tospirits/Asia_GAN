import pandas as pd

df = pd.read_csv('./crawling/cleaned_review_2020.csv', index_col=0)
df.dropna(inplace=True)

one_sentences = []
for title in df['titles'].unique():
    temp = df[df['titles']==title]['cleaned_sentences']
    one_sentence = ' '.join(temp)       # 여러 리뷰 한 문장으로 이어붙이기
    one_sentences.append(one_sentence)      # 영화별 리뷰 리스트에 넣기
df_one_sentences = pd.DataFrame({'titles':df['titles'].unique(), 'reviews':one_sentences})
print(df_one_sentences.head())
df_one_sentences.to_csv('./crawling/one_sentence_review_2020.csv', encoding='utf-8-sig')