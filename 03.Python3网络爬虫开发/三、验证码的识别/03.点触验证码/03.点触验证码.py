'''
2018年11月27日19:17:47

    验证码的识别 -- 点触验证码

点触验证码也是近几年出现的新型验证码之一。其特点是点击图片中符合要求的位置（挑选符合要求的图或字等）。所有答案都正确即验证通过。
'''

# 1、前期准备
#     selenium + Chrome + ChromeDriver
# 2、测试目标
#     https://www.touclick.com/       点触验证码服务站点
# 3、识别思路
#     1、图像识别。如 请选择下图中所有的 ****
#         首先要识别题目。题目一般经过压缩、变形、模糊化处理，导致OCR识别技术的精准度会大打折扣。
#         其次需要识别图片。需要大量的图片资源以供机器学习，可以借用识图接口，但成功率不高，图片清晰度不够时识别难度更大。
#     2、文字识别。如 请按顺序点击上图中的 ****
#         首先要识别题目。题目或多或少会有一些背景、线条、旋转等处理，识别难度较大。
#         其次需要识别图片中的字。一般这个识别难度要比题目中大很多。
# 4、验证码服务平台
#     https://www.chaojiying.com  （收费平台）
#     该平台提供了以下服务：
#         英文数字：20位以下的混合识别
#         中文汉字：7个以下的汉字识别
#         纯英文：12位以下的英文识别
#         纯数字：11位以下的数字识别
#         特殊字符：汉字、英文、计算题、成语混合、集装箱号等
#         坐标选择识别：复杂的计算题、问答题、选择题、点选相同的字、物品等返回多个坐标的识别
# 5、API准备、调整
#     cjyAPI.py
# 6、初始化变量

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

import time
from io import BytesIO
from PIL import Image

from cjyAPI import Chaojiying

# 目标网站信息
TEL = '18893121482'
EMAIL = ''
PASSWORD = '199510261515mcd'
URL = 'https://kyfw.12306.cn/otn/resources/login.html'  # 12306官网登录

# 验证码服务平台的用户名、密码、软件ID、验证码类型
CJY_USERNAME = 'CDMeng'
CJY_PASSWORD = '199510261515mcd'
CJY_SOFT_ID = '893590'
CJY_KIND = '9201'   # 不同类型收费标准  http://www.chaojiying.com/price.html

class CrackTouClick():
    def __init__(self):
        self.url = URL
        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, 20)
        self.email = EMAIL
        self.tel = TEL
        self.password = PASSWORD
        self.cjy = Chaojiying(CJY_USERNAME, CJY_PASSWORD, CJY_SOFT_ID)

    def open(self):
        """
        访问目标网站，键入用户名密码
        :return :None
        """
        self.browser.get(self.url)
        email = self.wait.until(EC.presence_of_element_located((By.ID, '')))
        password = self.wait.until(EC.presence_of_element_located((By.ID, '')))
        email.send_keys(self.email)
        password.send_keys(self.password)

    def get_touclick_button(self):
        """
        获取验证按钮
        :return :按钮对象
        """
        button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, '')))
        return button

    def get_touclick_element(self):
        """
        获取验证图片对象
        :return :图片对象
        """
        element = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'imgCode')))
        return element

    def get_position(self):
        """
        获取验证码位置
        :return :位置元组
        """
        element = self.get_touclick_element()
        time.sleep(2)
        location = element.location
        size = element.size
        top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size['width']
        return (top, bottom, left, right)

    def get_screenshot(self):
        """
        获取网页截图
        :return :图片对象
        """
        screenshot = self.browser.get_screenshot_as_png()
        screenshot = Image.open(BytesIO(screenshot))
        return screenshot

    def get_touclick_image(self, name = 'captcha.png'):
        """
        获取验证码图片
        :return :图片对象
        """
        top, bottom, left, right = self.get_position()
        print("验证码位置", top, bottom, left, right)
        screenshot = self.get_screenshot()
        # screenshot.show()
        captcha = screenshot.crop((left, top, right, bottom))
        return captcha

    
    # 解析识别结果
    def get_points(self, captcha_result):
        """
        解析识别结果
        :param captcha_result :识别结果 
                ex：  {'err_no': 0, 'err_str': 'OK', 'pic_id': '8051220461974300001', 'pic_str': '118,69|256,56|17,147|222,148', 'md5': '202e15c5609e132b238921546f49c12c'}
        :return :转换后的结果
        """
        groups = captcha_result.get('pic_str').split('|')
        locations = [[int(number) for number in group.split(',')] for group in groups]
        return locations

    def touch_click_words(self, locations):
        """
        点击验证图片
        :param location :点击位置
        :return :None
        """
        for location in locations:
            print('点击位置：',location)
            ActionChains(self.browser).move_to_element_with_offset(self.get_touclick_element(), location[0], location[1]).click().perform()
            time.sleep(1)

if __name__ == "__main__":

    # 初始化对象
    c = CrackTouClick()

    # 访问目标站点
    c.browser.get(URL)

    # 最大化窗口
    c.browser.maximize_window()


    '''
    循环验证
    '''
    while(1):
        
        # 选择账号登录功能
        btn_ = c.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.login-hd li:nth-child(2)')))
        
        # 点击更换登录方式
        btn_.click()

        # 键入用户名、密码
        input_name = c.wait.until(EC.presence_of_element_located((By.ID, 'J-userName')))
        input_password = c.wait.until(EC.presence_of_element_located((By.ID, 'J-password')))
        input_name.send_keys(TEL)
        input_password.send_keys(PASSWORD)

        # 获取验证码图片
        image = c.get_touclick_image()
        bytes_array = BytesIO()
        image.save(bytes_array, format='PNG')

        # 识别验证码
        print('正在识别...')
        result = c.cjy.PostPic(bytes_array.getvalue(), CJY_KIND)
        print('识别结果：', result)

        # 处理识别结果 获取点击坐标
        # result = {'err_no': 0, 'err_str': 'OK', 'pic_id': '8051220461974300001', 'pic_str': '118,69|256,56|17,147|222,148', 'md5': '202e15c5609e132b238921546f49c12c'}
        location = c.get_points(result)

        # 保存验证码 ID
        pic_id = result.get('pic_id')
        print(pic_id)

        # 点击验证图片
        c.touch_click_words(location)

        # 获取登录按钮
        btn_login = c.wait.until(EC.element_to_be_clickable((By.ID, 'J-login')))

        # 点击登录按钮
        btn_login.click()

        # 可否获取点击按钮后返回的AJAX信息

        # 强制刷新当前页面 获取页面标题来判断是否登录成功
        time.sleep(5)
        c.browser.refresh()
        try:
            c.wait.until(EC.presence_of_element_located((By.ID, 'J-header-logout')))
            print('登录成功')
            break
        except:
            c.cjy.ReportError(pic_id)

        time.sleep(5)

    print('执行其他操作')

    