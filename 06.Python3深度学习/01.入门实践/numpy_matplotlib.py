# 2018年12月13日19:38:07

#     numpy & matplotlib

# numpy：数值计算库。提供高级的数学算法和便利的数组（矩阵）操作。
# matplotlib：画图库。将实验结果可视化，方便从视觉上确认深度学习运行期间的数据。

import numpy as np
import matplotlib as plt

# 1、生成 Numpy 数组
x = np.array([1.0, 2.0, 3.0])   # 传入列表作为参数
print(x)