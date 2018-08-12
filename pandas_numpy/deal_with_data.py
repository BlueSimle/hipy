# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

df = pd.DataFrame(data=[
    [11,'shiyi','sy@gmail.com',13838381411],
    [12,'shier','se@gmail.com',13838381412],
    [13,'shishan','ss@gmail.com',13838381413]
],columns=['id','username','email','phone'])

# 一、选择col列的值大于0.5的行
# df[df[col]>0.5]

# 二、按照col排序数据，默认升序排列
# df.sort_values(col)

# 三、按照列col降序排列
# df.sort_values(col, ascending=False)

# 四、先按列col1升序排列，后按col2降序排列
# df.sort_values([col1,col2],ascending=[True, False])

# 五、返回一个按列col进行分组的Groupby对象
# df.groupby(col)

# 六、返回一按多列进行分组的Groupby对象
# df.groupby([col1,col2])

# 七、返回按列col1分组后，列col2的均值
# df.groupby(col1)[col2]

# 八、创建一个按列col1进行分组，并计算col2和col3的最大值的数据透视表
# df.pivot_table(index=col1,values=[col2,col3],aggfunc=max)

# 九、返回按列col1分组的所有的均值
# df.groupby(col1).agg(np.mean)

# 十、对DataFrame中的每一列应用函数np.mean
# df.apply(np.mean)

# 十一、对DataFrame中的每一行应用函数np.max
# df.apply(np.max,axis=1)

