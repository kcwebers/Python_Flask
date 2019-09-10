from flask import Flask, render_template
app = Flask(__name__)
# our index route will handle rendering our 
@app.route('/')
def start():
    return "Hello There!"

@app.route('/play')
def index():
    return render_template("playground.html", times = 3, background_color = 'lightblue')

@app.route('/play/<num>')
def repeat(num):
    return render_template("playground.html", times = int(num), background_color = 'lightblue')

@app.route('/play/<num>/<color>')
def colorChange(num, color):
    return render_template("playground.html", times = int(num), background_color = color)


if __name__ == "__main__":
    app.run(debug=True)
