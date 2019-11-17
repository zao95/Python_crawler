# 메모
# __name__ == '__main__' 기능들을 전부 다 넣어버리기
# 크롤러 내용 논문에 넣기
# Flask 모듈화? 파일나누기? 필요 - 그러면 파일 실행할때 매개변수처럼 넣는 방법 필요함
# 리다이렉션의 이유?
# 웹서비스용 Flask 사용법
# 멀티프로세싱 브라우저 여러개 뜨는 문제
# 메일 양식만들기
# 만약 나중에 시간 된다면 이미지 분류 프로
# MD5 해시
# 파일 저장 후 절대경로 리스트 보내기
# 멀티프로세스 내에서 통신 queue, pipe 이용 # map에서 process 형태로 바꾸는거 검토

# 패키지 옮기기
# pip install -r [pip freeze > (파일이름)]

from pathlib import Path
from selenium import webdriver
import time
import os
from module import CrawlerN
from module import DownloaderN
from module import CrawlerG
from module import DownloaderG
from multiprocessing import Pool
from multiprocessing import Queue

# ========== Setting part ==========
# Choose the search word
searchWord = "이순신 장군 동상"
# Justify download max image count - The actual number of downloaded files might be small due to an error.
downloadCnt = 100
# Select mode
testMode = True  # if it is true visible the browser
fastTestMode = True  # if it is true the number of search images is up to 100.
naverCrawling = True  # if it is true crawl naver
googleCrawling = True  # if it is true crawl google

# ========== Main part ==========
if __name__ == "__main__":

    # ========== Run the chrome driver ==========
    # Path import
    path = Path("./chromedriver")
    # Change to the absolute path
    full_path = path.absolute()
    # Change to string type
    my_path = full_path.as_posix()

    # ========== Create directory ==========
    # If not the img folder
    if not (os.path.isdir("img")):
        # Make the img folder
        os.makedirs(os.path.join("img"))

    # ========== Selenium setting ==========
    if not testMode:
        # Headless options
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument("disable-gpu")
        # Execute chrome browser
        driver = webdriver.Chrome(my_path, chrome_options=options)
    if testMode:
        # Execute chrome browser
        driver = webdriver.Chrome(my_path)

    # ========== Multiprocessing setting ==========
    pool = Pool(processes=6)

    # ========== Naver crawling part ==========
    if naverCrawling:

        # Naver crawling
        htmlN = CrawlerN.crawlingN(driver, searchWord, fastTestMode)
        # Naver image download
        pool.map(DownloaderN.downloadingN, DownloaderN.dataN(htmlN, downloadCnt))

    # ========== Google crawling part ==========
    if googleCrawling:

        # Import html using google crawling
        htmlG = CrawlerG.crawlingG(driver, searchWord, fastTestMode)
        # Google image download with multiprocess
        pool.map_async(DownloaderG.downloadingG, DownloaderG.dataG(htmlG, downloadCnt))
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