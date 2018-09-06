from flask import Flask, render_template, url_for, flash, redirect, session
from forms import RegistrationForm, LoginForm
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'b4ae2746c5fead2b9a233adeefe93e63'
app.secret_key = b'_5#y2L"F4Q8z]/'

@app.route("/")
@app.route("/home")
def home():
    if 'username' in session:
        return redirect(url_for('profile', username=session['username']))
    return render_template('home.html', title="Home")

@app.route("/profile/<username>")
def profile(username):
    if 'username' in session:
        if session['username'] == username:
            conn = sqlite3.connect('aw.db')
            cursor = conn.cursor()
            query = "select datetime from loginhistory where username = ?"
            lst=[username]
            cursor.execute(query,lst)
            timestamps = list(sum(cursor.fetchall(), ()))
            conn.commit()
            conn.close()
            return render_template('profile.html', username=username, timestamps=timestamps)
        else:
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        conn = sqlite3.connect('aw.db')
        cursor = conn.cursor()
        query = "select count(*) from users where username = ? and password = ?"
        lst=[form.username.data, form.password.data]
        cursor.execute(query,lst)
        if cursor.fetchone()[0]==1:
            session['username'] = form.username.data
            dt = 'NOW'
            insertquery = "insert into loginhistory values (datetime(?),?)"
            insertlst = [dt, form.username.data]
            conn.execute(insertquery, insertlst)
            conn.commit()
            conn.close()
            flash(f'You have been logged in!', 'success')
            return redirect(url_for('profile', username=form.username.data))
        else:
            flash('Login Unsuccessful. Please check your username and password', 'danger')
    return render_template('login.html', title="Login", form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            conn = sqlite3.connect('aw.db')
            query = "insert into users values (?,?)"
            lst = [form.username.data, form.password.data]
            conn.execute(query,lst)
            conn.commit()
            conn.close()
            flash(f'Account created for {form.username.data}!', 'success')
            return redirect(url_for('login'))
        except:
            flash(f'Account already exists for {form.username.data}!', 'danger')
    return render_template('register.html', title="Register", form=form)

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route("/stackoverflow")
def stackoverflow():
    if 'username' in session:
        return render_template('stackoverflow.html')
    return redirect(url_for('home'))

@app.route("/visualizations")
def visualizations():
    if 'username' in session:
        return render_template('visualizations.html')
    return redirect(url_for('home'))

@app.route("/profilerouting")
def profilerouting():
    if 'username' in session:
        return redirect(url_for('profile', username=session['username']))
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)