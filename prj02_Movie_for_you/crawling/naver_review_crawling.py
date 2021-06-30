# crawling 작업

# crawling은 각자 진행하고 빨리 완성되는 코드로 연도를 나눠서 진행하겠습니다.
# 일단 2019년 개봉작만 크롤링 해주시고 나머지는 연도별로 크롤링해서 합칠게요.
# 데이터는 데이터프레임으로 작업해주시고 저장 형식은 csv로 하겠습니다.
# 컬럼 명은 ['years', 'titles', 'reviews']로 통일해 주세요.
# 파일명은 reviews_0000.csv 로 해주세요. 0000은 연도입니다.
# 크롤링 파일은 https://url.kr/74bjw5 에 올려주세요.


from selenium import webdriver
import pandas as pd
from selenium.common.exceptions import NoSuchElementException  #그런 element없다. xpath가 일정한 규칙성있는 중 중간중간 빠진거 있을때 나오는 에러. 이런 에러에서 프로그램종료하지 말고 어떻게 하라고 할때 사용
import time

options = webdriver.ChromeOptions()
# options.add_argument('headless')  #브라우저 열리는거 안보이게
options.add_argument('disable_gpu')
options.add_argument('lang=ko_KR')

driver = webdriver.Chrome('chromedriver', options=options)
years = []
titles = []
reviews = []

# url = 'https://movie.naver.com/movie/sdb/browsing/bmovie.nhn?open=2019&page=43'
# driver.get(url)
# y = driver.find_elements_by_xpath('//*[@id="old_content"]/ul/li')   #elements로 해야 해당 xpath의 element를 다 가져옴
# # print(len(y))
# driver.find_element_by_xpath('//*[@id="old_content"]/ul/li[1}]/a').click()
# time.sleep(0.5)
# driver.find_element_by_xpath('//*[@id="movieEndTabMenu"]/li[6]/a/em').click()

#2019년만
try:
    for i in range(1,44):   #2019 개봉영화 리스트 44  #연도별 영화 리스트 페이지수 확인하세요
        url = 'https://movie.naver.com/movie/sdb/browsing/bmovie.nhn?open=2019&page={}'.format(i)
        #영화제목 눌러서 들어가기
        # y = driver.find_elements_by_xpath('//*[@id="old_content"]/ul/li')  #영화개수
        for j in range(1,21):   #영화 제목 리스트 페이지당 20개  21
            try:
                driver.get(url)
                time.sleep(1)
                movie_title_xpath = '//*[@id="old_content"]/ul/li[{}]/a'.format(j)
                title = driver.find_element_by_xpath(movie_title_xpath).text  #영화제목 가져오기
                print(title)

                driver.find_element_by_xpath(movie_title_xpath).click()   #영화제목 클릭
                #/li[%d]/a'%j)  이렇게 문자열표현도 가능
                time.sleep(1)
                # 리뷰버튼 누르기   #리뷰 버튼 없을때를 대비한 try except문
                try:
                    btn_review_xpath = '//*[@id="movieEndTabMenu"]/li[6]/a/em'
                    driver.find_element_by_xpath(btn_review_xpath).click()
                    time.sleep(1)
                    # 들어가있는 영화의 리뷰 총개수
                    review_len_xpath = '//*[@id="reviewTab"]/div/div/div[2]/span/em'
                    review_len = driver.find_element_by_xpath(review_len_xpath).text

                    review_len = int(review_len)  #str을 int로 바꾸기
                    try:
                        for k in range(1, ((review_len-1) // 10)+2):  #리뷰 개수로 리뷰 리스트 페이지 개수 만큼 for문
                            review_page_xpath = '//*[@id="pagerTagAnchor{}"]'.format(k)
                            driver.find_element_by_xpath(review_page_xpath).click()
                            time.sleep(1)
                            for l in range(1,11):  #리뷰가 한페이지 당 10개씩
                                review_title_xpath = '//*[@id="reviewTab"]/div/div/ul/li[{}]'.format(l)
                                try:  #리뷰제목 클릭
                                    driver.find_element_by_xpath(review_title_xpath).click()
                                    time.sleep(1)
                                    try:   #리뷰 크롤링
                                        review_xpath = '//*[@id="content"]/div[1]/div[4]/div[1]/div[4]'
                                        review =  driver.find_element_by_xpath(review_xpath).text
                                        titles.append(title)
                                        reviews.append(review)
                                        driver.back()
                                        time.sleep(1)
                                    except:
                                        driver.back()
                                        time.sleep(1)
                                        print('review crawling error')
                                except:
                                    #.click()하다가 에러난건 못들어간거니까 driver.back하면 안됨
                                    time.sleep(1)
                                    print('review title click error')
                    except:
                        print('review page btn click error')
                except:
                    print('review btn click error')

            except NoSuchElementException:
                driver.get(url)  #에러나면 처음으로 돌아감
                time.sleep(1)
                print('NoSuchElementException')
        print(len(titles))
        df_review = pd.DataFrame({'titles':titles, 'reviews':reviews})
        df_review['years'] = 2019
        print(df_review.head(20))
        df_review.to_csv('./reviews_2019_{}_page.csv'.format(i), encoding='utf-8-sig') #### 세번째 업뎃


except:
    print('except1')
finally:   #try에서 잘 끝나든 except로 끝나든 무조건 하는거
    driver.close()

#하다가 지움
# #리뷰리스트
# x = driver.find_elements_by_xpath('//*[@id="reviewTab"]/div/div/ul/li')  #리뷰개수
# if x:   #숫자는 0일때 false.  리뷰가 0개일때는 if문 안들어가도록
#     for k in range(1, 3):   #len(x)+1
#         try:   #리뷰 제목 클릭
#             driver.find_element_by_xpath(
#                 '//*[@id="reviewTab"]/div/div/ul/li[{}]'.format(k)).click()  #리뷰제목 클릭
#             time.sleep(0.5)
#             #영화제목 크롤링
#             name = driver.find_element_by_xpath('//*[@id="content"]/div[1]/div[2]/div[1]/h3/a').text  #.text로 해당 xpath에서 문자만 가져오기
#             #리뷰내용 크롤링
#             reviewcontext = driver.find_element_by_xpath('//*[@id="content"]/div[1]/div[4]/div[1]/div[4]').text
#             names.append(name)
#             reviewcontexts.append(reviewcontext)
#             #뒤로-리뷰나열된 페이지- 돌아가기
#             driver.back()
#         except NoSuchElementException:
#             print('NoSuchElementException')
=======
