from flask import Flask, render_template, request, redirect
app = Flask(__name__)

@app.route('/')
def initial():
    return render_template("input.html")

@app.route('/result', methods=['POST'])
def result():

    # comment = request.form['comment']
    return render_template("result.html", name=request.form['name'], location=request.form['location'], language=request.form['language'], comment=request.form['comment'], happy=request.form['happy'])




if __name__ == "__main__":
    app.run(debug=True)