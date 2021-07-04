# crawling 작업

# https://music.bugs.co.kr/recomreview
# 타겟 데이터 수 : 4,741개 (2021년 7월 2일 기준)
# 크롤링할 데이터 : 앨범명, 가수, 리뷰 제목, 리뷰 내용
# 크롤링 작업 URL : https://music.bugs.co.kr/recomreview?&order=listorder&page={pageNumber}
# 총 페이지 수 : 475 페이지

# 크롤링은 160페이지씩 진행하겠습니다. 이서하 : 1-160 / 구윤정 : 161 - 320 / 홍두기 : 321 - 475
# 10페이지마다 'bugs_album_page_1_10.csv' 형태로 개별 중간 저장, 160페이지(또는 마지막 페이지)에 도달하면 'bugs_album_page_{startPage}_{finishPage}.csv'로 최종 저장합니다.
# 저장 형식은 csv이며, 인코딩은 utf-8-sig입니다.
# 컬럼명은 ['album titles', 'artists', 'review titles', 'reviews']로 통일해 주세요.
# 크롤링 파일은 https://url.kr/8its76 에 올려주세요.

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import os
import time
import datetime


def pageNumber():       # 시작 페이지, 종료 페이지 지정 함수
    global startPage, finishPage        # 전역변수 선언
    startPage = int(input('시작 페이지를 입력해주세요.'))
    finishPage = int(input('종료 페이지를 입력해주세요.'))

def resetData():        # 필요 변수 생성 및 초기화 함수
    global albumTitles, artists, reviewTitles, reviews, multiArtists        # 전역변수 선언
    albumTitles = []        # 앨범명
    artists = []            # 아티스트명
    reviewTitles = []       # 리뷰 제목
    reviews = []            # 리뷰 내용
    multiArtists = []       # 아티스트 공동 작업 시 artists로 넘기기 전 임시로 저장하는 리스트

def errorCheckData():       # 에러 관련 필요 변수 생성 및 초기화 함수
    global errorPages, errorContents        # 전역변수 선언
    errorPages = []                         # 에러 페이지 번호 리스트
    errorContents = []                      # 에러 콘텐츠 번호 리스트

def saveDirectory(page):        # csv파일 저장 경로 지정 함수
    path = './crawling/'
    os.makedirs(path, exist_ok=True)        # path 경로가 없으면 생성, 있으면 그대로 진행
    now = datetime.datetime.now()           # 현재 시간
    now = now.strftime('%y%m%d_%H%M%S')     # 표현방식 YYMMDD_HHMMSS
    saveFileName = 'bugs_album_page_{0:>03d}_{1:>03d}_{2}.csv'.format(startPage, page, now)     # 파일명 예시 : bugs_album_page_001_100_210702_235055.csv
    return path+saveFileName

def errorLogDirectory(page):        # 에러 로그파일 저장 경로 지정 함수
    path = './crawling/log/'
    os.makedirs(path, exist_ok=True)
    now = datetime.datetime.now()
    now = now.strftime('%y%m%d_%H%M%S')
    logFileName = 'bugs_album_errorlog_page_{0:>03d}_{1:>03d}_{2}.txt'.format(startPage, page, now)  # 파일명 예시 : bugs_album_errorlog_page_001_100_210702_235055.txt
    return path+logFileName

### webdriver 옵션 지정 ###
options = webdriver.ChromeOptions()
# options.add_argument('headless')
options.add_argument('disable_gpu')
options.add_argument('lang=ko_KR')

driver = webdriver.Chrome('chromedriver', options=options)
driver.implicitly_wait(1)       # 로드 대기시간 1초 (이전에 로드 완료되면 기다리지 않고 진행)

pageNumber()        # 페이지 지정 함수 호출
resetData()     # 필요 변수 생성 및 초기화 함수 호출
errorCheckData()        # 에러 관련 필요 변수 생성 및 초기화 함수 호출

try:
    for i in range(startPage, finishPage+1):        # 입력받은 페이지 수만큼 반복
        url = f'https://music.bugs.co.kr/recomreview?&order=listorder&page={i}'
        try:        # 접속 1회 시도
            driver.get(url)
        except Exception as e:
            print('\n access URL error \n', e)
            try:        # 접속 2회 시도
                time.sleep(5)
                driver.get(url)
            except Exception as e:
                print('\n access URL error \n', e)
                try:        # 접속 3회 시도
                    time.sleep(5)
                    driver.get(url)
                except Exception as e:
                    print('\n access URL error \n', e)
                    print('\n continue next page \n')
                    errorPages.append(i)     # 에러 페이지 리스트에 넣어 추후 작업 가능하도록 저장
                    continue        # 이하 코드 실행하지 않고 다음 페이지로 넘어가기

        for j in range(1, 11):      # 한 페이지당 콘텐츠 수 10개씩 반복
            try:        # 앨범명
                albumTitle_xpath = f'//*[@id="container"]/section/div/ul/li[{j}]/div/figure/figcaption/a'
                albumTitle = driver.find_element_by_xpath(albumTitle_xpath).text
            except Exception as e:
                print('\n album title crawling error \n', e)
                errorContents.append(f'{i} page, contents number: {j} album title crawling error')      # 에러 콘텐츠 리스트에 페이지, 번호, 타입 넣어 추후 작업 가능하도록 저장
                continue        # 이하 코드 실행하지 않고 다음 콘텐츠로 넘어가기

            try:        # 아티스트명
                artist_xpath = f'//*[@id="container"]/section/div/ul/li[{j}]/div/figure/figcaption/p[1]/a'      # 아티스트 1명인 경우
                artist = driver.find_element_by_xpath(artist_xpath).text
            except Exception as e:
                print('\n artist crawling error \n', e)
                print('finding multiple artists')
                try:        # 아티스트 2명 이상인 경우
                    moreArtists = f'//*[@id="container"]/section/div/ul/li[{j}]/div/figure/figcaption/p[1]/span/a[2]'     # 아티스트 더보기 화살표 버튼
                    driver.find_element_by_xpath(moreArtists).click()       # 버튼 클릭
                    multiArtists_xpath = '//*[@id="commonLayerMenu"]/div[2]/div/div/ul/li'
                    multiArtists = driver.find_elements_by_xpath(multiArtists_xpath)        # find_elements를 통해 리스트로 받아서 문자열로 바꾸기 전까지 저장
                    print('success finding artists')
                except Exception as e:
                    try:        # 아티스트 VariousArtists인 경우
                        variousArtists = f'//*[@id="container"]/section/div/ul/li[{j}]/div/figure/figcaption/p[1]/span'     # 기존 xpath 맨 앞의 '#' 제거하니 정상 작동
                        artist = driver.find_element_by_xpath(variousArtists).text
                        print('success finding artists')
                    except Exception as e:
                        print('artist crawling error \n', e)
                        errorContents.append(f'{i} page, contents number: {j} artist crawling error')
                        continue

            try:        # 리뷰 제목
                reviewTitle_xpath = f'//*[@id="container"]/section/div/ul/li[{j}]/div/aside/h1'
                reviewTitle = driver.find_element_by_xpath(reviewTitle_xpath).text
            except Exception as e:
                print('\n review title crawling error \n', e)
                errorContents.append(f'{i} page, contents number: {j} review title crawling error')
                continue

            try:        # 리뷰 내용
                review_xpath = f'//*[@id="container"]/section/div/ul/li[{j}]/div/aside/p[1]/span'
                review = driver.find_element_by_xpath(review_xpath).text
            except Exception as e:
                print('\n review crawling error \n', e)
                errorContents.append(f'{i} page, contents number: {j} review crawling error')
                continue

            try:        # 전체 리스트에 데이터 추가
                if multiArtists != []:        # 참여 가수가 여러 명이면
                    artist = multiArtists[0].text        # 첫 번째 가수 먼저 입력
                    for k, m in enumerate(multiArtists):
                        if k == 0:      # 첫 번째 가수 제외하고 두 번째 가수부터,
                            continue
                        artist = artist + ' & ' + m.text     # '가수 & 가수 & 가수' 형식으로 지정
                    multiArtists.clear()        # 사용한 리스트 초기화

                albumTitles.append(albumTitle)
                artists.append(artist)
                reviewTitles.append(reviewTitle)
                reviews.append(review)

                print('.', end='')      # 진행과정 표시
            except Exception as e:
                print('\n list append error \n', e)
                errorContents.append(f'{i} page, contents number: {j} list append error')
        print(f'\n {i} 페이지 수집 완료 \n')

        ### 체크포인트 저장 ###
        if (i % 10) == 0:       # 10, 20, ..., 470 페이지에 도달할 때마다 csv 파일 저장
            df_temp = pd.DataFrame({'album titles': albumTitles, 'artists': artists, 'review titles': reviewTitles,
                               'reviews': reviews})     # 데이터프레임 4개 컬럼에 각 데이터 입력
            df_temp.to_csv(saveDirectory(i), encoding='utf-8-sig')      # saveDirectory 함수 호출하며 경로 지정 및 엑셀과 파이썬 양쪽에서 글자 깨지지 않도록 utf-8-sig 인코딩
            print(f'checkpoint data saved in {saveDirectory(i)}')       # 체크포인트 저장 알림 메시지

            ### 에러 로그 저장 ###
            if errorPages!=[] or errorContents!=[]:        # 크롤링 과정 중 에러가 있으면
                with open(errorLogDirectory(i), 'w') as f:      # 에러 로그 작성
                    f.write('==========ERROR PAGES==========')
                    for errorpage in errorPages:
                        print(errorpage)
                        f.write(f'{errorpage}\n')
                    f.write('\n==========ERROR CONTENTS==========\n')
                    for errorcontent in errorContents:
                        f.write(f'{errorcontent}\n')
                    f.close()
                print(f'checkpoint log data saved in {errorLogDirectory(i)}')       # 체크포인트 에러 로그 저장 알림 메시지

    ### 최종 저장 ###
    df = pd.DataFrame({'album titles':albumTitles, 'artists':artists, 'review titles':reviewTitles, 'reviews':reviews})
    df.to_csv(saveDirectory(finishPage), encoding='utf-8-sig')
    print(f'All data saved in {saveDirectory(finishPage)}')

    ## 최종 에러 로그 저장 ###
    with open(errorLogDirectory(finishPage), 'w') as f:
        if errorPages != [] or errorContents != []:
            f.write('==========ERROR PAGES==========\n')
            for errorpage in errorPages:
                f.write(f'{errorpage}\n')
            f.write('\n==========ERROR CONTENTS==========\n')
            for errorcontent in errorContents:
                f.write(f'{errorcontent}\n')
            f.close()
        else:
            f.write('Congratulations! NO ERROR IN THIS TASK!!\n Special Thanks to 구윤정, 이서하, 그리고 홍두기')
            f.close()
    print(f'Log data saved in {errorLogDirectory(finishPage)}')

    print('finished')

except Exception as e:      # 에러 세부 내용 출력하도록
    print(e)
finally:
    driver.close()          # 크롬드라이버 종료