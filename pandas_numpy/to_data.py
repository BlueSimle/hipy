# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from playhouse.db_url import connect

df = pd.DataFrame(data=[
    [11,'shiyi','sy@gmail.com',13838381411],
    [12,'shier','se@gmail.com',13838381412],
    [13,'shishan','ss@gmail.com',13838381413]
],columns=['id','username','email','phone'])

# 一、导出数据到csv文件，index=Fales不要第一列
# df.to_csv('test.csv',index=False)

# 二、导出数据到excel文件
# df.to_excel('test.xlsx')

# 三、导出数据到sql表
# table_name = '' # 表名
# db_conn = '' # 数据库连接
# df.to_sql(table_name, conn)

# 四、以json格式导出数据到文本文件
# df.to_json('test.josn')

