from flask import Flask, render_template, request, session, redirect

import mysql.connector as mysql

db=mysql.connect(
    host='localhost',
    user='root',
    password='root',
    database='db'
)

cur=db.cursor()

app = Flask(__name__)
app.secret_key='har123'

@app.route("/") # handlers
def registrationPage():
    return render_template('register.html')

@app.route("/login")
def loginPage():
    return render_template('login.html')

@app.route("/success")
def dashboardPage():
    if session['roll'] and session['pass']:
        print(session['roll'])
        print(session['pass'])
        return render_template('dashboard.html')
    else:
        return render_template('register.html')


@app.route("/collect",methods=['POST'])
def collectPage():
    r = request.form['roll']
    n = request.form['name']
    p = request.form['pass']

    session['roll']=r
    session['pass']=p

    resu = getDataFromDB(r,p)
    if resu:
        return render_template('register.html', result="User Exists")
    else:
        storeData(n, r, p)
        return render_template('register.html', result="Data Created")

@app.route("/compare",methods=['POST'])
def comparePage():
    r = request.form['roll1']
    p = request.form['pass1']
    # print(r,n)

    session['roll1']=r
    session['pass1']=p

    resu = getDataFromDB(r,p)
    if resu:
        cur.execute(" SELECT * FROM data ")
        result = cur.fetchall()
        # db.commit()
        data = []
        for i in result:
            data.append(i)
        return render_template('dashboard.html',res = data)
    else:
        k = "IN VALID"
        return render_template('login.html', result=k)

# This is to retrieve and show the data that is present in database 
@app.route('/getdata', methods=['GET','POST'])
def getDataFromDB(rn,pwd):
    cur.execute(" SELECT * FROM data")
    result = cur.fetchall()
    return result
    # data = []
    # for i in result:
    #     data.append(i)
    # for i in data:
    #     print(i)
    # return render_template('admin.html',res = data)

    # cur.execute("SELECT name FROM data WHERE rollno = %s AND password = %s",(rn,pwd))
    # result=cur.fetchone()
    # return result
    # data=[]
    # for i in result:
    #     data.append(i)
    # return (str(data))

# This is to insert data in database that is entered in registration form   
def storeData(name,rollno,password):
    sql='INSERT INTO data (name,rollno,password) VALUES (%s,%s,%s)'
    val=(name,rollno,password)
    cur.execute(sql,val)
    db.commit()


if __name__ == "__main__":
    app.run(debug=True)