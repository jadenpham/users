from flask import Flask, render_template, request, redirect, url_for
from mysqlconnection import connectToMySQL

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index2.html")

@app.route('/users')
def all_users():
    mysql=connectToMySQL("first_flask_mysql")
    query= "SELECT * FROM friends"
    result=mysql.query_db(query)
    return render_template('/users.html')

@app.route('/users/new', methods=['POST', 'GET'])
def create_user():
    query="INSERT INTO friends (first_name, last_name, email, created_at, updated_at) VALUE (%(fname)s, %(lname)s, %(email)s, NOW(), NOW());"
    data ={
        "fname": request.form["fname"],
        "lname": request.form["lname"],
        "email": request.form["email"]
    }
    db=connectToMySQL("first_flask_mysql")
    user_id = db.query_db(query, data)
    return redirect (url_for('user_id', id=user_id))
    # return redirect('/users/'+str(user_id), user_id=user_id)
@app.route('/users/<id>')
def user_id(id):
    print("ID"+id)
    mysql=connectToMySQL('first_flask_mysql')
    query = f"SELECT * FROM friends WHERE id = {id}"
    result= mysql.query_db(query)
    return render_template('show.html',result=result)

@app.route('/users/<id>/edit', methods=['POST', 'GET'])
def show_user(id):
    mysql=connectToMySQL('first_flask_mysql')

    query = f"SELECT * FROM friends WHERE id = {id}"
    result= mysql.query_db(query)
    return render_template("/edit.html", result=result)

@app.route('/update', methods=['POST', 'GET'])
def update_user():
    db=connectToMySQL("first_flask_mysql")
    data ={
        "uf_name": request.form["update_fn"],
        "ul_name": request.form["update_ln"],
        "u_email": request.form["update_email"],
        "id"   : request.form['id']
    }
    query = "UPDATE friends SET first_name = %(uf_name)s, last_name= %(ul_name)s, email=%(u_email)s WHERE id = %(id)s;"
    user_id=db.query_db(query, data)
    print(user_id)
    return redirect (url_for('user_id', id=request.form['id']))


if __name__=="__main__":
    app.run(debug=True)