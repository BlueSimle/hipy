# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

df = pd.DataFrame(data=[
    [11,'shiyi','sy@gmail.com',13838381411],
    [12,'shier','se@gmail.com',13838381412],
    [13,'shishan','ss@gmail.com',13838381413]
],columns=['id','username','email','phone'])

# 一、重命名列名
# df.columns = ['a','b','c','d']
# print(df)

# 二、检查DataFrame对象中的空值、并返回一个Boolean数组
# print(pd.isnull(df))

# 三、检查DataFrame对象中的非空值，并返回一个Boolean数组
# print(pd.notnull(df))

# 四、删除所有包含空值的行
# df.dropna()

# 五、删除所有包含空值的列
# df.dropna(axis=1)

# 六、删除所有小于n个非空值的行
# df.dropna(axis=1,thresh=n)

# 七、用x替换DataFrame对象中所有的空值
# df.fillna(x)

# 八、将Series中的数据类型更改为float类型
# s.astype(float)

# 九、用'one'代替所有等于1
# s.replace(1,'one')

# 十、用'one'代替1，用'three'代替3
# s.replace([1,3],['one','three'])

# 十一、批量更改列名
# print(df.rename(columns=lambda x:x + '1'))

# 十二、选择性更改列名
# df.rename(columns={'old_name':'new_name'})

# 十三、更改索引列
# df.set_index('column_one')

# 十四、批量重命名索引
# print(df.rename(index=lambda x:x + 1))