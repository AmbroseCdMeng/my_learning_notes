# 2018年10月30日10:59:26

#     数据爬取 -- Ajax数据爬取 -- 结果提取

# Ajax 结果提取基本步骤：

#     1.分析请求
#         打开 Ajax 过滤器， 选定一个请求， 分析参数， 进入该请求详情页面
#     2.分析响应
#         分析请求返回的响应内容， 一般为 JSON 格式的数据
#     3.模拟测试

from urllib.parse import urlencode
import requests     # 请求库
from pyquery import PyQuery as pq       # 解析库

# 定义基本链接
base_url = "https://m.weibo.cn/api/container/getIndex?"     # cuiqingcai 个人微博

# 伪造请求头
headers = {
    'Host': 'm.weibo.cn',
    'Referer': 'https://m.weibo.cn/u/2830678474',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

# 向指定链接发送模拟请求 返回Json内容
def get_page(page):
    # 构造参数字典
    params = {
        'type': 'uid',
        'value': '2830678474',
        'containerid': '1076032830678474',
        'page': page
    }
    # 转换请求为GET请求参数 拼接完整链接
    url = base_url + urlencode(params)
    # 发送请求
    try:
        response = requests.get(url, headers = headers)
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError as e:
        print("Error", e.args)


# 解析返回响应
def parse_page(json):
    if json:
        items = json.get('data').get('cards')
        # print(items)
        for item in items :
            item = item.get('mblog')
            if item != None:
                weibo = {}
                weibo['id'] = item.get('id')        # ID
                weibo['text'] = pq(item.get('text')).text()     # 正文
                weibo['attitudes'] = item.get('attitudes_count')        # 点赞书
                weibo['comments'] = item.get('comments_count')      # 评论数
                weibo['reposts'] = item.get('reposts_count')        # 转发数
            yield weibo

# 遍历page输出获取结果
if __name__ == '__main__':
    for page in range(1, 11):
        json = get_page(page)
        # print(json)
        results = parse_page(json)
        for result in results:
            print(result)

'''

# 附加：保存结果到 MongDB 数据库
from pymongo import MongoClient

client = MongoClient()
db = client['weibo']
collection = db['weibo']

def save_to_mongo(result):
    if collection.insert(result):
        print("Save Success")

'''