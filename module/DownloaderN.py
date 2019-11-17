from bs4 import BeautifulSoup
import urllib.request
import time
import hashlib
import os


def dataN(html, downloadCnt):

    # html parsing
    soup = BeautifulSoup(html, 'html.parser')

    # ========== image download by beautifulSoup execute section ==========
    img = soup.find_all("img")
    # delete unnecessary part
    del img[0:4]
    del img[-3:]
    imgSrcListN = []
    imgNameListN = []

    # input image data to m variable
    for m in img:
        imgSrcN = m.get("src")
        imgNameN = hashlib.md5(bytes(imgSrcN, encoding='utf8')).hexdigest()[0:32]
        imgSrcListN.append(str(imgSrcN))
        imgNameListN.append(str(imgNameN))

    data = []
    if len(imgSrcN) >= downloadCnt:
        for i in range(downloadCnt):
            data.append((imgSrcListN[i], imgNameListN[i]))
    else:
        for i in range(len(imgSrcListN)):
            data.append((imgSrcListN[i], imgNameListN[i]))
    return data


def downloadingN(data):

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