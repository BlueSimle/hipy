# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

df = pd.DataFrame()

# 一、查看DataFrame对象的前n行
# df.head(n)

# 二、查看DataFrame对象的最后n行
# df.tail(n)

# 三、查看行数和列数
# df.shape()

# 四、查看索引、数据了下和内存信息
# print(df.info())

# 五、查看数值型列的汇总统计
# df.describe()

# 六、查看Series对象的每唯一值和基数
# s.value_count(dropna=False)

# 七、查看DataFrame对象中每一列的唯一值和计数
# df.apply(pd.Series.value_counts)