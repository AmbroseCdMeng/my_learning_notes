# 2018年11月9日16:30:44

#     数据爬取 -- 动态渲染页面的爬取 -- Selenium的示例

# Selenium 是一个自动化测试工具，利用它可以驱动浏览器执行特定的动作，模拟点击、滚动等操作。
#     同时还可以获取浏览器当前呈现的页面源代码

# 1、安装 Selenium 库
# 2、基本使用
#       示例功能
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

browser = webdriver.Chrome()
try:
    browser.get('http://www.baidu.com')
    input = browser.find_element_by_id('kw')
    input.send_keys('Python')
    input.send_keys(Keys.ENTER)
    wait = WebDriverWait(browser, 10)
    wait.until(EC.presence_of_element_located((By.ID, 'content_left')))
    print(browser.current_url)
    print(browser.get_cookies())
    print(browser.page_source)
finally:
    browser.close()
    