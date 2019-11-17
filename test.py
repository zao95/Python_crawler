from pathlib import Path
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import os
from module import CrawlerN
from module import DownloaderN
from module import CrawlerG
from module import DownloaderG

# ========== Setting part ==========
# Choose the search word
searchWords = ["재활", "4차산업", "재활치료", "재활운동", "재활의학과"]
relativeWord = []
It_is_Error = 0

# ========== Main part ==========
if __name__ == "__main__":

    # ========== Run the chrome driver ==========
    # Path import
    path = Path("./chromedriver")
    # Change to the absolute path
    full_path = path.absolute()
    # Change to string type
    my_path = full_path.as_posix()

    # ========== Selenium setting ==========
    # Execute chrome browser
    driver = webdriver.Chrome(my_path)
    for j in range(0, 3):
        if j == 0:
            print("1) Naver 검색어-", end="")
        elif j == 1:
            print("2) Google 검색어-", end="")
        elif j == 2:
            print("3) Daum 검색어-", end="")
        for searchWord in searchWords:
            It_is_Error = 0
            if j == 0:
                try:
                    # ========== web crawling execute section ==========
                    # open naver website
                    driver.get('https://www.naver.com')
                    # checking the sure site is open
                    assert "NAVER" in driver.title
                    # save search section as elem
                    elem = driver.find_element_by_name("query")
                    # clear search section
                    elem.clear()
                    # typing searchWord at search section
                    elem.send_keys(searchWord)
                    # submit them
                    elem.submit()
                    # html parsing
                    html = driver.page_source
                    soup = BeautifulSoup(html, 'html.parser')

                    # ========== image download by beautifulSoup execute section ==========
                    target1 = soup.find("ul", {'class': "_related_keyword_ul"})
                    target2 = target1.find_all("li")
                    count = 0
                    print(searchWord, end="(")
                    for i in target2:
                        count += 1
                        if count == len(target2):
                            print(i.text.strip(), end=")")
                        else :
                            print(i.text.strip(), end=", ")
                except:
                    print("", end="")
                    It_is_Error = 1

            elif j == 1:
                try:
                    # ========== web crawling execute section ==========
                    # open naver website
                    driver.get('https://www.google.com/')
                    # checking the sure site is open
                    assert "Google" in driver.title
                    # save search section as elem
                    elem = driver.find_element_by_name("q")
                    # clear search section
                    elem.clear()
                    # typing searchWord at search section
                    elem.send_keys(searchWord)
                    # submit them
                    elem.submit()
                    # html parsing
                    html = driver.page_source
                    soup = BeautifulSoup(html, 'html.parser')

                    # ========== image download by beautifulSoup execute section ==========
                    target1 = soup.find("div", {'class': "card-section"})
                    target2 = target1.find_all("p")
                    count = 0
                    print(searchWord, end="(")
                    for i in target2:
                        count += 1
                        if count == len(target2):
                            print(i.text.strip(), end=")")
                        else :
                            print(i.text.strip(), end=", ")
                except:
                    print("", end="")
                    It_is_Error = 1

            elif j == 2:
                try:
                    # ========== web crawling execute section ==========
                    # open naver website
                    driver.get('https://www.daum.net/')
                    # checking the sure site is open
                    assert "Daum" in driver.title
                    # save search section as elem
                    elem = driver.find_element_by_id("q")
                    # clear search section
                    elem.clear()
                    # typing searchWord at search section
                    elem.send_keys(searchWord)
                    # submit them
                    elem.submit()
                    # html parsing
                    html = driver.page_source
                    soup = BeautifulSoup(html, 'html.parser')

                    # ========== image download by beautifulSoup execute section ==========
                    target1 = soup.find("div", {'id': "netizen_lists_top"})
                    target2 = target1.find_all("span")
                    count = 0
                    print(searchWord, end="(")
                    for i in target2:
                        if i.text.strip() == "검색어":
                            continue
                        count += 1
                        if count == len(target2):
                            print(i.text.strip(), end=")")
                        else :
                            print(i.text.strip(), end=", ")
                except:
                    print("", end="")
                    It_is_Error = 1
            if not searchWord == searchWords[len(searchWords)-1]:
                if It_is_Error == 0:
                    print("", end=", ")
        print("")
    # ========== Chrome driver close ==========
    if driver is not None:
        isQuited = False
        while not isQuited:
            try:
                time.sleep(1)
                driver.quit()
                print("크롤러가 정상적으로 종료되었습니다.")
                isQuited = True
            except:
                print("이미지 다운로드가 끝나지 않아 종료 대기중입니다.")