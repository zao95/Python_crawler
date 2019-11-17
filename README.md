# Project-Predict-Crawler
Project_predict_crawler is a Naver image crawler using Python. 

The headless option has been applied for use in terminals as well, with chrome drivers built in.

## Required python library

beautifulsoup4==4.7.1

certifi==2019.3.9

chardet==3.0.4

idna==2.8

pathlib==1.0.1

requests==2.21.0

selenium==3.141.0

soupsieve==1.9.1

urllib3==1.24.2

## How to execute

1. Empty the img folder.

2. Enter search term in SearchWord location. Hangul is also available.

```python
# ========== important setting ==========
# choose the search word
searchWord = "SearchWord"
```
Location is [main.py] 9:11.

[main.py]: https://github.com/npr05324/Project-Predict-Crawler/blob/master/main.py

3. Execute main.py.

4. Check the output in img folder.

## License

Copyright (c) 2019 Kim Hyunwoo & Lee Jeongwoo. It is free software, 

and may be redistributed under the terms specified in the [LICENSE] file.

[LICENSE]: https://github.com/npr05324/Project-Predict-Crawler/blob/master/LICENSE
