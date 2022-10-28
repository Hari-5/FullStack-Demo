from flask import Flask, render_template, request, session

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
    return render_template('registration.html')

@app.route("/login")
def loginPage():
    return render_template('login.html')

@app.route("/success")
def successPage():
    return render_template('success.html',roll=session['roll1'],name=session['name1'])

@app.route("/collect",methods=['POST'])
def collectPage():
    r = request.form['roll']
    n = request.form['name']
    p = request.form['pass']

    resu = getDataFromDB(r,p)
    if resu:
        return render_template('registration.html', result="User Exists")
    else:
        storeData(n, r, p)
        return render_template('registration.html', result="Data Created")

    # print(r,n)
    # session['roll']=r
    # session['name']=n
    # session['pass']=p

    # result='Registration Success'
    # storeData(r,n,p)
    # return (render_template('registration.html',result=result))

@app.route("/compare",methods=['POST'])
def comparePage():
    r = request.form['roll1']
    p = request.form['pass1']
    # print(r,n)
    resu = getDataFromDB(r,p)
    if resu:
        k = resu[0]
        return render_template('success.html', result=k)
    else:
        k = "IN VALID"
        return render_template('login.html', result=k)

    # if r==session['roll'] and p==session['pass']:
    #     return (render_template('success.html'))
    # else:
    #     result="No data found"
    #     return (render_template('login.html',result=result))


# This is to retrieve and show the data that is present in database 
@app.route('/getdata', methods=['GET','POST'])
def getDataFromDB(rn,pwd):
    cur.execute("SELECT name FROM data WHERE rollno = %s AND password = %s",(rn,pwd))
    result=cur.fetchone()
    return result
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