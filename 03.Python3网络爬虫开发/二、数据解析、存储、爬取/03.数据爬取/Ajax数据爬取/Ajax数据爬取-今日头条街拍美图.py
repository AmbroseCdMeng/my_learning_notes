# 2018年11月5日9:05:50

#     数据爬取 -- Ajax数据爬取 -- Ajax爬取今日头条街拍美图

#     因反爬技术不断更新 该代码于2018年11月5日16:53:04测试可用 后续可能需要根据反爬技术略作修改

#  基本步骤：
#     1.前期准备
#         安装 requests 库
#     2.抓取分析
#         确定目标地址。  http://www.toutiao.com/
#         分析抓取逻辑
#         查看网络请求
#         分析请求结果 -- 发现网页源代码中并无页面中的标题 - 初步判断：页面由Ajax加载，JS渲染
#         确认渲染信息的提取与筛选规则 -- data --> image_detail --> url

#     3.模拟Ajax请求提取数据

import time
import requests
from urllib.parse import urlencode
import os
from hashlib import md5
from multiprocessing.pool import Pool

# 加载单个 Ajax 请求

def get_page(offset):
    # 构造 get 请求参数 转码构造完整链接
    params = {
        'offset': offset,
        'format': 'json',
        'keyword': '街拍',
        'autoload': 'true',
        'count': '20',
        'cur_tab': '1',
    }
    url = 'http://www.toutiao.com/search_content?' + urlencode(params)

    # 发送请求 返回JSON数据
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError:
        return None


# JSON 数据解析 提取图片链接

def get_image(json):
    if json.get('data'):
        for item in json.get('data'):
            title = item.get('title')
            images = item.get('image_list')
            if images != None:
                for image in images:
                    yield{
                        'image': image.get('url'),
                        # 'title':title + str(round(time.time() * 1000))  # 毫秒级时间戳
                        'title': title
                    }
            else:
                print('Not Found ImageList')

# 保存图片
def save_image(item):
    if not os.path.exists(item.get('title')):
        os.mkdir(item.get('title'))
    try:
        temp = item.get('image')
        response = requests.get('http:' + item.get('image'))
        if response.status_code == 200:
            file_path = 'pic/{0}/{1}.{2}'.format(item.get('title'),
                                             md5(response.content).hexdigest(), 'jpg')
            if not os.path.exists(file_path):
                with open(file_path, 'wb') as f:
                    f.write(response.content)
            else:
                print('Already download', file_path)
    except requests.ConnectionError:
        print('Failed to Save Image')


# 构造offset数组 提取图片链接 下载图片

def main(offset):
    print("Running")
    json = get_page(offset)
    for item in get_image(json):
        # print(item)
        save_image(item)


# 定义分页起止

GROUP_START = 1
GROUP_END = 20

# 利用线程池实现多线程下载  ★ Python是解释性语言 其方法必须先定义才能使用 这一点和其它许多语言不同

if __name__ == '__main__':
    print('START')
    pool = Pool()
    groups = ([x * 20 for x in range(GROUP_START, GROUP_END + 1)])
    # print(groups)
    pool.map(main, groups)
    # main(groups)
    pool.close()
    pool.join()
    print('THE END')
