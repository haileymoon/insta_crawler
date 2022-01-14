from urllib.parse import quote_plus

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd
import time
import configparser

config = configparser.ConfigParser()
config.read("config.ini", encoding='UTF8')

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)

def login():
    flag = False
    try:
        id_space = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.NAME, 'username')))
        id_space.send_keys(config["LOGIN_KEY"]["instagram_id"])
        time.sleep(2)

        pwd_space = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.NAME, 'password')))
        pwd_space.send_keys(config["LOGIN_KEY"]["instagram_pwd"])
        time.sleep(2)

        login_button = driver.find_element(By.XPATH,config['XPATH']['login_button'])
        login_button.click()

        time.sleep(2)

        save_later_button = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH, config['XPATH']['save_later'])))
        save_later_button.click()
        flag = True
        return flag
    except:
        # 로그인이 안되거나, 인터넷이 안될때 에러 처리 - 에러 코드가 뭐지
        print("login error")
        return flag

def crawl():
    flag = False
    try:
        first_post = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR ,config['CSS_SELECTOR']['first_post'])))
        first_post.click() #div사이에 공백있으면 .으로 replace -- 이유는 유튭 참고
        # 이 first_post가 없을때의 에러 처리 (검색어입력이 잘못되었을때)
        data = []
        crawl_post_number = 5
        for i in range(crawl_post_number):
            time.sleep(3)
            hashtag_array = driver.find_elements(By.CSS_SELECTOR , config['CSS_SELECTOR']['hashtags'])
            for hashtag in hashtag_array:
                data.append(hashtag.text.replace('#',''))

            #다음 포스트로 넘어가기
            next_button = WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR , ['hashtags']['next_post_button'])))
            next_button.click()
            flag = True
        return data
    except:
        print("crawl error")
        return flag

def convertToCsv(data):
    flag = False
    try:
        data_frame = pd.DataFrame(data)
        data_frame.to_csv('crawled_data.csv', index=False, encoding='utf-8-sig')
        flag = True
        return flag
    except:
        print("csv convert error")
        return flag

# beautiful soup을 활용해서 데이터를 긁어올 수 있지만
# 지금같은 경우는 다른 잡다한 정보는 필요없고 오로지 해시태그 정보만 필요해서 Bs4를 
# 활용하지 않을 것.

def main():

    keyword = input('검색할 키워드를 입력하세요')
    search_url = config["URL"]["baseUrl"] + quote_plus(keyword)
    login_url = config["URL"]["loginUrl"]
    flag = False

    driver.get(login_url)
    if login():
        driver.get(search_url)
    else: 
        return flag
    data = crawl()
    if data != False:
        convertToCsv(data)
    else:
        return flag

    return True

main()
driver.quit()

# while(True):
#     pass

