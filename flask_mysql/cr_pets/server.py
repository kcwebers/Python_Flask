from flask import Flask, render_template, request, redirect
from db import connectToMySQL    #import the function that will return an instance of a connection
app = Flask(__name__)

@app.route('/')
def index():
    mysql = connectToMySQL("Me_Pets")
    pets = mysql.query_db("SELECT * FROM pets;")
    print(pets)
    return render_template("pets.html", all_pets = pets)

@app.route("/add_pets", methods=["POST"])
def add_pet_to_db():
    mysql = connectToMySQL("Me_Pets")

    query = "INSERT INTO pets (name, type, created_at, updated_at) VALUES (%(nm)s, %(tp)s, NOW(), NOW());"
    data = {
        "nm": request.form["name"],
        "tp": request.form["type"]
    }
    new_pet_id = mysql.query_db(query, data)
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