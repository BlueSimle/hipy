# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import xlrd, openpyxl

# 加载excel数据
weibo_xlsx = pd.ExcelFile('./data/weibo_data.xlsx')

# 取出sheet的all
all = weibo_xlsx.parse('All')

# 删除无用的列
df = all.drop(all.columns[:11],axis=1,inplace=False)
all = df.drop(df.columns[-1],axis=1,inplace=False)

# 获取到重复的行的行号的前20个
# all[all.duplicated()==True].index[:20]
# 删除掉重复的行，在原值上直接修改
all.drop_duplicates(inplace=True)

# 处理缺失值
all[u'转发数'][all[u'转发数']==u'转发'] = '0'
all[u'评论数'][all[u'评论数']==u'评论'] = '0'
# 等价于 all[u'点赞数'].replace(u'赞','0')
all[u'点赞数'][all[u'点赞数']==u'赞'] = '0'

# 为了能进行数据透视，需要将对应的列的数据类型转换成数值
# 将DataFrame表中的某列数据进行转换类型
all[u'转发数'] = all[u'转发数'].astype('int64')
all[u'评论数'] = all[u'评论数'].astype('int64')
all[u'点赞数'] = all[u'点赞数'].astype('int64')

# 将预处理过的保存到另一个变量
all_save = all

#------------------------------------------------------------------------

# 数据透视表
all_pivot = all.pivot_table(values=[u'转发数',u'评论数',u'点赞数',u'微博内容'],index=[u'用户名'],\
                            aggfunc={u'转发数':np.sum,u'评论数':np.sum,u'点赞数':np.sum,u'微博内容':np.size})

# 给该列换名称
all_pivot.rename(columns={u'微博内容':u'当月总微博数'},inplace=True)

# 保存完成的透视表
all_pivot_save = all_pivot

#------------------------------------------------------------------

# 读取sf单元
sf = weibo_xlsx.parse('sf')

# 读取sfweibo单元
sf_weibo = weibo_xlsx.parse('sfweibo')

# 通过上面的表格输出可以看出，要想将sf和sfweibo进行连接，需要对sf及sf微博中的"省份名"
# 但是，由于sf_weibo中的省份名是不完整的，已知名称中肯定包含省份中的前面两个字，为此，需要对两个表格切割后，
# 进行连接

sf[u'省份前两字'] = np.nan
for i in range(len(sf[u'省份名'])):
    sf[u'省份前两字'][i] = sf[u'省份名'][i][:2]

sf_weibo[u'省份前两字'] = np.nan
for i in range(len(sf_weibo[u'省份名'])):
    sf_weibo[u'省份前两字'][i] = sf_weibo[u'省份名'][i][:2]

# 保存数据
sf_save = sf
sf_weibo_save =sf_weibo

#------------------------------------------------------------

# 连接两表
sf_sf_weibo = sf.merge(sf_weibo,on=u'省份前两字')

# 获取连接后表格中需要的字段名，并重新排列
sf_sf_weibo_one = sf_sf_weibo.iloc[:,[4,1,2]]

# 保存数据
sf_sf_weibo_one_save = sf_sf_weibo_one

#------------------------------------------------------------
# 连接sf_sf_weibo和all_pivot两表
sf_sf_weibo = sf_sf_weibo_one
sf_sf_weibo_all_pivot = pd.merge(sf_sf_weibo, all_pivot, left_on=u'微博用户名',right_on=u'用户名',right_index=True)

# 保存数据
sf_sf_weibo_all_pivot_save = sf_sf_weibo_all_pivot

#------------------------------------------------------------

# 处理爬取的用户的基本信息表base_info
base = weibo_xlsx.parse('base_info')

# 将base表与sf_sf_weibo_all_pivot进行连接
sf_sf_weibo_all_pivot_base = base.merge(sf_sf_weibo_all_pivot,left_on=u'昵称',right_on=u'微博用户名')
# 名称太长，换个名称
ssapb = sf_sf_weibo_all_pivot_base

# 替换某列的名字
ssapb.rename(columns={u'当月总微博数_x':u'当月总微博数'},inplace=True)

# 删除其中的多余列
ssapb = ssapb.drop([u'昵称',u'当月总微博数_y'],axis=1)

# 添加一列
ssapb[u'当月原创数'] = ssapb[u'当月总微博数'] - ssapb[u'当月转发数']

# 将某列同时与某字段字符串连接，通过观察网页可以发现这是网址的特点
linkfix = "?is_ori=1&is_forward=1&is_text=1&is_pic=1&is_video=1&is_music=1&is_\
article=1&key_word=&start_time=2017-05-01&end_time=2017-05-31&is_search=1&is_searchadv=1#_0"
ssapb[u'当月博文网址'] = ssapb[u'主页链接'] + linkfix

allfix = "?profile_ftype=1&is_all=1#_0"
ssapb[u'全部博文网址'] = ssapb[u'主页链接'] + allfix

# 计算出篇均转发、点赞、评论，并添加列
ssapb[u'篇均点赞'] = ssapb[u'点赞数']/ssapb[u'当月总微博数']
ssapb[u'篇均转发'] = ssapb[u'转发数']/ssapb[u'当月总微博数']
ssapb[u'篇均评论'] = ssapb[u'评论数']/ssapb[u'当月总微博数']

# 保存数据
ssapb_save = ssapb

# ---------------------------------------------------------
# 计算h值
# 将all表分组，获取表格的index值
gb = all.groupby(u'用户名')
gb_one = gb.size()
gb_index = gb_one.index

# 根据h指数的定义，分别计算转发、评论、点赞h指数
# 再记录下每个"用户名的最大互动度max(转发+评论+点赞)"
sort_all_f = all.sort_values(by=[u'用户名',u'转发数'],ascending=[True,False])
sort_all_c = all.sort_values(by=[u'用户名',u'评论数'],ascending=[True,False])
sort_all = all.sort_values(by=[u'用户名',u'点赞数'],ascending=[True,False])

m_m = (sort_all_f,sort_all_c,sort_all)

# 将计算得到的结果重新存储到一个新的DataFrame中
all_h = pd.DataFrame(np.arange(136).reshape(34,4),columns=['fh','ch','lh','max_hdd'],index=gb_index)
fh = []
ch = []
lh = []
max_hdd = []

for j in range(len(m_m)):
    for i in gb_index:
        tem_df = m_m[j][m_m[j][u'用户名']==i]
        tem_df['hdd'] = tem_df[u'转发数'] + tem_df[u'评论数'] + tem_df[u'点赞数']
        max_hdd.append(tem_df['hdd'].max())
        tem_df['numf'] = range(len(tem_df))
        if j == 0:
            a = len(tem_df[tem_df[u'转发数']>=tem_df['numf']+1])
            fh.append(a)
        elif j == 1:
            b = len(tem_df[tem_df[u'评论数']>=tem_df['numf']+1])
            ch.append(b)
        else:
            c = len(tem_df[tem_df[u'点赞数']>=tem_df['numf']+1])
            lh.append(c)

all_h['fh'] = fh
all_h['ch'] = ch
all_h['lh'] = lh

# 因为，前面的循环一共循环了三遍，使得all_h重复了3遍，因此只要获取前34位即可
all_h['max_hdd'] = max_hdd[:34]

# 插入一个综合h指数，该指数是转发、评论、点赞h指数三个的均值
all_h.insert(3,'HS',all_h.iloc[:,:3].mean(1))

# 更改列名称
all_h.rename(columns={'fh':u'转发h指数','ch':u'评论h指数',\
                      'lh':u'点赞h指数','HS':u'综合h指数','max_hdd':u'单篇最大互动度'},inplace=True)

# 连接ssapb和all_h
ssapb_all_h = pd.merge(ssapb, all_h, left_on=u'微博用户名',right_on=u'用户名',right_index=True)

# 加一列原创率
ssapb_all_h[u'原创率'] = ssapb_all_h[u'当月原创数']/ssapb_all_h[u'当月总微博数']

# 保存数据
ssapb_all_h_save = ssapb_all_h

# ----------------------------------------------------------------------------------

# 获取原DataFrame中的几列存储到新的DataFrame中，计算综合h指数与其他分
# 指数之间的相关性
f_one = ssapb_all_h.loc[:,[u'综合h指数',u'转发h指数',u'评论h指数',u'点赞h指数']]

# 计算f_one中各列数据的相关性
corr_one = f_one.corr()

# 保存数据
corr_one_save = corr_one

# -------------------------------------------------------------

# 获取原DataFrame中的列存储到新的DataFrame中，计算综合h指数与其他微博信息之间的相关性
f_two = ssapb_all_h.loc[:,[u'综合h指数',u'转发数',u'评论数',u'点赞数',u'篇均转发',u'篇均评论',u'篇均点赞']]
corr_two = f_two.corr()

# 保存数据
corr_two_save = corr_two
# -------------------------------------------------------------

# 获取原DataFrame中的几列存储到新的DataFrame中，计算综合指数h与其他信息之间的相关性
f_three = ssapb_all_h.loc[:,[u'综合h指数',u'原创率',u'粉丝数',u'微博总数',u'单篇最大互动度']]
corr_three = f_three.corr()

# 保存数据
corr_three_save = corr_three
#---------------------------------------------------------------------

# 重新排序
a_a = ssapb_all_h.iloc[:,[8,9,10,5,15,16,0,1,2,3,4,6,14,7,11,12,13,24,20,21,22,23,17,18,19,25]]

# 保存数据
a_a_save = a_a
#---------------------------------------------------------------------

# 将表中的浮点数类型保留至小数点后四位
f = lambda x:'%.4f' % x
a_a.ix[:,21:] = a_a.ix[:,21:].applymap(f)
a_a.ix[:,21:] = a_a.ix[:,21:].astype('float64')

# 将原创率转换成百分比形式
f1 = lambda x:'%.2f%%' % (x*100)
a_a[[u'原创率']] = a_a[[u'原创率']].applymap(f1)

a_a.sort_values(by=u'综合h指数',ascending=False,inplace=True)

# 按照综合h指数降序排序，添加一个排序位数
a_a['rank'] = np.arange(34) + 1

# 要想得到"综合h指数排名"的列，需要将a_a['rank']和a_a[u'综合h指数']进行合并成一列
# 这就要求必须连接字符串类型
a_a['rank'] = a_a['rank'].astype('str')
a_a[u'综合h指数'] = a_a[u'综合h指数'].astype('str')

# 连接成一列
# a_a[u'综合h指数/排名'] = a_a[u'综合h指数']+'/'+a_a['rank']
a_a[u'综合h指数/排名'] = a_a[u'综合h指数'] + '/' + a_a['rank']

# 删掉一列rank
del a_a['rank']

# 将该数据类型转换回来，换成浮点型
a_a[u'综合h指数'] = a_a[u'综合h指数'].astype('float64')

a_a.to_excel('finally.xlsx',index=False)