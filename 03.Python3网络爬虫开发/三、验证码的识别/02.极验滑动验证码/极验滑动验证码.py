'''
2018年11月25日13:52:50

    验证码的识别 -- 极验滑动验证码

极验滑动验证码是近几年出现的新型验证码之一。其特点就是需要拖动拼合滑块才能完整验证。
'''

# 1、前期准备
#     Selenium + Chrome + ChromeDriver
# 2、测试目标
#     https://www.geetest.com/    专门提供验证安全的网站
# 3、极验验证码的特点
#     极验验证码的识别难度相对图形验证码更大。
#     目前极验验证码 3.0 版本的验证步骤：
#         --> 点击"确定"按钮开始验证 
#         --> 弹出滑动验证窗口
#         --> 拖动滑块拼合图形
#         --> 生成三个加密参数，通过表单提交到后台
#         --> 后台再次验证
#     最新版的极验验证码还增加了机器学习的方式去识别拖动轨迹是否是人类操作

#     目前"验证安全官网"的安全防护有以下几点：
#         □ 三角防护之防模拟。利用机器学习和神经网络构建线上线下多重静态、动态防御模型。识别模拟轨迹，界定人机边界。
#         □ 三角防护之防伪造。深度分析浏览器的实际性能来识别伪造信息，同时根据伪造时间更新黑名单，大幅提升防伪造能力。
#         □ 三角防护之防暴力。利用神经网络生成海量图库储备，大幅减少图片重复概率，提升更新频率，极大程度提高暴力识别的成本。
# 4、识别思路
#     1、模拟表单提交（排除）。加密参数的构造过程和校验逻辑相对繁琐复杂。
#     2、模拟浏览器操作（可行）。
#         测试：
#             1、确定测试地址：https://account.geetest.com/login
#                             https://www.binance.co/register.html?ref=35902631
#                             https://www.binance.co/login.html
#             2、配置所需参数：用户名（邮箱）、密码
#             3、模拟点击验证按钮。触发极验验证码刷新
#             4、识别验证码图片缺口
#             5、模拟拖动

####################################################################################


# 导入模块
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import time

# 定义参数常量
URL = 'https://www.binance.co/login.html'
E_MAIL = '395239311@qq.com'
PASSWORD = '12345SHDLH'

class CrackGeetest():

    # 初始化参数与Selenium对象
    def __init__(self):
        self.url = URL
        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, 30)
        self.email = E_MAIL
        self.password = PASSWORD

    # 获取验证按钮
    def get_geetest_button(self):
        """
        return: 按钮对象
        """
        # button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'btn btn-orange btn-block')))
        button = self.wait.until(EC.element_to_be_clickable((By.ID, 'login-btn')))
        return button

    # 识别验证码图片缺口(获取前后两张图片。对比二者的不一致地方即为缺口)
    # 获取验证码图片位置
    def get_position(self):
        """
        return: 验证码位置元组
        """
        # 缺口图片
        # img = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_canvas_bg geetest_absolute')))
        # 滑块
        # img = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_canvas_slice geetest_absolute')))
        # 不带缺口图片
        # print('start')
        # print(self.browser.page_source)
        img = self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'geetest_canvas_fullbg geetest_fade geetest_absolute')))
        img.show()
        time.sleep(2)
        location = img.location
        size = img.size
        top, bottom, left, right = location['y'], location['y'] + size['heignt'], location['x'], location['x'] + size['width']
        return (top, bottom, left, right)

    # 获取验证码图片
    def get_geetest_image(self, name = 'captcha.jpg'):
        """
        param name: 图片名
        return: 图片对象
        """
        top, bottom, left, right = self.get_position()
        print('验证码位置', top, bottom, left, right)
        screenshot = self.get_screenshot()  # 获取网页截图
        captcha = screenshot.crop((left, top, right, bottom))   # 裁取图片，获取image对象
        return captcha

    # 获取滑块对象
    def get_slider(self):
        """
        return: 滑块对象
        """
        slider = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_slider_button')))
        return slider

    # 点击呼唤出缺口
    # slider = self.get_slider()
    # slider.click()

    # 获取第二张图片

    # 对比两张图片 获取缺口
    def is_pixel_equal(self, image1, image2, x, y):
        """
        param image1: 图片1
        param image2: 图片2
        param x: 位置x
        param y: 位置y
        return: 像素是否相等
        """
        # 取两张图片的像素点
        pixel1 = image1.load()[x, y]
        pixel2 = image2.load()[x, y]
        # 定义允许误差范围 阈值
        threshold = 60
        if abs(pixel1[0] - pixel2[0]) < threshold and abs(pixel1[1] - pixel2[1]) < threshold and abs(pixel1[2] - pixel2[2]) < threshold:
            return True
        return False

    # 获取缺口偏移量
    def get_gap(self, image1, image2):
        """
        param image1: 不带缺口图片
        param image2: 带缺口图片
        """
        left = 60 # 搜索的起始横坐标定位60 查找缺口位置。因为两张图片不同的位置地方一个为滑块，一个为缺口，而缺口在滑块右侧，所以直接从60开始搜索
        for i in range(left, image1.size[0]):
            for j in range(image1.size[1]):
                if not self.is_pixel_equal(image1, image2, i, j):
                    left = 1
                    return left
        return left    
            
    # 模拟拖动。需要完全模拟真人操作需要遵循两点
        # 1、前段加速运动，速度与加速度小幅度随机变动
        # 2、后段减速运行，速度与加速度小幅度随机变动
        #   x = v0 * t + 0.5 * a * t * t
        #   v = v0 + a * t
    def get_track(self, distance):
        """
        :param distance: 偏移量
        :return: 移动轨迹
        """
        # 移动轨迹
        track = []
        # 当前位移
        current = 0
        # 减速阈值
        mid = distance * 4 / 5
        # 计算间隔
        t = 0.2
        # 初速度
        v = 0

        while current < distance:
            if current < mid:
                # 加速度为 +2
                a = 2
            else:
                # 加速度为 -3
                a = -3
            # 初速度为 0
            v0 = 0
            # 当前速度 v = v0 + a * t
            v = v0 + a * t
            # 移动距离 x = v0 * t + 1/2 * a * t^2
            move = v0 * t + 1 / 2 * a * t * t
            # 当前位移
            current += move
            # 加入轨迹
            track.append(round(move))
        return track

    # 拖动滑块
    def move_to_gap(self, slider, tracks):
        # 按住拖动滑块
        ActionChains(self.browser).click_and_hold(slider).perform()
        for x in tracks:
            # 执行拖动动作 获取位移距离
            ActionChains(self.browser).move_by_offset(xoffset = x, yoffset = 0).perform()
        time.sleep(0.5)
        # 释放鼠标
        ActionChains(self.browser).release().perform()


if __name__ == '__main__':
    # 创建 CrackGeetest 对象
    cg = CrackGeetest()
    # 访问目标连接
    cg.browser.get(cg.url)
    # 最大化窗口
    cg.browser.maximize_window()
    # 键入用户名密码
    input_email = cg.wait.until(EC.presence_of_element_located((By.ID, 'email')))
    input_email.send_keys(cg.email)
    input_password = cg.wait.until(EC.presence_of_element_located((By.ID, 'pwd')))
    input_password.send_keys(cg.password)
    # 获取登录按钮
    login_button = cg.get_geetest_button()
    # 点击登录按钮
    # print('****************************')
    # print(cg.browser.page_source)
    login_button.click()
    
    # 获取第一张图片
    # print('*****')
    # print(cg.browser.page_source)
    cg.get_geetest_image('pic1.jpg')
    # 点击呼出缺口
    slider = cg.get_slider()
    slider.click()
    # 获取第二张图片
    cg.get_geetest_image('pic2.jpg')
    # 执行拖动
    cg.move_to_gap(slider, cg.get_track(get_gap))
