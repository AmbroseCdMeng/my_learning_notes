'''
2019年9月15日17:25:48

    验证码识别 -- 宫格验证码识别

宫格验证码是一种新型的交互式验证码，每个宫格之间会有一条连线，指示应该的滑动轨迹，需要按照指定轨迹一次滑行，才能完成验证。
'''

# 1、准备测试目标网站。https://passport.weibo.cn/signin/login
# 2、环境准备。Selenium + Chrome + ChromeDriver
# 3、获取模板。因目标网站的宫格只有 4 个点，所以验证码只有 24 中样式。如果有 9 个点，则会更多
# 4、

import time
from io import BytesIO
from PIL import Image
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


USERNAME = '18893121482'
PASSWORD = 'MCDdeweibo'


class CrackWeiboSlide():
    def __init__(self):
        self.url = 'https://passport.weibo.cn/signin/login'
        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, 20)
        self.username = USERNAME
        self.password = PASSWORD

    def __del__(self):
        self.browser.close()

    def open(self):
        '''
        打开网页输入用户名密码并点击
        '''
        self.browser.maximize_window()
        self.browser.get(self.url)

        username = self.wait.until(
            EC.presence_of_all_elements_located((By.ID, 'loginName')))
        password = self.wait.until(
            EC.presence_of_all_elements_located((By.ID, 'loginPassword')))
        submit = self.wait.until(
            EC.presence_of_all_elements_located((By.ID, 'loginAction')))
        username[0].send_keys(self.username)
        password[0].send_keys(self.password)
        submit[0].click()

    def get_position(self):
        '''
        获取验证码位置
        '''
        try:
            img = self.wait.until(EC.presence_of_all_elements_located(
                (By.CLASS_NAME, 'patt-shadow')))
        except TimeoutException:
            print('not found')
            self.open()
        time.sleep(2)
        location = img.location
        size = img.size
        top, bottom, left, right = location['y'], location['y'] + \
            size['height'], location['x'], location['x'] + size['width']
        return (top, bottom, left, right)

    def get_screenshot(self):
        '''
        获取网页截图
        '''
        screenshot = self.browser.get_screenshot_as_png()
        screenshot = Image.open(BytesIO(screenshot))
        return screenshot

    def get_image(self, name='captcha.png'):
        '''
        获取验证码图片
        '''
        top, bottom, left, right = self.get_position()
        print('验证码位置：', top, bottom, left, right)

        screenshot = self.get_screenshot()
        captcha = screenshot.crop((left, top, right, bottom))
        captcha.save(name)
        return captcha

    def main(self):
        '''
        批量获取验证码
        '''
        count = 0
        while True:
            self.open()
            self.get_image(str(count) + '.png')
            count += 1


if __name__ == '__main__':
    crack = CrackWeiboSlide()
    crack.main()
