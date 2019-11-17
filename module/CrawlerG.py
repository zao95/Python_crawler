import time


def crawlingG(driver, searchWord, fastTestMode):

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

    htmlG = driver.page_source
    return htmlG
