from flask import Flask, render_template
app = Flask(__name__)
# our index route will handle rendering our form
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/left')
def wentLeft():
    return render_template("first.html")

@app.route('/right')
def wentRight():
    return render_template("second.html")
    
@app.route('/left/bridge')
def wentBridge():
    return render_template("bridge.html")

    
@app.route('/left/river')
def wentRiver():
    return render_template("river.html")

@app.route('/left/plane')
def wentPlane():
    return render_template("plane.html")

@app.route('/left/balloon')
def wentBalloon():
    return render_template("balloon.html")

@app.route('/right/balloon/death')
@app.route('/right/plane/death')
@app.route('/left/bridge/death')
@app.route('/left/river/death')
def wentDeath():
    return render_template("death.html")

@app.route('/right/balloon/survived')
@app.route('/right/plane/survived')
@app.route('/left/bridge/survived')
@app.route('/left/river/survived')
def wentSurvived():
    return render_template("survived.html")

if __name__ == "__main__":
    app.run(debug=True)
