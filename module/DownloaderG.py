from bs4 import BeautifulSoup
import urllib.request
import time
import hashlib
import os
from pathlib import Path


def dataG(html, downloadCnt):

    # html parsing
    soup = BeautifulSoup(html, 'html.parser')

    # ========== image download by beautifulSoup execute section ==========
    img = soup.find_all("div", {"class": "rg_bx rg_di rg_el ivg-i"})
    imgSrcListG = []
    imgNameListG = []

    # input image data to m variable
    for m in img[:]:
        metaDiv = m.find("div", {"class": "rg_meta notranslate"})
        meta = eval(metaDiv.text)
        imgSrcG = meta["ou"]
        imgNameG = hashlib.md5(bytes(imgSrcG, encoding='utf8')).hexdigest()[0:32]
        imgSrcListG.append(str(imgSrcG))
        imgNameListG.append(str(imgNameG))

    data = []
    if len(imgSrcG) >= downloadCnt:
        for i in range(downloadCnt):
            data.append((imgSrcListG[i], imgNameListG[i]))
    else:
        for i in range(len(imgSrcListG)):
            data.append((imgSrcListG[i], imgNameListG[i]))
    return data


def downloadingG(data):

    # import data from return value of dataG function
    src = data[0]
    name = data[1]

    # if not the file has downloaded
    if not ((os.path.exists("./img/" + str(name) + ".jpg")) or (os.path.exists("./img/" + str(name) + ".png"))):
        try:
            # pick the image file name
            if src[-3:] == "jpg" or src[-3:] == "png":
                fullname = name + "." + src[-3:]
            else:
                fullname = name + ".jpg"

            # file download
            urllib.request.urlretrieve(src, "./img/" + fullname)

            # make downloadListG
            path = Path("img/" + name)
            full_path = path.absolute()
            my_path = full_path.as_posix()
            print(my_path)
            print(type(my_path))
            print(src)
            print(name)
            print("다운로드 성공")
        except Exception as ex:
            print("에러가 발생했습니다.")
            print("상세 에러내역을 다음과 같습니다.")
            print(ex)
        time.sleep(0.1)
    else:
        print("이미 다운로드받은 파일입니다.")