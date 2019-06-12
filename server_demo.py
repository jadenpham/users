from flask import Flask, render_template, request, redirect, url_for
from mysqlconnection import connectToMySQL

app = Flask(__name__)
@app.route('/users')
def index():
    mysql= connectToMySQL("first_flask_mysql")
    users = mysql.query_db('SELECT * FROM friends2')
    return render_template("index_demo.html", all_users=users)

@app.route('/users/new')
def new_user():
    return render_template("add_user_demo.html")


@app.route('/add_user', methods=['POST'])
def add_user():
    mysql = connectToMySQL("first_flask_mysql")
    query = "INSERT INTO friends2 (first_name, last_name, email) VALUES (%(fn)s, %(ln)s, %(email)s);"
    data = {
        "fn": request.form["fname"],
        "ln": request.form["lname"],
        "email": request.form["email"]
    }

    user_id = mysql.query_db(query, data)
    return redirect('/user/' + str(user_id))

@app.route("/user/<user_id>")
def show(user_id):
    mysql = connectToMySQL("first_flask_mysql")
    query = "SELECT * FROM friends2 WHERE id = %(id)s;"
    data = {
        'id' : user_id
    }
    user= mysql.query_db(query, data)
    return render_template('show_demo.html', users=user)


@app.route('/user/<user_id>/edit')
def show_edit(user_id):
    mysql = connectToMySQL("first_flask_mysql")
    query = "SELECT * FROM friends2 WHERE id = %(id)s;"
    data = {
        'id' : user_id
    }
    user= mysql.query_db(query, data)
    return render_template('edit_demo.html', user=user)

@app.route('/edit_user/<user_id>', methods=['POST'])
def update_user(user_id):
    mysql = connectToMySQL("first_flask_mysql")
    query = "UPDATE friends2 SET first_name = %(fn)s, last_name=%(ln)s, email=%(email)s WHERE id = %(id)s;"
    data = {
        "fn": request.form["fname"],
        "ln": request.form["lname"],
        "email": request.form["email"],
        "id": user_id
    }
    user= mysql.query_db(query, data)
    return render_template('edit_demo.html', user=user)

@app.route('/delete/<user_id>')
def delete(user_id):
    mysql = connectToMySQL("first_flask_mysql")
    query = "DELETE FROM friends2 WHERE ID = %(id)s;"
    data = {
        'id': user_id
    }
    mysql.query_db(query, data)
    return redirect('/users')

if __name__=="__main__":
    app.run(debug=True)