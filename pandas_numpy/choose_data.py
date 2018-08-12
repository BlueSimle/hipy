# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

df = pd.DataFrame(data=[
    [11,'shiyi','sy@gmail.com',13838381411],
    [12,'shier','se@gmail.com',13838381412],
    [13,'shishan','ss@gmail.com',13838381413]
],columns=['id','username','email','phone'])


# 一、根据列名，并以Series的形式返回列
# print(df['id'])

# 二、以DataFrame形式返回多列
# print(df[['id','username']])

# 三、按位置选取数据
# print(s.iloc[0])

# 四、按索引选取数据
# print(s.loc['index_one'])

# 五、返回第一行
# print(df.iloc[0,:])
# print(df.iloc[0])

# 六、返回第一列的第一个元素
# print(df.iloc[0,0])