# -*- coding:utf-8 -*-
from selenium import webdriver
from bs4 import BeautifulSoup
import csv
import argparse


def start(port):
    url_list = list()
    f = open("./assets/subscrip_list.csv", "r", newline="", encoding="utf-8")
    rdr = csv.reader(f)
    for row in rdr:
        url_list.append(row[2])
    f.close()

    # chrome setting
    _chrome_options = webdriver.ChromeOptions()
    _chrome_options.add_argument("disable-infobars")
    _chrome_options.add_argument("headless")
    _chrome_options.add_argument("lang=ko_KR")
    _chrome_options.add_argument("--no-sandbox")
    _chrome_options.add_argument("--disable-dev-shm-usage")
    _chrome_options.add_experimental_option(
        "debuggerAddress", "127.0.0.1:{}".format(port)
    )
    driver = webdriver.Chrome("./assets/chromedriver", options=_chrome_options)
    for url in url_list[1:]:
        driver.get(url)
        html_source = driver.page_source
        soup = BeautifulSoup(html_source, "lxml")
        header = soup.find("div", {"id": "inner-header-container"})
        header = header.find("div", {"id": "subscribe-button"})
        button = header.find(
            "yt-formatted-string",
            {"class": "style-scope ytd-subscribe-button-renderer"},
        )
        if button.text == "구독":
            driver.find_element_by_css_selector(
                "#subscribe-button > ytd-subscribe-button-renderer > tp-yt-paper-button"
            ).click()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="유튜브 구독하기", description="유튜브 구독기")
    parser.add_argument("-p", "--port", dest="port", help="크롬 디버깅 모드 포트")
    args = parser.parse_args()
    port = args.port
    start(port)
