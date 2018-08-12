# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

df = pd.DataFrame(data=[
    [11,'shiyi','sy@gmail.com',13838381411],
    [12,'shier','se@gmail.com',13838381412],
    [13,'shishan','ss@gmail.com',13838381413]
],columns=['id','username','email','phone'])

# 一、将df2的行添加到df1的尾部
# df1.append(df2)

# 二、将df2中的列添加到df1的尾部
# df.concat([df1,df2],axis=1)

# 三、对df1的列和df2的列执行sql形式的join
# df.join(df2,on=col1,how='inner')