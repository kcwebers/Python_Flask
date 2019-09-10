from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/dojo")
def dojo():
    return "Dojo!"

@app.route("/say/<name>")
def say(name):
    if type(name) is str:
        return f"Hi {name}!"

@app.route("/repeat/<num>/<word>")
def repeating(num, word):
    if type(word) is str and int(num) is int:
        return f"{word}" * int(num)

@app.errorhandler(404)
def pageNotFound(e):
    return "Sorry! No response. Try again."

if __name__ == "__main__":
    app.run(debug=True)


