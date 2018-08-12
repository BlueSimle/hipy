# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from playhouse.db_url import connect

# 一、从csv文件导入数据
# df_csv = pd.read_csv('./data_input/guest_user_info.csv')
# print(df_csv)

# 二、从限定分隔符的文本文件导入数据
# pd.read_table('test.txt')

# 三、从excel文件导入数据
# pd.read_excel('test.xlsx')

# 四、从SQL表、库导入数据
# conn = connect("mysql://%s:%s@%s:%s/%s" % ('root','1234','127.0.0.1','3307','guest'))
# df = pd.read_sql_query('select * from user_info', conn)
# print(df)

# 五、从json格式的字符串导入数据
# pd.read_json(json_string)

# 六、解析url、字符串或者html文件，抽取其中的tables表格
# pd.read_html(url)

# 七、从你的粘贴板获取内容，并传给read_table()
# pd.read_clipboard()

# 八、从字典对象导入数据，key是列名，value是数据
# pd.DataFrame(dict)