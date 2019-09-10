from flask import Flask, render_template, request, redirect, session, flash
from db import connectToMySQL 
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

app = Flask(__name__)

app.secret_key = "keep it secret"

@app.route('/')
def login():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def addEmail():
    if not EMAIL_REGEX.match(request.form['email']) or len(request.form['email']) < 1:
        flash("Email is not valid!", "first")
        flash("Please enter a valid email address", "second")
        return redirect('/')

    else: # if email already exists in database, flash different message
        mysql = connectToMySQL("emails")
        query = "SELECT * FROM email_info WHERE email = %(email)s;"
        data = {
            "email": request.form["email"]
        }
        result = mysql.query_db(query, data)

        if result != ():
            flash("Email is not valid!", "first")
            flash("Email already exists, please enter new email", "second")
            return redirect('/')

        mysql = connectToMySQL("emails")
        query = "INSERT INTO email_info (email) VALUES (%(email)s);"
        data = {
            "email": request.form["email"]
        }
        new_email_id = mysql.query_db(query, data)
        new_email = request.form['email']

        flash("The email address you entered (" + new_email + ") is a VALID email addess! Thank you!", "success")
        return redirect("/success") # return the reirect to success page

@app.route('/success')
def success():
    mysql = connectToMySQL("emails")
    emails = mysql.query_db("SELECT * FROM email_info;")
    print(emails)
    return render_template('success.html', all_emails = emails)

@app.route("/success/delete/<id>")
def delete(id):
    mysql = connectToMySQL("emails")
    mysql.query_db("DELETE FROM email_info WHERE id="+str(id)+";")
    return redirect("/success")

if __name__ == "__main__":
    app.run(debug=True)