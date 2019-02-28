'''
 2018年11月20日19:44:34

    验证码的识别 -- 图形验证码

图形验证码是最早出现的、也是最常见的一种验证码。一般由 4 ~ 6 位数字或字母组成。
'''

# 1、目标确定
#     知网：http://my.cnki.net/elibregister/commonRegister.aspx
# 2、前期准备
#     安装 tesserocr 库。利用 OCR 技术识别图形验证码
# 3、获取验证码
#     进入开发模式，保存验证码图片到本地。http://my.cnki.net/elibregister/CheckCode.aspx
# 4、识别测试
#     启动项目，调用 tesserocr 识别验证码
# 5、验证码处理
#     额外对验证码图片进行二值化操作、灰度转换等操作。提高验证码的识别率

import tesserocr
from PIL import Image

''' 示例代码

image = Image.open('jpg/code.jpg')
result = tesserocr.image_to_text(image)
print(result)   # 由于线条的干扰。  可能识别不准确

# 处理验证码图片
image = image.convert('L')  # 将图像转换为灰度图像
# image.show()
image = image.convert('1')  # 将图片进行二值化处理。可以指定二值化的阈值。默认为127。原图不能直接转换，需要转为灰度图像后才可以指定二值化的阈值
image.show()

'''

# 完整的转换代码如下
image = Image.open('jpg/code.jpg')
image = image.convert('L')
threshold = 127  # 阈值
table = []
for i in range(256):
    if i < threshold:
        table.append(0)
    else:
        table.append(1)

image = image.point(table, '1')
image.show()

result = tesserocr.image_to_text(image)
print(result)

