import  selenium
from selenium import  webdriver


browser = webdriver.Chrome()


browser.get('https://maoyan.com/board/4?')
print(browser.page_source)
