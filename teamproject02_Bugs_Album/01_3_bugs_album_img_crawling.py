import pandas as pd
from glob import glob
import urllib.request
from bs4 import BeautifulSoup

df = pd.read_csv('./crawling/bugs_album_page_001_160_210707_120316.csv', index_col=0)

target_list = list(df['album links'])       # 목표치
print(len(target_list))

saved_list = []
saved_imgs = glob('./images/*.jpg')


for i in range(len(saved_imgs)):
    saved_img = saved_imgs[i].split('\\')[1]
    saved_img = int(saved_img.split('.')[0])
    saved_list.append(saved_img)
print(len(saved_list))

target_set = set(target_list)
saved_set = set(saved_list)

s_numbers_set = target_set - saved_set      # 차집합
s_numbers = list(s_numbers_set)

print(len(s_numbers))


path = './images/'

count = 0
for s_number in s_numbers:
    url = f'https://music.bugs.co.kr/album/{s_number}'
    print(s_number, 'img searching')
    try:
        req = urllib.request.Request(url)
        res = urllib.request.urlopen(url).read()

        soup = BeautifulSoup(res, 'html.parser')
        soup = soup.find(class_='big')
        imgUrl = soup.find("img")["src"]

        urllib.request.urlretrieve(imgUrl, path + f'{s_number}.jpg')
        count += 1
    except Exception as e:
        print(e)
    print(count, '/', len(s_numbers))