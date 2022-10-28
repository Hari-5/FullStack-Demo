from flask import Flask, render_template, request, session

import mysql.connector as mysql

db=mysql.connect(
    host='localhost',
    user='root',
    password='root',
    database='db'
)

cur=ex.cursor()

app = Flask(__name__)
app.secret_key='har123'

@app.route("/")
def indexPage():
    return render_template('index.html')

@app.route("/admin")
def loginPage():
    return render_template('admin.html')

@app.route("/collect",methods=['POST'])
def collectPage():
    n = request.form['name']
    p = request.form['phoneno']
    t = request.form['time']

    result='Data Request Sent'
    storeData(n,p,t)
    return (render_template('index.html',res=result))

# This is to retrieve and show the data that is present in database 
@app.route('/getdata', methods=['GET','POST'])
def getDataFromDB():
    cur.execute("SELECT * FROM data")
    result=cur.fetchall()
    data=[]
    for i in result:
        data.append(i)
    for i in data:
        print(i)
    return render_template('admin.html',res=data)

@app.route('/collectcheck',methods=['GET','POST'])
def checkStatus():
    mob = request.form['mobile']
    print(mob)
    sql = ' SELECT * FROM SCHEDULE WHERE phoneno = %s '
    val = (mob,)
    cur.execute(sql,val)
    result = cursor.fetchone()
    if result:
        sql = "SELECT * FROM SCHEDULE WHERE phoneno = %s"
        val = (mob,)
        cur.execute(sql,val)
        r1 = cur.fetchone()
        stus = r1[3]
        at = r1[2]
        print(stus)
        if stus == "approved":
            return render_template('index.html', res2 = stus, res3="at", res4 = at)
        else:
            return render_template('index.html', res2 = stus)
    else:
        return render_template('index.html',res2 = "INVALID CREDITIONALS")

@app.route('/collectmob',methods=['POST']) #Collect the data(Handler)  
def collectData1():
    n = request.form['nom']
    st = request.form['stus']
    print(st)
    if st == 'approve':
        k = 'approved'
        sql = "UPDATE SCHEDULE SET status = %s WHERE mobile = %s"
        val = (k,n)
        cursor.execute(sql,val)
        db.commit()
        return render_template('admin.html',res1=k)
    elif st == 'reject':
        kn = 'rejected'
        sql = "UPDATE SCHEDULE SET status = %s WHERE MOBILE = %s"
        val = (kn,n)
        cursor.execute(sql,val)
        db.commit()
        return render_template('admin.html',res1=kn)
    elif st == "assign":
        dt = request.form['time']
        k = 'approved'
        sql = "UPDATE SCHEDULE SET status = %s WHERE mobile = %s"
        val = (k,n)
        cursor.execute(sql,val)
        db.commit()
        sql = "UPDATE SCHEDULE SET time  = %s WHERE MOBILE = %s"
        val = (dt,n)
        cursor.execute(sql,val)
        db.commit()
        return render_template('admin.html',res2 = k)

# This is to insert data in database that is entered in registration form   
def storeData(name,phoneno,time):
    sql='INSERT INTO data (name,phoneno,time) VALUES (%s,%s,%s)'
    val=(name,phoneno,time)
    cur.execute(sql,val)
    db.commit()

if __name__ == "__main__":
    app.run(debug=True)