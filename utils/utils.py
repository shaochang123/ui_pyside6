import csv

#保存用户信息
def save_user_info(username,pwd):
    header = ['name','key']
    values = [{'name':username,'key':pwd}]
    with open('userInfo.csv','a',encoding='utf-8',newline='\n') as f:
        writer = csv.DictWriter(f,header)
        writer.writerows(values)
    pass
#获取用户名和密码
def get_user_info():
    #读取csv文件用户信息
    USERS = {}
    with open('userInfo.csv','r') as f:
        reader = csv.reader(f)
        #逐行遍历
        for row in reader:
            USERS[row[0]] = row[1]
    #返回
    return USERS
