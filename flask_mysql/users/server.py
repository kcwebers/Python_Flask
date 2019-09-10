from flask import Flask, render_template, request, redirect
from db import connectToMySQL    #import the function that will return an instance of a connection
app = Flask(__name__)

@app.route('/user')
def index():
    mysql = connectToMySQL("Users")
    users = mysql.query_db("SELECT * FROM user_info;")
    print(users)
    return render_template("index.html", all_users = users)

@app.route("/user/new")
def inputUserInfo():
    return render_template("new_user.html")

@app.route("/user/new", methods=["POST"])
def addUserInfo():
    mysql = connectToMySQL("Users")

    query = "INSERT INTO user_info (first_name, last_name, email, created_at, updated_at) VALUES (%(fn)s, %(ln)s, %(em)s, NOW(), NOW());"
    data = {
        "fn": request.form["first_name"],
        "ln": request.form["last_name"],
        "em": request.form["email"]
    }
    new_user_id = mysql.query_db(query, data)

    return redirect("/user/" + str(new_user_id))

@app.route("/user/<id>")
def addedInfo(id):
    mysql = connectToMySQL("Users")
    users = mysql.query_db("SELECT * FROM user_info WHERE id="+str(id)+";")
    return render_template("new_user_info.html", all_users = users)


@app.route("/user/<id>/edit")
def userToUpdate(id):
    mysql = connectToMySQL("Users")
    user = mysql.query_db("SELECT * FROM user_info WHERE id="+str(id)+";")
    return render_template("edit_user.html", user_info = user)

@app.route("/user/<id>/edit", methods=["POST"])
def updateUserInfo(id):
    mysql = connectToMySQL("Users")

    query = "UPDATE user_info SET first_name=%(fn)s, last_name=%(ln)s, email=%(em)s, updated_at=NOW() WHERE id="+str(id)+";"
    data = {
        "fn": request.form["first_name"],
        "ln": request.form["last_name"],
        "em": request.form["email"]
    }
    mysql.query_db(query, data)

    return redirect("/user/" + str(id))

@app.route("/user/<id>/delete")
def delete(id):
    mysql = connectToMySQL("Users")
    mysql.query_db("DELETE FROM user_info WHERE id="+str(id)+";")
    return redirect("/user")


if __name__ == "__main__":
    app.run(debug=True)
