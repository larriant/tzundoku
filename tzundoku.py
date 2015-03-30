from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html') 

@app.route("/login", methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
	if request.form['submit'] == "Login":
	    if request.form['username'] != 'admin' or request.form['password'] != 'password':
	        error = 'Invalid Credentials. Please try again.'
	    else:
	        return redirect(url_for('overview'))
    return render_template('login.html', error=error)

@app.route("/register")
def register():
    return render_template('register.html')

@app.route("/logout")
def logout():
    return render_template('logout.html')

@app.route("/overview")
def overview():
    return render_template('overview.html')

if __name__ == "__main__":
    app.run()


