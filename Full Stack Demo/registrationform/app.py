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

@app.route("/")
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
    # print(r,n)
    session['roll']=r
    session['name']=n
    session['pass']=p

    result='Registration Success'
    storeData(r,n,p)
    return (render_template('registration.html',result=result))

@app.route("/compare",methods=['POST'])
def comparePage():
    r = request.form['roll1']
    p = request.form['pass1']
    # print(r,n)
    if r==session['roll'] and p==session['pass']:
        return (render_template('success.html'))
    else:
        result="No data found"
        return (render_template('login.html',result=result))


# This is to retrieve and show the data that is present in database 
@app.route('/getdata', methods=['GET','POST'])
def getDataFromDB():
    cur.execute("SELECT * FROM data")
    result=cur.fetchall()
    data=[]
    for i in result:
        data.append(i)
    return (str(data))

# This is to insert data in database that is entered in registration form   
def storeData(name,rollno,password):
    sql='INSERT INTO data (name,rollno,password) VALUES (%s,%s,%s)'
    val=(rollno,name,password)
    cur.execute(sql,val)
    db.commit()

if __name__ == "__main__":
    app.run(debug=True)