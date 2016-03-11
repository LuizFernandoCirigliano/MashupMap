import requests
import re
from selenium import webdriver


def check_youtube(url_check):
    r = requests.get(url_check)
    html = r.text
    # print(str(html))
    match = re.search('Sorry about that', html)
    if match:
        return True
    else:
        return False

def check_soundcloud(url_check):
    driver = webdriver.PhantomJS()
    driver.set_window_size(1120, 550)
    driver.get(url_check)
    # help(driver)
    html = driver.page_source
    # print(html)
    match = re.search('We can.t find that track\.', html)
    # print(match)
    if match:
        return True
    else:
        return False



# print(check_youtube('https://www.youtube.com/watch?v=em0MknB6wFo'))
print(check_soundcloud('https://soundcloud.com/cntrlmashups/hotline-link'))
