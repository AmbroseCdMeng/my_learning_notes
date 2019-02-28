# 2018年11月10日17:06:21

#     数据爬取 -- 动态渲染页面的爬取 -- Selenium的基本使用


# 1、声明浏览器对象
#     Selenium 支持很多浏览器。
#     包括如：
#         PC 端浏览器：Chrome、Firefox、Edge等；
#         手机端浏览器：Android、BlackBerry等
#         无界面浏览器：PhantomJS等

from selenium import webdriver
from selenium.webdriver.common.by import By
import time

from selenium import webdriver
from selenium.webdriver import ActionChains

from selenium.common.exceptions import NoSuchElementException, TimeoutException

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def fun_1():
    browser = webdriver.Chrome()
    browser = webdriver.Firefox()
    browser = webdriver.Edge()
    browser = webdriver.PhantomJS()
    browser = webdriver.Safari()


# 2、模拟浏览器操作访问页面

def fun_2():
    browser = webdriver.Chrome()
    browser.get('https://www.taobao.com')   # 访问 URL
    print(browser.page_source)              # 输出源码
    browser.close()                         # 关闭浏览器


# 3、查找节点。想要模拟点击、填充表单等操作，就需要对目标节点进行查找定位

def fun_3():
    browser = webdriver.Chrome()
    browser.get('https://www.taobao.com')
    input_first = browser.find_element_by_id('q')                   # 通过 ID选择器 获取
    input_second = browser.find_element_by_css_selector('#q')       # 通过 CSS选择器 获取
    input_third = browser.find_element_by_xpath('//*[@id="q"]')     # 通过 XPath 选择器获取
    print(input_first, input_second, input_third)
    # browser.close()

        # 另外 还有一种查找节点的方式： find_element() 方法。传入两个参数，第一个参数为 获取方式，第二个参数为 值
        # 使用该方法需要导入 By 库 from selenium.webdriver.common.by import By

    input_first = browser.find_element(By.ID, 'q')                  # 等价于上面的 ID 选择器

        # find_element() 方法只能获取指定条件的第一个节点
        # find_elements() 方法可以获取指定条件的所有节点。它返回的是一个列表，列表中的每个节点都是 WebElement 类型

    lis = browser.find_elements_by_css_selector('.service-bd li')   # 通过 CSS选择器 获取指定条件的所有节点
    lis = browser.find_elements(By.CSS_SELECTOR, '.service-bd li')  # 二者等价

    browser.close()

# 4、节点的交互（模拟操作）
    # 常用的方法：
        # send_keys()：输入文字
        # clear()：清空文字
        # click()：点击按钮
def fun_4():
    browser = webdriver.Chrome()                                    # 声明浏览器对象
    browser.get('https://www.taobao.com')                           # 打开指定链接
    input = browser.find_element_by_id('q')                         # 获取该链接下搜索框
    input.send_keys('iPhone')                                       # 输入文本内容
    time.sleep(1)                                                   # 暂停
    input.clear()                                                   # 清空文本框
    input.send_keys('iPad')                                         # 重新输入文本内容
    button = browser.find_element_by_class_name('btn-search')       # 获取搜索按钮
    button.click()                                                  # 点击按钮


# 5、动作链（没有特定的执行对象：如拖拽、键盘按键等）
    # from selenium import webdriver
    # from selenium.webdriver import ActionChains

def fun_5():
    browser = webdriver.Chrome()
    browser.get('http://www.runoob.com/try/try.php?filename=jqueryui-api-droppable')    # 模拟访问在线编辑器 尝试拖拽操作
    browser.switch_to.frame('iframeResult')
    source = browser.find_element(By.CSS_SELECTOR, '#draggable')    # 选中准备拖拽的节点
    target = browser.find_element(By.CSS_SELECTOR, '#droppable')    # 拖拽的目标节点
    action = ActionChains(browser)          # 声明动作链 ActionChains 对象
    action.drag_and_drop(source, target)    # 调用动作链对象的拖拽方法
    action.perform()        # 执行动作

    # 更多类型的动作链方法参考官方文档 Selenium API
    # https://selenium-python.readthedocs.io/api.html#module-selenium.webdriver.common.action_chains


# 6、执行 JavaScript
    # 对于某些操作 Selenium API 并没有提供。比如：下拉滚动条
    # 此时，就可以模拟 JavaScript 运行。使用 execute_script() 方法

def fun_6():
    browser = webdriver.Chrome()
    browser.get('https://www.zhihu.com/explore')
    browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')   # 执行JS代码 将滚动条下拉到最底部
    browser.execute_script('alert("Execute Success")')    # 指定JS代码 弹窗显示执行成功


# 7、获取节点信息
    # 前面有提到 可以通过 page_source 属性获取到网页的源码 然后调用解析库来提取信息
    # 但是 selenium 自身也提供了选择节点的方法 其返回的是 WebElement 类型

def fun_7():
    browser = webdriver.Chrome()
    browser.get('http://www.zhihu.com/explore')
    logo = browser.find_element(By.ID, 'zh-top-link-logo')  # 通过 ID 获取节点
    print(logo)     # 打印 logo 节点信息
    print(logo.get_attribute('class'))      # 打印 Logo 节点的 Class 属性

    input = browser.find_element(By.CLASS_NAME, 'zu-top-add-question')      # 通过 class 名获取节点（提问按钮）
    print(input.text)       # 节点内文本
    print(input.id)         # 节点 ID 
    print(input.location)   # 节点在页面的相对位置
    print(input.tag_name)   # 节点的标签名称
    print(input.size)       # 节点的大小（宽、高）


# 8、切换 Frame 子页面
    # Selenium 打开页面后 默认是在父级 Frame 中操作 而此时如果页面中还有子 Frame 它是无法获取到里面的节点的
    # 这种情况下 就需要使用 switch_to.frame() 方法来切换 Frame
    
def fun_8():
    browser = webdriver.Chrome()
    browser.get('http://www.runoob.com/try/try.php?filename=jqueryui-api-droppable')
    browser.switch_to_frame('iframeResult')     # 切换到子 Frame
    try:
        logo = browser.find_element(By.CLASS_NAME, 'logo')  # 尝试获取 logo 节点（logo节点存在父 Frame 所以这里是获取不到的）
        print(logo)
        print(logo.text)
    except NoSuchElementException:
        print('No Logo')

    browser.switch_to.parent_frame()    # 切换回父级 Frame
    try:
        logo = browser.find_element(By.CLASS_NAME, 'logo')  # 获取 logo 节点
        print(logo)
        print(logo.text)
    except NoSuchElementException:
        print('No Logo')
        

# 9、延时等待
    # 在 Selenium 中 get() 方法会在网页框架加载结束后执行。 此时的页面源码 page_source 并不一定是完整的
    # 在某些特定情况下，例如某些页面会有额外的 Ajax 请求。 想要获取到更加完整的源码 就需要延时等待 确保节点已经加载出来

    # 隐式等待：如果 Selenium 没有在 DOM 中找到节点，将等待一段时间，超出这个时间后，抛出找不到节点异常
        # 换句话说：当节点没有立即出现，则等待一段时间再次查找 DOM，默认时间 0 
    # 显式等待：指定最长等待时间，如果在规定的时间内加载出来了这个节点，则返回这个节点。如果超过该时间依然没有加载出来，则抛出异常
        # from selenium.webdriver.support.ui import WebDriverWait
        # from selenium.webdriver.support import expected_conditions as EC
        
def fun_9():
    browser = webdriver.Chrome()
    browser.get('https://www.zhihu.com/explore')
    browser.implicitly_wait(10)     # 隐式等待 10 秒
    input = browser.find_element(By.CLASS_NAME, 'zu-top-add-question')
    print(input)

def fun_10():
    browser = webdriver.Chrome()
    browser.get('https://www.taobao.com/')
    wait = WebDriverWait(browser, 10)           # 引入 WebDriverWait 对象 指定最长等待时间
    input = wait.until(EC.presence_of_all_elements_located((By.ID, 'q')))           # 调用 WebDriverWait 对象的 until 方法 传入等待的条件
    button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.btn-search')))       # 调用 WebDriverWait 对象的 until 方法 传入等待的条件
    print(input, button)
    # fun10 的整体效果为：如果 10 秒中之内 ID 为 q 的搜索框成功加载，class 为 btn-search 的按钮可点击， 则返回；否则，抛出异常
    # 以上传入的等待条件
        # title_is                                标题内容为
        # title_contains                          标题内容包含
        # presence_of_element_located             节点加载出来（传入定位元组）
        # visibility_of_element_located           节点可见（传入定位元组）
        # visibility_of                           为可见的（传入节点对象）
        # presence_of_all_elements_located        所有节点加载出来
        # text_to_be_present_in_element           某个节点包含
        # text_to_be_present_in_element_value     某节点的值包含
        # frame_to_be_available_and_switch_to_it  加载并切换 frame
        # invisibility_of_element_located         节点不可见
        # element_to_be_clickable                 节点可点击
        # staleness_of                            节点是否仍然在 DOM
        # element_to_be_selected                  节点可选择（传入节点对象）
        # element_located_to_be_selected          节点可选择（传入定位元组）
        # alert_is_present                        是否出现警告

        # 更多参考：http://selenium-python.readthedocs.io/api.html#module-selenium.webdriver.support.expected_conditions


# 10、前进和后退
    # back() 和 forward() 方法

def fun_11():
    browser = webdriver.Chrome()
    browser.get('https://www.baidu.com/')
    browser.get('https://www.taobao.com/')
    browser.get('https://www.python.org/')      # 一次打开三个网址
    browser.back()      # 后退
    time.sleep(1)
    browser.forward()   # 前进
    browser.close()

# 11、Cookies 管理

def fun_12():
    browser = webdriver.Chrome()
    browser.get('https://www.zhihu.com/explore')
    print(browser.get_cookies())         # 获取 cookies
    browser.add_cookie({'name':'admin', 'domain':'www.zhihu.com', 'value':'germey'})        # 添加 cookie
    print(browser.get_cookies())
    browser.delete_all_cookies()        # 删除 cookies
    print(browser.get_cookies())


# 12、选项卡管理

def fun_13():
    browser = webdriver.Chrome()
    browser.get('http://10.197.11.240:8090')        # 打开第一个网站
    browser.execute_script('window.open()')         # 执行 JS 代码 新开选项卡
    print(browser.window_handles)
    browser.switch_to_window(browser.window_handles[1])     # 切换到 第 1 个 选项卡（新开的选项卡）
    browser.get('http://10.197.11.240:8090/HCSKB')          # 访问第二个网址
    time.sleep(1)               
    browser.switch_to_window(browser.window_handles[0])     # 切换到 第 0 个 选项卡（最开始的选项卡）
    browser.get('https://www.baidu.com')                    # 访问第三个网址


# 13、异常处理
    # 更多异常类 参考：http://selenium-python.readthedocs.io/api.html#module-selenium.common.exceptions

def fun_14():
    browser = webdriver.Chrome()
    try:
        browser.get('https://www.baidu.com')
    except TimeoutException:
        print('Time Out')
    try:
        browser.find_element_by_id('hello')
    except NoSuchElementException:
        print('No Element')
    finally:
        browser.close()



if(__name__ == '__main__'):
    fun_13()


