from flask import Flask, render_template, request, redirect, session, abort
import hashlib
import connection_info

from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = connection_info.MyHost
app.config['MYSQL_USER'] = connection_info.MyUser
app.config['MYSQL_PASSWORD'] = connection_info.MyPassword
app.config['MYSQL_DB'] = connection_info.MyDatabase
mysql = MySQL(app)

if __name__ == "__main__":
	app.run(debug=True)

@app.route('/')
@app.route('/home')
def index():
	return render_template('index.html')

def set_login(username):
	session['logged_in'] = True
	session['username'] = username

@app.route('/login', methods=['POST'])
def login():
	cursor = mysql.connection.cursor()
	cursor.execute('SET TRANSACTION ISOLATION LEVEL READ COMMITTED')
	username = request.form.get('username')
	password = str(request.form.get('password')).encode()
	password = hashlib.sha256(password).hexdigest() # literally the least we can do
	cursor.execute('''SELECT * FROM Passenger WHERE Username = %s AND PasswordHash = %s''',(username, password))
	e = cursor.fetchone()
	to_ret = (e != None)
	if not to_ret:
		return render_template('login.html', msg_login='Incorrect Username/Password')
	cursor.close()

	set_login(username, e[1])
	return redirect('/')

@app.route('/register', methods=['POST'])
def register():
	cursor = mysql.connection.cursor()
	cursor.execute('SET TRANSACTION ISOLATION LEVEL READ COMMITTED')
	username = request.form.get('username')
	cursor.execute('''SELECT * FROM Passenger WHERE username = %s''',(username,))
	if (cursor.fetchone() != None):
		cursor.close()
		return {'success': False}

	firstname = request.form.get('firstname')
	lastname = request.form.get('lastname')
	password = str(request.form.get('password')).encode()
	password = hashlib.sha1(password).hexdigest() # literally the least we can do
	cursor.execute('''INSERT INTO Passenger VALUES (%s,%s,%s,%s);''',(username, firstname, lastname, password))
	mysql.connection.commit()
	cursor.close()

	# Log in the user on register
	set_login(username, firstname, lastname)
	# TODO redirect to user page
	return redirect('/')

@app.route('/login.html')
def login_page():
	if 'logged_in' in session and session['username'] != None:
		# Logging out
		session['logged_in'] = False
		session['username'] = None
		session['firstname'] = None
		session['lastname'] = None
		return redirect('/')
	# else
	return render_template('login.html')
