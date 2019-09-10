# from flask import Flask  # Import Flask to allow us to create our app
# app = Flask(__name__)    # Create a new instance of the Flask class called "app"
# @app.route('/')          # The "@" decorator associates this route with the function immediately following
# def hello_world():
#     return 'Hello World!'  # Return the string 'Hello World!' as a response
# # if __name__=="__main__":   # Ensure this file is being run directly and not from a different module    
# #     app.run(debug=True)    # Run the app in debug mode.

# from flask import Flask, render_template  # added render_template!
# app = Flask(__name__)                     
    
# @app.route('/')                           
# def hello_world():
#     # Instead of returning a string, 
#     # we'll return the result of the render_template method, passing in the name of our HTML file
#     return render_template('index.html')  
    
# if __name__=="__main__":
#     app.run(debug=True)  

from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html", phrase="hello", times=5)	# notice the 2 new named arguments!

@app.route('/lists')
def render_lists():
    # Soon enough, we'll get data from a database, but for now, we're hard coding data
    student_info = [
       {'name' : 'Michael', 'age' : 35},
       {'name' : 'John', 'age' : 30 },
       {'name' : 'Mark', 'age' : 25},
       {'name' : 'KB', 'age' : 27}
    ]
    return render_template("lists.html", random_numbers = [3,1,5], students = student_info)


if __name__=="__main__":
    app.run(debug=True)
