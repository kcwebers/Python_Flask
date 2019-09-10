from flask import Flask, render_template, request, redirect, session, flash
from db import connectToMySQL 
app = Flask(__name__)

app.secret_key = "keep it secret"

@app.route('/')
def initial():
    mysql = connectToMySQL("dojo_survery")
    students = mysql.query_db("SELECT * FROM students;")
    print(students)
    return render_template("input.html", all_students = students)


@app.route('/', methods=['POST'])
def result():
    print(request.form)


    is_valid = True
    if len(request.form['name']) < 1:
        is_valid = False
        flash("Please enter valid name", "first")
    if 'location' not in request.form:
        is_valid = False
        flash("Please select a valid location", "second")
    if 'language' not in request.form:
        is_valid = False
        flash("Please select a valid language", "third")
    if len(request.form['comment']) > 120:
        is_valid = False
        flash("Cannot exceed 120 characters", "fourth")



    if not is_valid: # if any selection returns false
        return redirect("/")  
    else: # only if there are no 'flashes' will the code for adding person to database
        mysql = connectToMySQL("dojo_survery")

        query = "INSERT INTO students (name, location, language, comment) VALUES (%(name)s, %(loc)s, %(lang)s, %(comm)s);"
        data = {
            "name": request.form["name"],
            "loc": request.form["location"],
            "lang": request.form["language"],
            "comm": request.form["comment"]
        }
        new_student_id = mysql.query_db(query, data)

        return redirect("/result/" + str(new_student_id)) # return the reirect to new student input
    # if not go back to main page

@app.route("/result/<id>") # added id to help with direction of result
def addedInfo(id):
    flash("New Student Successfully Added!")

    mysql = connectToMySQL("dojo_survery")
    student = mysql.query_db("SELECT * FROM students WHERE id="+str(id)+";")
    return render_template("result.html", single_student = student)




if __name__ == "__main__":
    app.run(debug=True)