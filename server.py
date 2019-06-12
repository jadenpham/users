from flask import Flask, render_template, request, redirect
from mysqlconnection import connectToMySQL

app = Flask(__name__)

@app.route('/')
def index():
    mysql= connectToMySQL('first_flask_mysql')
    friends= mysql.query_db("SELECT * FROM friends;")
    return render_template("index.html")

@app.route('/user/new', methods=["POST"])
def create_user():
    query="INSERT INTO friends (first_name, last_name, email, created_at, updated_at) VALUE (%(fname)s, %(lname)s, %(email)s, NOW(), NOW());"
    data ={
        "fname": request.form["fname"],
        "lname": request.form["lname"],
        "email": request.form["email"]
    }

    db=connectToMySQL("first_flask_mysql")
    id = db.query_db(query, data)
    return redirect('/users/'+str(id))

@app.route('/users/<int:id>')
def show(id):
    mysql = connectToMySQL("first_flask_mysql")
    friends= mysql.query_db("SELECT * FROM friends;")
    return render_template("/show.html",friends=friends, userid=id-1)

if __name__=="__main__":
    app.run(debug=True)