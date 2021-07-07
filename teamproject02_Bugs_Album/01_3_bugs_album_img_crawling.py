import pandas as pd
from glob import glob
import urllib.request
from bs4 import BeautifulSoup

df = pd.read_csv('./crawling/bugs_album_reviews.csv', index_col=0)
df.drop_duplicates(['album links'], keep='first', ignore_index=True, inplace=True)      # 중복 앨범 제거

target_list = list(df['album links'])       # 목표 앨범 고유번호 리스트


### BS4를 이용한 크롤링 도중 이미지 로드하는 과정에서 멈추는 경우가 발생하므로 필요한 이미지만 불러오도록 개선 완료###
### 이미지 서칭 과정에서 멈출 경우 정지 후 재시작하면 이어서 작업함 ###

saved_list = []
saved_imgs = glob('./images/*.jpg')         # 저장된 앨범 경로 리스트


for i in range(len(saved_imgs)):
    saved_img = saved_imgs[i].split('\\')[1]        # 경로에서 고유번호만 불러오기
    saved_img = int(saved_img.split('.')[0])        # 고유번호 추출하며 int 값으로 변환
    saved_list.append(saved_img)                    # 리스트 추가
print(len(saved_list))

target_set = set(target_list)                       # 집합을 이용하기 위해 세트로 변환
saved_set = set(saved_list)

s_numbers_set = target_set - saved_set      # 차집합 구하기
s_numbers = list(s_numbers_set)             # 리스트로 다시 변환

print(len(s_numbers))


path = './images/'      # 저장경로 지정

count = 0       # 진행상황 표시용 카운트
for s_number in s_numbers:
    url = f'https://music.bugs.co.kr/album/{s_number}'
    print(s_number, 'img searching')
    try:
        req = urllib.request.Request(url)
        res = urllib.request.urlopen(url).read()

        soup = BeautifulSoup(res, 'html.parser')            # html parser
        soup = soup.find(class_='big')                      # 이미지를 보유한 클래스 찾아가기
        imgUrl = soup.find("img")["src"]                    # 이미지 url 찾기

        urllib.request.urlretrieve(imgUrl, path + f'{s_number}.jpg')        # 저장
        count += 1
    except Exception as e:
        print(e)
    print(count, '/', len(s_numbers))