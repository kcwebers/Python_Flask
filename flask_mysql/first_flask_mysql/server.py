from flask import Flask, render_template, request, redirect
from db import connectToMySQL    #import the function that will return an instance of a connection
app = Flask(__name__)

@app.route('/')
def index():
    mysql = connectToMySQL("first_flask")
    friends = mysql.query_db("SELECT * FROM friends;")
    print(friends)
    return render_template("index.html", all_friends = friends)

@app.route("/create_friend", methods=["POST"])
def add_friend_to_db():

    # SQL Injection
    mysql = connectToMySQL("first_flask")

    query = "INSERT INTO friends (first_name, last_name, occupation, created_at, updated_at) VALUES (%(fn)s, %(ln)s, %(occup)s, NOW(), NOW());"
    data = {
        "fn": request.form["fname"],
        "ln": request.form["lname"],
        "occup": request.form["occ"]
    }
    new_friend_id = mysql.query_db(query, data)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)

# query = "UPDATE friends SET first_name=%(fn)s WHERE id=%(id_num)s;" #query string - "INSERT INTO ..." - the string that will eventually be executed on our MySQL server
# data = { #data dictionary - the values that will be interpolated into the query string
#     "fn": # possibly a value from a form,    
#     "id_num": # possibly a value from the url,
#     # data dictionary keys - fn, id_num - the keys of the data dictionary used in the query string with %-interpolation
# }
# mysql.query_db(query, data)  #connection to the db - mysql - the instance of the MySQLConnection class