from flask import Flask, render_template, request, redirect,session

app = Flask(__name__)
app.secret_key = "keep it secret"

@app.route('/')         
def counter():
    if 'total' in session:
        session['total'] = session.get('total') + 1
    else:
        session['total'] = 1
    return render_template("counter.html")

@app.route('/add_two')
def addTwo():
    if 'total' in session:
        session['total'] = session.get('total') + 1
    return redirect("/")

@app.route('/reset')
def reset():
    if 'total' in session:
        session['total'] = 0
    return redirect("/")

@app.route('/destroy_session')         
def destroy():
    session.clear()
    return redirect("/")

@app.route('/your_increment', methods=['POST'])
def youPick():
    session['total'] = session.get('total') + int(request.form['your_input']) - 1
    return redirect("/")

if __name__=="__main__":   
    app.run(debug=True)  
