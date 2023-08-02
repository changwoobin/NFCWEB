from flask import Flask, render_template, request, redirect, send_file
import sys
import os
import pymysql
from werkzeug.utils import secure_filename;
import hashlib
app = Flask(__name__)


def insert_info_db_user(name, password):
    db = pymysql.connect(host='localhost',
                       user='pycontrol',
                       password='1vkdltjsM^^',
                       db='nfcproject',
                       charset='utf8')
    cursor = db.cursor()
    os.mkdir('./files/'+name)
    cursor.execute('INSERT INTO user (username, password) VALUES (%s, %s);',[name, password])
    db.commit()
    db.close()
    
def insert_info_db_nfc(nfcname, nfcnum, userid):
    db = pymysql.connect(host='localhost',
                       user='pycontrol',
                       password='1vkdltjsM^^',
                       db='nfcproject',
                       charset='utf8')
    cursor = db.cursor()
    cursor.execute('SELECT * FROM nfc WHERE nfc_num=%s',[nfcnum])
    result = cursor.fetchall()
    if len(result) != 0:
        db.close()
    else:
        cursor.execute('INSERT INTO nfc (nfc_name, nfc_num, user_id) VALUES (%s, %s, %s);',[nfcname, nfcnum, userid])
        db.commit()
        db.close()

def update_info_db_nfc(nfcname, username, filename):
    db = pymysql.connect(host='localhost',
                       user='pycontrol',
                       password='1vkdltjsM^^',
                       db='nfcproject',
                       charset='utf8')
    cursor = db.cursor()
    cursor.execute('SELECT * FROM user WHERE username=%s',[username])
    result = cursor.fetchall()
    userid = result[0][0]
    cursor.execute('SELECT * FROM nfc WHERE nfc_name=%s AND user_id=%s',[nfcname, userid])
    result = cursor.fetchall()
    if result[0][3] != None:
        if os.path.isfile("./files/"+username+"/"+result[0][3]):
            os.remove("./files/"+username+"/"+result[0][3])
    cursor.execute('UPDATE nfc SET file=%s WHERE user_id=%s AND nfc_name=%s',[filename, userid, nfcname])
    db.commit()
    db.close()
    
        
def delete_db_nfc(nfcname, userid):
    db = pymysql.connect(host='localhost',
                       user='pycontrol',
                       password='1vkdltjsM^^',
                       db='nfcproject',
                       charset='utf8')
    cursor = db.cursor()
    cursor.execute('SELECT * FROM nfc LEFT JOIN user ON nfc.user_id = user.id WHERE nfc.nfc_name=%s AND nfc.user_id=%s;',[nfcname, userid])
    result = cursor.fetchall()
    if result[0][3] != None:
        if os.path.isfile("./files/"+result[0][6]+"/"+result[0][3]):
            os.remove("./files/"+result[0][6]+"/"+result[0][3])
    cursor.execute('DELETE FROM nfc WHERE nfc_name=%s AND user_id=%s',[nfcname, userid])
    db.commit()
    db.close()
    
def check_id(name):
    db = pymysql.connect(host='localhost',
                       user='pycontrol',
                       password='1vkdltjsM^^',
                       db='nfcproject',
                       charset='utf8')
    cursor = db.cursor()
    cursor.execute('SELECT * FROM user WHERE username = %s;',[name])
    result = cursor.fetchall()
    db.close()
    
    if len(result) == 0:
        return 0
    else:
        return 1
    
def check_account(name):
    db = pymysql.connect(host='localhost',
                       user='pycontrol',
                       password='1vkdltjsM^^',
                       db='nfcproject',
                       charset='utf8')
    cursor = db.cursor()
    cursor.execute('SELECT * FROM user WHERE username = %s;',[name])
    result = cursor.fetchall()
    db.close()
    
    return result[0]

def nfclist(name):
    db = pymysql.connect(host='localhost',
                       user='pycontrol',
                       password='1vkdltjsM^^',
                       db='nfcproject',
                       charset='utf8')
    cursor = db.cursor()
    cursor.execute('SELECT * FROM nfc LEFT JOIN user ON nfc.user_id = user.id WHERE user.username=%s;',[name])
    result = cursor.fetchall()
    db.close()
    
    return result

def search_id(id):
    db = pymysql.connect(host='localhost',
                       user='pycontrol',
                       password='1vkdltjsM^^',
                       db='nfcproject',
                       charset='utf8')
    cursor = db.cursor()
    cursor.execute('SELECT * FROM user WHERE id = %s;',[id])
    result = cursor.fetchall()
    db.close()
    
    return result[0]

def get_nfc_file_name(nfc_num):
    db = pymysql.connect(host='localhost',
                       user='pycontrol',
                       password='1vkdltjsM^^',
                       db='nfcproject',
                       charset='utf8')
    cursor = db.cursor()
    cursor.execute('SELECT * FROM nfc LEFT JOIN user ON nfc.user_id = user.id WHERE nfc.nfc_num=%s;',[nfc_num])
    result = cursor.fetchall()
    db.close()
    
    return result[0]




















@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/signin")
def signin():
    return render_template('signin.html')

@app.route("/signup")
def signup():
    return render_template('signup.html')

@app.route("/scan")
def scan():
    return render_template('scan.html')

@app.route("/mypagecreate", methods=['GET', 'POST'])
def createnfc():
    name = request.form['username']
    userid = check_account(name)
    
    return render_template('mypage_create.html',userid=userid[0]);

@app.route("/mypagedelete", methods=['GET', 'POST'])
def mypagedelete():
    username = request.form['username']
    
    return render_template("deletenfc.html", username=username)


@app.route("/mypageupdate", methods=['GET', 'POST'])
def mypageupdate():
    username = request.form['username']
    
    return render_template("updatenfc.html", username=username)

@app.route("/downloadnfc", methods=['GET', 'POST'])
def downloadnfc():
    nfcnum = request.form['nfcname']
    result = get_nfc_file_name(nfcnum)
    
    file_path = './files/'+result[6]+'/'+result[3]
    return send_file(file_path,as_attachment=True)
    
    
    
    


@app.route("/create", methods=['GET', 'POST'])
def create_account():
    name = request.form['name']
    password = request.form['password']
    m = hashlib.sha256()
    m.update(password.encode('utf-8'))
    hexpassword = m.hexdigest()
    result = check_id(name)
    
    if result == 0:
        insert_info_db_user(name, hexpassword)
    
        return redirect('https://file-with-nfc-chzci.run.goorm.site/signin')
    else:
        return redirect('https://file-with-nfc-chzci.run.goorm.site/signup')
    
@app.route("/check", methods=['GET', 'POST'])
def check():
    name = request.form['name']
    password = request.form['password']
    m = hashlib.sha256()
    m.update(password.encode('utf-8'))
    hexpassword = m.hexdigest()
    
    result = check_account(name)
    
    if result[2] == hexpassword:
        nfcnames = nfclist(name)
        if len(nfcnames) == 0:
            return render_template('mypage.html', name=name, nfcnamelist=["비어있습니다."])
        else:
            nfcnamelist = []
            for nfcname in nfcnames:
                nfcnamelist.insert(0, nfcname[1])
            return render_template('mypage.html', name=name, nfcnamelist=nfcnamelist)
            
    else:
        return redirect('https://file-with-nfc-chzci.run.goorm.site/signin')


@app.route("/createnfc", methods=['GET', 'POST'])
def insertnfc():
    nfcname = request.form['nfcname']
    nfcnum = request.form['nfcnum']
    userid = request.form['senduserid']
    
    insert_info_db_nfc(nfcname, nfcnum, userid)
    result = search_id(userid)
    nfcnames = nfclist(result[1])
    if len(nfcnames) == 0:
        return render_template('mypage.html', name=result[1], nfcnamelist=["비어있습니다."])
    else:
        nfcnamelist = []
        for nfcname in nfcnames:
            nfcnamelist.insert(0, nfcname[1])
        return render_template('mypage.html', name=result[1], nfcnamelist=nfcnamelist)

@app.route("/deletenfc", methods=['GET', 'POST'])
def deletenfc():
    nfcname = request.form['nfcname']
    username = request.form['username']
    
    result = check_account(username)
    userid = result[0]
    delete_db_nfc(nfcname, userid)
    nfcnames = nfclist(username)
    if len(nfcnames) == 0:
        return render_template('mypage.html', name=username, nfcnamelist=["비어있습니다."])
    else:
        nfcnamelist = []
        for nfcname in nfcnames:
            nfcnamelist.insert(0, nfcname[1])
        return render_template('mypage.html', name=username, nfcnamelist=nfcnamelist)
    
@app.route("/updatenfc", methods=['GET', 'POST'])
def updatenfc():
    nfcname = request.form['nfcname']
    username = request.form['username']
    nfcfile = request.files['file']
    
    update_info_db_nfc(nfcname, username, secure_filename(nfcfile.filename))
    

    nfcfile.save("./files/"+username+"/"+secure_filename(nfcfile.filename))
    
    nfcnames = nfclist(username)
    if len(nfcnames) == 0:
        return render_template('mypage.html', name=username, nfcnamelist=["비어있습니다."])
    else:
        nfcnamelist = []
        for nfcname in nfcnames:
            nfcnamelist.insert(0, nfcname[1])
        return render_template('mypage.html', name=username, nfcnamelist=nfcnamelist)
    

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(sys.argv[1]))
