from flask import Flask, render_template, request, session

app = Flask(__name__)
app.secret_key='hari123'

@app.route("/")
def indexPage():
    return render_template('index.html')

@app.route("/about")
def aboutPage():
    return render_template('about.html',roll=session['roll'],name=session['name'])

@app.route("/navigation")
def navigationPage():
    return render_template('navigation.html')

@app.route("/collect",methods=['POST'])
def collectPage():
    r = request.form['roll']
    n = request.form['name']
    # print(r,n)
    session['roll']=r
    session['name']=n

    result='data collected'
    return (render_template('index.html',result=result))

    
if __name__ == "__main__":
    app.run(debug=True)