import csv
import pandas as pd
import xlrd
import numpy as np

'''
# 筛选出可能反映组织恐袭特征字段
header = ['eventid', 'iyear', 'imonth', 'iday', 'country', 'region', 'city', 'latitude', 'longitude', 'success',
          'gname', 'targtype1', 'targsubtype1', 'weaptype1', 'weapsubtype1', 'suicide', 'attacktype1', 
          'ishostkid', 'INT_LOG', 'INT_IDEO', 'INT_MISC', 'INT_ANY']
df = pd.read_csv(open('E:/data.csv', encoding='utf8'))
dfs = df[['eventid', 'iyear', 'imonth', 'iday', 'country', 'region', 'city', 'latitude', 'longitude', 'success',
          'gname', 'targtype1', 'targsubtype1', 'weaptype1', 'weapsubtype1', 'suicide', 'attacktype1',
          'ishostkid', 'INT_LOG', 'INT_IDEO', 'INT_MISC', 'INT_ANY']]
dfs.to_csv('E:/zuzhi.csv',index=False,header=header)
'''
'''
# 组织恐袭特征数据处理
df = pd.read_csv(open('E:/zuzhi.csv', encoding='utf8'))
df.replace(-9, 0.5, inplace=True)
dfs = df[['eventid','iyear','imonth', 'iday','country','region','latitude', 'longitude','success',
          'gname','targtype1','targsubtype1','weaptype1','weapsubtype1','suicide',
          'attacktype1','ishostkid','INT_LOG', 'INT_IDEO', 'INT_MISC', 'INT_ANY']]
df_city = pd.read_csv(open('E:/city.csv', encoding='utf8'))  # 将城市字段按第一问方式设置
city = df_city['city'].tolist()
f_sec = open('E:/著名城市.txt', encoding='utf8')
city_sec = []
for line in f_sec.readlines():
    city_sec.append(line.strip())
cc = xlrd.open_workbook('E:/国家名称包含首都名称.xls')
table = cc.sheets()[0]
nrows = table.nrows
data = []
for i in range(nrows):
    if i == 0:
        continue
    temp = table.row_values(i)[:]
    data.append(temp)
capital = []
for i in range(len(data)):
    capital.append(data[i][-1])
city_new = []
for i in range(len(city)):
    if city[i] in capital:
        city_new.append(3)
    elif city[i] in city_sec:
        city_new.append(2)
    else:
        city_new.append(1)
dataset = []
for i in range(len(dfs)):
    temp = dfs.loc[i][:]
    temp = temp.tolist()
    temp.append(city_new[i])
    dataset.append(temp)
dataset = np.array(dataset)
header = ['eventid','iyear','imonth', 'iday','country','region','latitude', 'longitude','success',
          'gname','targtype1','targsubtype1','weaptype1','weapsubtype1','suicide',
          'attacktype1','ishostkid','INT_LOG', 'INT_IDEO', 'INT_MISC', 'INT_ANY','city']
ddf = pd.DataFrame(dataset)
ddf.to_csv('E:/zuzhi2.csv', index= False, header=header)
# fa = ['卢森堡','挪威','瑞士','爱尔兰','丹麦','冰岛','瑞典','英国','奥地利','荷兰','芬兰','比利时','法国','德国',
#       '意大利','西班牙','希腊','葡萄牙','美国','加拿大','日本','新加坡','澳大利亚','新西兰','塞浦路斯','巴哈马',
#       '斯洛文尼亚','以色列','韩国','马耳他','匈牙利','捷克','波兰','斯洛伐克','安道尔','巴林','巴巴多斯','文莱',
#       '爱沙尼亚','中国香港','列支敦士登','摩纳哥','卡塔尔','圣马力诺','阿联酋']
# df = pd.read_csv(open('E:/country.csv', encoding='utf8'))
# country = df['country'].tolist()
# f_sec_country = open('E:/发展中国家.txt', encoding='utf8')
# country_sec = []
# for line in f_sec_country.readlines():
#     country_sec.append(line.strip())
# country_new = []
# for i in range(len(country)):
#     if country[i] in fa:
#         country_new.append(3)
#     elif country[i] in country_sec:
#         country_new.append(2)
#     else:
#         country_new.append(1)

'''
'''
df = pd.read_csv(open('E:/zuzhi2.csv',encoding='utf8'))
df.fillna(0, inplace=True)
df1 = df[~df['gname'].isin(['Unknown'])]
df2 = df1[df1['iyear'].isin([2015.0, 2016.0])]
gname = df2['gname'].tolist()
eventid = df2['eventid'].tolist()
name_zu = set(gname)
name_zu = list(name_zu) # 现已知组织未重复
gn_eve = [] # 事件id与组织对应
for i in range(len(gname)):
    gn_eve.append([gname[i], eventid[i]])
data = xlrd.open_workbook('E:/result_class.xlsx')
table = data.sheets()[0]
nrows = table.nrows
tt = []  # id对应等级
pos = 0
for i in range(nrows):
    if i == 0:
        continue
    temp = table.row_values(i)[:]
    for j in range(pos, len(eventid)):
        if temp[1] == eventid[j]:
            tt.append([temp[1], temp[0]])
            pos = j
            break
gn_lab = []
for i in range(len(gn_eve)):
    if gn_eve[i][1] == tt[i][0]:
        gn_lab.append([gn_eve[i][0],tt[i][1]])

zu_score = {} # 每个组织发起的恐袭事件数量统计
for i in range(len(name_zu)):
    sum = 0
    n = 0
    for j in range(len(gn_lab)):
        if name_zu[i] == gn_lab[j][0]:
            n += 1
            sum += gn_lab[j][1]
    zu_score[name_zu[i]] = sum/n

ss = sorted(zu_score.items(), key=lambda x: x[1], reverse=True)
print(ss)
print("危害性最高的五个组织或个人：")
num = 0
for i in range(len(ss)):
    if num < 5:
        print(ss[i][0])
        num += 1
'''
'''
# 15、16年相关案件分类
df = pd.read_csv(open('E:/zuzhi2.csv',encoding='utf8'))
df.fillna(0, inplace=True)
df1 = df[df['gname'].isin(['Unknown'])].reset_index(drop=True)
df1_year = df1[df1['iyear'].isin([2015.0, 2016.0])].reset_index(drop=True)
df1_year.drop(['gname', 'iyear'], axis=1, inplace=True)
unknown = [] # 未知作案者的恐袭特征
for i in range(len(df1_year)):
    temp = df1_year.loc[i][:]
    temp = temp.tolist()
    unknown.append(temp)
print(len(unknown[0]))

df2 = df[~df['gname'].isin(['Unknown'])].reset_index(drop=True)
df2_year = df2[df2['iyear'].isin([2015.0, 2016.0])].reset_index(drop=True)
df2.drop(['eventid', 'iyear'], axis=1, inplace=True)
gname = df2['gname'].tolist()
gname = set(gname)
gname_new = list(gname)
gname_fea = []
for i in range(len(df2)):
    temp = df2.loc[i][:]
    temp = temp.tolist()
    gname_fea.append(temp)
gname_mean = [] # 已知组织的特征
for i in range(len(gname_new)):
    content = []
    for j in range(len(gname_fea)):
        if gname_new[i] == gname_fea[j][7]:
            content.append(gname_fea[j][:7]+gname_fea[j][8:])
    contents = np.array(content)
    contents_mean = np.mean(contents, axis=0)
    s = contents_mean.tolist()
    print(type(s))
    gname_mean.append([gname_new[i]]+s)
print(len(gname_mean[0]))


def cos(vector1, vector2):  # 计算余弦相似度
    dot_product = 0.0
    normA = 0.0
    normB = 0.0
    for a,b in zip(vector1,vector2):
        dot_product += a*b
        normA += a**2
        normB += b**2
    if normA == 0.0 or normB == 0.0:
        return None
    else:
        return dot_product / ((normA*normB)**0.5)


unknown_cos = []
for i in range(len(unknown)):
    max = -2
    max_name = ''
    for j in range(len(gname_mean)):
        dis = cos(unknown[i][1:],gname_mean[j][1:])
        if dis > max:
            max = dis
            max_name = gname_mean[j][0]
    unknown_cos.append([unknown[i][0], max_name, max])
dfs = pd.DataFrame(unknown_cos, columns=['eventid', 'gname', 'max_similarity'])
dfs.to_excel('E:/15-16年未知作案者相关性分类.xlsx')
'''
'''
# 表2
name = ["Kata'ib Hezbollah", "Popular Front for the Renaissance of the Central African Republic (FPRC)",
        "United Front for Democracy Against Dictatorship", "Jundallah (Pakistan)", "Ansar al-Din Front"]
df = pd.read_csv(open('E:/zuzhi2.csv',encoding='utf8'))
df.fillna(0, inplace=True)
gname = []
for i in range(len(df)):
    temp = df.loc[i][:]
    temp = temp.tolist()
    gname.append(temp)
gname_mean = []
for i in range(len(name)):
    content = []
    n = 0
    for j in range(len(gname)):
        if name[i] == gname[j][9]:
            n += 1
            content.append(gname[j][2:9]+gname[j][10:])
    contents = np.array(content)
    contents_mean = np.mean(contents, axis=0)
    s = contents_mean.tolist()
    print(type(s))
    gname_mean.append([name[i]] + s)
print(len(gname_mean[0]))

df1_year = df[df['iyear'].isin([2017.0])].reset_index(drop=True)
df1_year.drop(['gname', 'iyear'], axis=1, inplace=True)
l = [201701090031, 201702210037, 201703120023, 201705050009, 201705050010, 201707010028, 201707020006, 201708110018,
     201711010006, 201712010003]
eve = []
for i in range(len(df1_year)):
    temp = df1_year.loc[i][:]
    temp = temp.tolist()
    if int(temp[0]) in l:
        eve.append(temp)
print(len(eve[0]))


def cos(vector1, vector2):  # 计算余弦相似度
    dot_product = 0.0
    normA = 0.0
    normB = 0.0
    for a,b in zip(vector1,vector2):
        dot_product += a*b
        normA += a**2
        normB += b**2
    if normA == 0.0 or normB == 0.0:
        return None
    else:
        return dot_product / ((normA*normB)**0.5)

result = []
for i in range(len(eve)):
    temp = []
    temp.append(eve[i][0])
    for j in range(len(gname_mean)):
        dis = cos(eve[i][1:], gname_mean[j][1:])
        temp.append((gname_mean[j][0], dis))
    result.append(temp)
for i in range(len(result)):
    print("针对恐袭事件",result[i][0],":")
    print(result[i][1][0],"的嫌疑度为：",result[i][1][1])
    print(result[i][2][0], "的嫌疑度为：", result[i][2][1])
    print(result[i][3][0], "的嫌疑度为：", result[i][3][1])
    print(result[i][4][0], "的嫌疑度为：", result[i][4][1])
    print(result[i][5][0], "的嫌疑度为：", result[i][5][1])
'''
