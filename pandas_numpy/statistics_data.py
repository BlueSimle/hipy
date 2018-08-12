# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

df = pd.DataFrame(data=[
    [11,'shiyi','sy@gmail.com',13838381411],
    [12,'shier','se@gmail.com',13838381412],
    [13,'shishan','ss@gmail.com',13838381413]
],columns=['id','username','email','phone'])

# 一、查看数据值列的汇总统计
# print(df.describe())

# 二、返回所有列的均值
# df.mean()

# 三、返回列与列之间的相关系数
# df.corr()

# 四、返回每一列中的非空值的个数
# df.count()

# 五、返回每一列的最大值
# df.max()

# 六、返回每一列的最小值
# df.min()

# 七、返回每一列的中位数
# df.median()

# 八、返回每一列的标准差
# df.std()