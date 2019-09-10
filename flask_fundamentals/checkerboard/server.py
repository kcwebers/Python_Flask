from flask import Flask, render_template, send_from_directory
app = Flask(__name__)

@app.route('/')
def originalCheckerboard():
    return render_template("index.html", times = 8, width = 8, color1 = 'red', color0 = 'black')

@app.route('/<num>')
def repeat(num):
    return render_template("index.html", times = int(num), width = 8, color1 = 'red', color0 = 'black')

@app.route('/<num>/<num2>')
def rowsNColumns(num, num2):
    return render_template("index.html", times = int(num), width = int(num2), color1 = 'red', color0 = 'black')

@app.route('/<num>/<num2>/<color1>/<color0>')
def changeAll(num, num2, color1, color0):
    return render_template("index.html", times = int(num), width = int(num2), color1 = color1, color0 = color0) 


if __name__ == "__main__":
    app.run(debug=True)