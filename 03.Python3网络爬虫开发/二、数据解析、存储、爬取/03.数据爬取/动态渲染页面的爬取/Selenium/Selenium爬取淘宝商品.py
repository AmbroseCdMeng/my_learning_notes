# 2018年11月15日19:06:43

#     数据爬取 -- 动态渲染页面的爬取 -- Selenium 爬取淘宝商品

# 1、目标确定。
#     目标地址：https:www.taobao.com
# 2、配置准备。
#     软件配置：Chrome、PhantomJS、Firefox
#     驱动配置：ChromeDriver、GeckoDriver
#     存储配置：MongoDB
#     模块导入：Selenium
# 3、接口分析。
#     访问目标地址。
#     模拟搜索功能。
#     截获 AJAX 请求。
#     分析商品列表接口。
# 4、获取数据 
#     构造参数抓取返回结果。
#     保存结果至数据库

# 导入模块
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from urllib.parse import quote

from pyquery import PyQuery as pq
import pymongo



# 初始化浏览器对象
browser = webdriver.Chrome()

# 指定默认的等待时间
wait = WebDriverWait(browser, 10)

# 初始化搜索关键字
KEYWORDS = 'IPad'

# 初始化目标基本地址 关键字转码 合并完整地址
url = 'https://s.taobao.com/search?q=' + quote(KEYWORDS)

# 抓取商品列表信息
def index_page(page):
    print('正在获取第 ', page, ' 页')
    try:
        browser.get(url)
        # 模拟页面跳转 -- 输入页码，点击跳转
        # 当前页 > 1 时 模拟跳转动作。否则等待当前页面加载完成
        if page > 1:
            input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager div.form > input')))
            submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager div.form > span.btn.J_submit')))
            input.clear()
            input.send_key(page)
            submit.click()
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '.m-itemlist .items .item')))
        # 自定义方法：解析商品列表
        get_products()
    except TimeoutError:
        index_page(page)

# 解析商品列表
def get_products():
    # 获取目标页源码
    html = browser.page_source
    # 解析源码 提取商品列表
    doc = pq(html)
    items = doc('#mainsrp-itemlist .items .item').items()
    for item in items:
        product = {
            'image':item.find('.pic .img').attr('data-src'),
            'price':item.find('.price').text,
            'deal':item.find('.deal-cnt').text(),
            'title':item.find('.title').text(),
            'shop':item.find('.shop').text(),
            'location':item.find('.location').text()
        }
        print(product)
        # 自定义方法：保存数据
        save_to_mongo(product)


# 初始化 MongoDB 连接参数
MONGO_URL = 'localhost'
MONG_DB = 'taobao'
MONG_COLLECTION = 'products'

# 建立 MongoDB 连接
client = pymongo.MongoClient(MONGO_URL)
db = client[MONG_DB]

# 保存数据到 MongoDB 
def save_to_mongo(result):
    try:
        if db[MONG_COLLECTION].insert(result):
            print('保存成功')
    except Exception:
        print("保存失败")


# 初始化最大页数
MAX_PAGE = 100

# 多页抓取
def main():
    for i in range(1, MAX_PAGE + 1):
        index_page(i)
    

# 入口
if __name__ == '__main__':
    browser.get('https://s.taobao.com/search?q=' + quote('IPAD'))
    browser.add_cookie(
        {'domain': 'login.taobao.com', 
        'expiry': 1857646467, 
        'httpOnly': False, 
        'name': '_uab_collina', 
        'path': '/member', 
        'secure': False, 
        'value': '154228646732844118213349'})
    main()