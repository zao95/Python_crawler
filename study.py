import requests as re
from bs4 import BeautifulSoup

# html = re.get("https://fs.cathode.dev")
source = re.get("https://tv.naver.com/r")
print(source)  # 에러코드
# print(source.text)  # 소스코드
print(source.elapsed)  # 응답시간

html = BeautifulSoup(source.text, "html.parser")

# 1~3위 파싱
target1 = html.select("div.inner")
target2 = html.select("div.cds")
count = 0
print_list = []
for i in target1:
    count += 1
    print(F'{count}위 :', end=" ")

    target1_ = i.select_one("dt.title")
    print(target1_.text.strip(), end=" ")
    print_list.append(target1_.text.strip())

    try:
        target3 = i.select_one("span.rank")
        target3_ = target3.select_one("span.blind")
        print(target3_.text.strip())
    except:
        print("NEW")
for i in target2:
    count += 1
    print(F'{count}위 :', end=" ")

    target2_ = i.select_one("dt.title")
    print(target2_.text.strip(), end=" ")
    print_list.append(target1_.text.strip())

    try:
        target3 = i.select_one("span.rank")
        target3_ = target3.select_one("span.blind")
        print(target3_.text.strip())
    except:
        print("NEW")
print(print_list)