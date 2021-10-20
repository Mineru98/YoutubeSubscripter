# -*- coding:utf-8 -*-
from selenium import webdriver
from bs4 import BeautifulSoup
import csv

f = open("./assets/subscrip_list.csv", "w", newline="", encoding="utf-8")
wr = csv.writer(f)
# open_chome_debug.sh를 디버깅 크롬을 열어서 미리 가져올 계정으로 로그인을 해둔다.

# chrome setting
_chrome_options = webdriver.ChromeOptions()
_chrome_options.add_argument("disable-infobars")
_chrome_options.add_argument("headless")
_chrome_options.add_argument("lang=ko_KR")
_chrome_options.add_argument("--no-sandbox")
_chrome_options.add_argument("--disable-dev-shm-usage")
_chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:{port}")
driver = webdriver.Chrome("./assets/chromedriver", options=_chrome_options)

url = "https://www.youtube.com"
driver.get(url)

# 좌측 메뉴바 오픈 여부 확인
yotube_menu = driver.find_element_by_id("masthead")
is_yotube_menu_open = yotube_menu.get_attribute("mini-guide-visible")

# 좌측 메뉴바가 닫혀있으면 해당 부분을 클릭해서 열기
if is_yotube_menu_open != None:
    driver.find_element_by_css_selector("#guide-button").click()

driver.find_element_by_css_selector(
    "#items > ytd-guide-collapsible-entry-renderer"
).click()

html_source = driver.page_source
soup = BeautifulSoup(html_source, "lxml")
s_list = soup.find_all(
    "a", {"class": "yt-simple-endpoint style-scope ytd-guide-entry-renderer"}
)

count = 1
wr.writerow([0, "채널명", "URL"])
for item in s_list[10 : len(s_list) - 12]:
    try:
        wr.writerow(
            [count, item.attrs["title"], "https://www.youtube.com" + item.attrs["href"]]
        )
        count += 1
    except KeyError as e:
        pass
f.close()
driver.quit()
