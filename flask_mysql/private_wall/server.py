from flask import Flask, render_template, request, redirect, session, flash
from db import connectToMySQL 
import re
from flask_bcrypt import Bcrypt
from datetime import datetime

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASS_REGEX = re.compile(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,15}$')
# Password matching expression. Password must be at least 8 characters, no more than 8 characters, and must include at least one upper case letter, one lower case letter, and one numeric digit.

app = Flask(__name__)

bcrypt = Bcrypt(app)

app.secret_key = "keep it secret"

@app.route('/')
def login():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def isValid():
    is_valid=True

    if len(request.form['fname']) < 1: # validate name
        is_valid=False
        flash("First name must be more than one letter and contain only letters", "first")
    
    if len(request.form['lname']) < 1: # validate last name
        is_valid=False
        flash("Last name must be more than one letter and contain only letters", "second")
    
    if not EMAIL_REGEX.match(request.form['email']) or len(request.form['email']) < 1: # validate email against regex
        is_valid=False
        flash("Invalid email address", "third")

    if not PASS_REGEX.match(request.form['password']): # validate password against regex
        is_valid=False
        flash("Password must be at least 8 characters, no more than 15 characters, and must include at least one upper case letter, one lower case letter, and one numeric digit", "fourth")

    if request.form['password'] != request.form['conf_pass']: # if password doesn't matcht he confirm field
        is_valid=False
        flash("Passwords do not match", "fifth")

    else: # if email already exists in database, flash different message
        mysql = connectToMySQL("user_schema")
        query = "SELECT * FROM users WHERE email = %(email)s;"
        data = {
            "email": request.form["email"]
        }
        result = mysql.query_db(query, data)

        if result != (): # if email exists in database, request new
            is_true=False
            flash("Email already exists, please enter new email", "third")
            return redirect('/')

    if not is_valid: # if any selection returns false
        return redirect("/")  # redirect with flash messages

    else:
        pw_hash = bcrypt.generate_password_hash(request.form['password']) # declare new variable to store a hashed password
        print(pw_hash)

        mysql = connectToMySQL("user_schema")
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(fn)s, %(ln)s, %(em)s, %(pass_hash)s);"
        data = {
            "fn": request.form["fname"],
            "ln": request.form["lname"],
            "em": request.form["email"],
            "pass_hash": pw_hash
        }
        new_user_id = mysql.query_db(query, data)
        session['name'] = request.form['fname']
        session['id'] = new_user_id

        flash("You have successfully registered! Welcome " + session['name'] +"!", "success")
        return redirect("/wall")

@app.route('/login', methods=['POST'])
def validLogin():
    is_valid=True

    if not EMAIL_REGEX.match(request.form['email_input']) or len(request.form['email_input']) < 1:
        is_valid=False
        flash("Invalid email address", "sixth")

    if len(request.form['password_input']) < 1:
        is_valid=False
        flash("Please enter password", "seventh")

    if not is_valid: # if any selection returns false
        flash("Login failed, please try again", "fail")
        return redirect("/")  # redirect with flash messages

    else:
        mysql = connectToMySQL("user_schema")
        query = "SELECT * FROM users WHERE email = %(email)s;"
        data = {
            "email": request.form["email_input"]
        }
        result = mysql.query_db(query, data)

        if len(result) < 1:
            flash("Email does not exist, please register for account", "sixth")
            return redirect("/")  # redirect with flash messages

        else: 
            if bcrypt.check_password_hash(result[0]['password'],request.form['password_input']): # check password input vs. stored hashed value
                session['id'] = result[0]['id']
                session['name'] = result[0]['first_name']
                flash("Welcome back " + session['name'] +"!", "success")
                return redirect('/wall')
            else:
                flash("Incorrect password", "seventh")
                return redirect('/')
    
@app.route('/wall')
def success():
    if 'id' not in session:
        flash("Login failed, please try again", "fail")
        return redirect("/")
    else:
        id = session['id']
        mysql = connectToMySQL("user_schema")
        query1 = "SELECT *, TIME_TO_SEC(TIMEDIFF(messages.created_at, NOW())) as time_diff FROM users LEFT JOIN messages ON messages.users_id = users.id WHERE recipients_id = " + str(id) + ";"
        all_info = mysql.query_db(query1)
        print(all_info)

        mysql = connectToMySQL("user_schema")
        query2 = "SELECT * FROM users WHERE id NOT IN ("+ str(id) + ");"
        all_other_info = mysql.query_db(query2)

        mysql = connectToMySQL("user_schema")
        query3 = "SELECT COUNT(*) as count FROM users LEFT JOIN messages ON messages.users_id = users.id WHERE recipients_id = " + str(id) + " GROUP BY recipients_id;"
        got_count = mysql.query_db(query3)
        print(got_count) # how many people have sent to this user

        mysql = connectToMySQL("user_schema")
        query4 = "SELECT COUNT(*) as count FROM users LEFT JOIN messages ON messages.users_id = users.id WHERE users.id = " + str(id) + " GROUP BY users.id;"
        sent_count = mysql.query_db(query4)
        print(sent_count) # what are we retrieving? how many msg sent


        return render_template('welcome.html', 
        all_info = all_info, 
        all_else = all_other_info, 
        got_count = got_count, 
        sent_count = sent_count)

@app.route('/send', methods=['POST'])
def sendMessage():
    is_valid=True

    if len(request.form['msg']) < 1:
        is_valid=False
        flash("Please enter message to send", "m1")
    elif len(request.form['msg']) > 225:
        is_valid=False
        flash("Message cannot exceed 225 characters", "m1")
    
    if not is_valid:
        return redirect('/wall')

    else:
        mysql = connectToMySQL("user_schema")
        query = "INSERT INTO messages (users_id, recipients_id, content) VALUES (%(sender)s, %(reciever)s, %(msg)s);"
        data = {
            'msg': request.form['msg'],
            'reciever': request.form['reciever'],
            'sender': request.form['sender']
        }
        new_user_id = mysql.query_db(query, data)

        flash("Message sent!", "m1")
        return redirect('/wall')

@app.route('/delete_message/<id>')
def delete(id):
    mysql = connectToMySQL("user_schema")
    query = "DELETE FROM messages WHERE messages.id=" + str(id)+ ";"
    delete = mysql.query_db(query)

    flash("Message deleted", "deleted")
    return redirect("/wall")

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/') 


if __name__ == "__main__":
    app.run(debug=True)