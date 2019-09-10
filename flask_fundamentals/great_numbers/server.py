from flask import Flask, render_template, request, redirect, session
import random 	                # import the random module
 
app = Flask(__name__) 
app.secret_key = "keep it secret"

number = random.randint(1, 100)
print(number)

@app.route('/')         
def index():   
    return render_template("great_number.html")

@app.route('/submit', methods=['POST'])
def youPick():
    if 'count' in session:
        session['count'] = session.get('count') + 1
    else:
        session['count'] = 1

    if session['count'] >= 5:
        return render_template("loser.html")

    if int(request.form['your_input']) < number:
        return render_template("loser_low.html")
    elif int(request.form['your_input']) > number:
        return render_template("loser_high.html")
    elif int(request.form['your_input']) == number:
        return render_template("winner.html", random = number)

@app.route('/again', methods=['POST'])
def winner():
    global number
    number = random.randint(1, 100)
    print(number)
    session.clear()
    return redirect("/")

if __name__=="__main__":   
    app.run(debug=True)  