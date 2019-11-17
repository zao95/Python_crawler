import time


def crawlingN(driver, searchWord, fastTestMode):

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

    htmlN = driver.page_source
    return htmlN
