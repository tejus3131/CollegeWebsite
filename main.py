from flask import Flask, render_template, session, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///MIET_Notes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Issue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), unique=False, nullable=False)
    last_name = db.Column(db.String(20), unique=False, nullable=False)
    email = db.Column(db.String(50), unique=False, nullable=False)
    issue = db.Column(db.String(500), unique=False, nullable=False)

    def __repr__(self):
        return f"first_name : {self.first_name}, last_name : {self.first_name}, email : {self.email}, issue: {self.issue}"


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), unique=False, nullable=False)
    last_name = db.Column(db.String(20), unique=False, nullable=False)
    email = db.Column(db.String(50), unique=False, nullable=False)
    password = db.Column(db.String(500), unique=False, nullable=False)
    status = db.Column(db.Integer, unique=False, nullable=False)

    def __repr__(self):
        return f"first_name : {self.first_name}, last_name : {self.first_name}, email : {self.email}, password: {self.password}, status: {self.status}"


@app.route("/")
def index():
    if session.get('logged_in'):
        return render_template("index.html", status=True, )
    else:
        return render_template("index.html")


@app.route("/login_page")
def login_page():
    return render_template("login.html")


@app.route("/sign_up")
def sign_up():
    return render_template("sign_up.html")


@app.route('/login', methods=['POST'])
def do_admin_login():
    password = request.form['password']
    email = request.form['email']
    user = User.query.filter_by(email=email).first()
    if user is not None:
        if user.password == password:
            session['logged_in'] = True
            return index()
        else:
            flash("Incorrect Password")
            return redirect('/login_page')
    else:
        return redirect("/sign_up")


@app.route("/contact_us")
def contact_us():
    return render_template("contact_us.html")


@app.route('/add_issue', methods=["POST"])
def add_issue():
    first = request.form.get("fname")
    last = request.form.get("lname")
    useremail = request.form.get("email")
    userissue = request.form.get("issue")
    if first == "" and useremail == "" and userissue == "":
        return redirect('/contact_us')
    else:
        issue_query = Issue(first_name=first, last_name=last,
                            email=useremail, issue=userissue)
        db.session.add(issue_query)
        db.session.commit()
        return redirect('/')


@app.route('/add_user', methods=["POST"])
def add_user():
    first = request.form.get("fname")
    last = request.form.get("lname")
    useremail = request.form.get("email")
    userpassword = request.form.get("password")
    if first == "" and useremail == "" and userpassword == "":
        flash("Fill All Information")
        return redirect('/sign_up')
    else:
        user_query = User(first_name=first, last_name=last,
                          email=useremail, password=userpassword, status=0)
        db.session.add(user_query)
        db.session.commit()
        return redirect('/login_page')


@app.route('/issue')
def issue():
    profiles = Issue.query.all()
    return render_template('issue.html', profiles=profiles)

@app.route('/users')
def userinfo():
    profiles = User.query.all()
    return render_template('users.html', profiles=profiles)


@app.route('/delete/<int:id>')
def erase(id):
    data = Issue.query.get(id)
    db.session.delete(data)
    db.session.commit()
    return redirect('/issue')

@app.route('/delete_user/<int:id>')
def erase_user(id):
    data = User.query.get(id)
    db.session.delete(data)
    db.session.commit()
    return redirect('/users')

@app.route('/make_user/<int:id>')
def make_user(id):
    data = User.query.get(id)
    data.status = 0
    db.session.commit()
    return redirect("/users")

@app.route('/make_admin/<int:id>')
def make_admin(id):
    data = User.query.get(id)
    data.status = 1
    db.session.commit()
    return redirect("/users")


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return redirect('/')


if __name__ == "__main__":
    app.secret_key = "123546798"
    app.run(debug=False,host="0.0.0.0")
