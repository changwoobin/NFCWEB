import pymysql

db = pymysql.connect(host='localhost',
                       user='pycontrol',
                       password='1vkdltjsM^^',
                       db='nfcproject',
                       charset='utf8')
cursor = db.cursor()
cursor.execute('SELECT * FROM user WHERE username = %s;',['woobin'])
result = cursor.fetchall()
print(result)
if len(result) == 0:
    print("비었다.")
db.close()