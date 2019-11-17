# 메모
# __name__ == '__main__' 기능들을 전부 다 넣어버리기
# 크롤러 내용 논문에 넣기
# Flask 모듈화? 파일나누기? 필요 - 그러면 파일 실행할때 매개변수처럼 넣는 방법 필요함
# 리다이렉션의 이유?
# 웹서비스용 Flask 사용법
# 멀티프로세싱 브라우저 여러개 뜨는 문제
# 메일 양식만들기
# 만약 나중에 시간 된다면 이미지 분류 프로

# 패키지 옮기기
# pip install -r [pip freeze > (파일이름)]

# Python TQDM
from pathlib import Path
from selenium import webdriver
from bs4 import BeautifulSoup
from multiprocessing import Pool
# from flask import Flask, redirect, url_for, request
import time
import urllib.request
import os

# ========== Flask setting ==========
# app = Flask(__name__)
#
#
# @app.route('/crawling', methods=['POST', 'GET'])
# def login():
#     if request.method == 'POST':
#         user = request.form['myName']
#         return redirect(url_for('success', name=user))
#     else:
#         searchWord = request.args.get('searchWord')
#         email = request.args.get('email')
#         return redirect(url_for('success', name=user))
#
#
# if __name__ == "__main__":
#     app.run(host="127.0.0.1", port="8080")

if __name__ == '__main__':
    # ========== important setting ==========
    # choose the search word
    searchWord = "Paris"
    # justify download image count
    downloadCnt = 100
    testMode = True
    fastTestMode = True
    naverCrawling = True
    googleCrawling = False


# ========== pathlib setting ==========
# path import
path = Path("source_data/program_files/chromedriver")
# change to the absolute path
full_path = path.absolute()
# change to string type
my_path = full_path.as_posix()

# ========== directory setting ==========
# if not img folder
if not (os.path.isdir("img")):
    # make img folder
    os.makedirs(os.path.join("img"))

# ========== selenium setting ==========
if not testMode:
    # headless options
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    # execute chrome browser
    driver = webdriver.Chrome(my_path, chrome_options=options)
if testMode:
    driver = webdriver.Chrome(my_path)

if naverCrawling:
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
    # go to image section
    driver.find_element_by_class_name("lnb2").click()

    # definite variable
    i = -1
    loadTime = 0
    if not fastTestMode:
        while True:
            imgCnt = driver.page_source.count('class="img_area _item"')
            print("Loaded image count :", imgCnt)
            # if image over 900, break
            if imgCnt > 900:
                print("Image load complete!")
                break
            # if complete image load
            elif imgCnt >= i * 100 + 50:
                i += 1
                # more image loading
                driver.find_element_by_class_name("more_img").click()
                continue
            # if image count less than when fully load image count
            elif imgCnt < i * 100 + 50:
                loadTime += 0.1
                # if load time more than 3 second, break
                if loadTime > 3:
                    break
                else:
                    # wait image loading
                    time.sleep(0.1)

    # checking success to search
    assert "No results found." not in driver.page_source

    # ========== beautifulSoup setting ==========
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')


    # ========== image download by beautifulSoup execute section ==========
    imgTag = soup.find_all("img")
    print(imgTag) # [<img alt="내 프로필 이미지" height="26" id="gnb_profile_img" src="data:image/gif;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs%3D" width="26"/>, <img alt="프로필 이미지" height="80" src="data:image/gif;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs%3D" width="80"/>,
    print(imgTag[0]) # <img alt="내 프로필 이미지" height="26" id="gnb_profile_img" src="data:image/gif;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs%3D" width="26"/>
    print(imgTag[1])
    print(imgTag[2])

    result = []
    for temp in imgTag:
        result.append(temp)

    # def multi_processing_test(num):
    #     temp = num
    #     cnt = 0
    #     # input image data to m variable
    #     for m in img[4:-3]:
    #         img_src = m.get("src")
    #         img_name = img_src.replace("/", "")
    #         # console print
    #         print("total image count: " + str(len(img)-6))
    #         print("========================================")
    #         print("다운로드 링크: " + img_src)
    #         # pick the image file name
    #         for i in range(2, 6):
    #             if cnt < i ** 10:
    #                 print(str(cnt) + "번째 이미지 다운로드")
    #                 temp = "0" * (6 - i)
    #                 fullname = "N" + temp + str(cnt) + ".jpg"
    #                 break
    #         if img_src.find("http") != -1:
    #             # download image
    #             try:
    #                 for i in range(2, 6):
    #                     if cnt < i ** 10:
    #                         print(cnt, " 번째 이미지를 저장중입니다.")
    #                         temp = "0" * (6 - i)
    #                         # pick the image file name
    #                         fullname = "N" + temp + str(cnt) + ".jpg"
    #                         break
    #                 urllib.request.urlretrieve(img_src, "./img/" + fullname)  # error sentence
    #                 cnt += 1
    #                 print("다운로드 성공")
    #             except Exception as ex:
    #                 print("에러가 발생했습니다.")
    #                 print(str(cnt) + "번째 다운로드 예정 이미지를 다운받을 수 없습니다.")
    #                 print("상세 에러내역을 다음과 같습니다.")
    #                 print(ex)
    #         else:
    #             continue
    #         time.sleep(0.1)
    #         if cnt >= downloadCnt:
    #             # browser close
    #             print(cnt+1, " 번째 이미지를 저장하고 크롤러를 종료합니다.")
    #             break
    # if __name__ == '__main__':
    #     pool = Pool(processes=2)
    #     pool.map(multi_processing_test, range(0, 500))

    # ==================== Test ====================

    # def multi_processing_test(img):
    #     m = img
    #     print("========== m= " + str(m))
    #     cnt = 0
    #     # input image data to m variable
    #     img_src = m.get("src")
    #     img_name = img_src.replace("/", "")
    #     # console print
    #     print("total image count: " + str(len(imgTag) - 6))
    #     print("========================================")
    #     print("다운로드 링크: " + img_src)
    #     # pick the image file name
    #     for i in range(2, 6):
    #         if cnt < i ** 10:
    #             print(str(cnt) + "번째 이미지 다운로드")
    #             temp = "0" * (6 - i)
    #             fullname = "N" + temp + str(cnt) + ".jpg"
    #             break
    #     if img_src.find("http") != -1:
    #         # download image
    #         try:
    #             for i in range(2, 6):
    #                 if cnt < i ** 10:
    #                     print(cnt, " 번째 이미지를 저장중입니다.")
    #                     temp = "0" * (6 - i)
    #                     # pick the image file name
    #                     fullname = "N" + temp + str(cnt) + ".jpg"
    #                     break
    #             urllib.request.urlretrieve(img_src, "./img/" + fullname)  # error sentence
    #             cnt += 1
    #             print("다운로드 성공")
    #         except Exception as ex:
    #             print("에러가 발생했습니다.")
    #             print(str(cnt) + "번째 다운로드 예정 이미지를 다운받을 수 없습니다.")
    #             print("상세 에러내역을 다음과 같습니다.")
    #             print(ex)
    #     time.sleep(0.1)
    #     if cnt >= downloadCnt:
    #         # browser close
    #         print(cnt + 1, " 번째 이미지를 저장하고 크롤러를 종료합니다.")
    #         exit()


    def multi_processing_test(img):
        m = img
        print("m = " + str(m))
    print("result")
    print(result)
    print(type(result))

    if __name__ == '__main__':
        pool = Pool(processes=2)
        pool.map(multi_processing_test, result)
        # maximum recursion depth exceeded while pickling an object


# google image crawling
if googleCrawling:
    # ========== web crawling execute section ==========
    # open google website
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
    # definite variable
    isImgTap = False
    # go to image section
    for tabCnt in range(1, 5):
        tab = driver.find_element_by_css_selector(".hdtb-imb:nth-child(" + str(tabCnt) + ")")
        if tab.text == '이미지':
            isImgTap = True
            tab.click()
            break
    if not isImgTap:
        driver.find_element_by_class_name("sqXXR").click()
        for tabCnt in range(1, 3):
            tab = driver.find_element_by_css_selector(".il8Sef>a:nth-child(" + str(tabCnt) + ")")
            if tab.text == '이미지':
                isImgTap = True
                tab.click()
                break
    # definite variable
    i = -1
    loadTime = 0
    if not fastTestMode:
        while True:
            imgCnt = driver.page_source.count('class="rg_bx rg_di rg_el ivg-i"')
            print("Loaded image count :", imgCnt)
            # if image over 1000, break
            if imgCnt > 1000:
                print("Image loaded over 1000")
                break
            # if complete image load
            elif imgCnt > i:
                i = imgCnt
                # more image loading using scroll
                driver.execute_script("window.scrollBy(0,10000)")
                # more image loading using button click
                try:
                    driver.find_element_by_id("smb").click()
                except Exception as ex:
                    print(ex)
                continue
            # if image not loaded
            elif imgCnt == i:
                loadTime += 0.1
                # if load time more than 3 second, break
                if loadTime > 3:
                    print("Time out")
                    break
                else:
                    # wait image loading
                    time.sleep(0.1)

    # checking success to search
    assert "일치하는 검색결과가 없습니다." not in driver.page_source

    # ========== beautifulSoup setting ==========
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # ========== image download by beautifulSoup execute section ==========
    img = soup.find_all("div", {"class": "rg_bx rg_di rg_el ivg-i"})
    cnt = 0
    # input image data to m variable
    for m in img[:]:
        metaDiv = m.find("div", {"class": "rg_meta notranslate"})
        meta = eval(metaDiv.text)
        img_src = meta["ou"]
        # console print
        print("========================================")
        print(m["data-ri"] + "번째 이미지 다운로드")
        print("다운로드 링크: " + meta["ou"])
        # download image
        try:
            for i in range(2, 6):
                if cnt < i ** 10:
                    print(cnt, " 번째 이미지를 저장중입니다.")
                    temp = "0" * (6 - i)
                    # pick the image file name
                    if img_src[-3:] == "jpg" or img_src[-3:] == "png":
                        fullname = "G" + temp + str(cnt) + "." + img_src[-3:]
                    else:
                        fullname = "G" + temp + str(cnt) + ".jpg"
                    break
            urllib.request.urlretrieve(img_src, "./img/" + fullname)  # error sentence
            cnt += 1
            print("다운로드 성공")
        except Exception as ex:
            print("에러가 발생했습니다.")
            print(str(cnt) + "번째 다운로드 예정 이미지를 다운받을 수 없습니다.")
            print("상세 에러내역을 다음과 같습니다.")
            print(ex)
        time.sleep(0.1)
        if cnt >= downloadCnt:
            # browser close
            print(cnt+1, " 번째 이미지를 저장하고 크롤러를 종료합니다.")
            break


# Chrome driver close
if driver is not None:
    isQuited = False
    while not isQuited:
        try:
            time.sleep(1)
            driver.quit()
            isQuited = True
        except:
            print("다운로드가 끝나지 않아 종료 대기중입니다.")
