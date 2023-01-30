from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)


class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), unique=False, nullable=False)
    last_name = db.Column(db.String(20), unique=False, nullable=False)
    email = db.Column(db.String(50), unique=False, nullable=False)
    issue = db.Column(db.String(500), unique=False, nullable=False)

    def __repr__(self):
        return f"First Name : {self.first_name}, Second Name : {self.first_name}, Email : {self.email}, issue: {self.issue}"


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/contact_us")
def contact_us():
    return render_template("contact_us.html")


@app.route('/add', methods=["POST"])
def profile():
    first =  request.form.get("fname")
    last = request.form.get("lname")
    useremail = request.form.get("email")
    userissue = request.form.get("issue")
    if first == "" and useremail == "" and userissue == "":
        return redirect('/contact_us')
    else:
        p = Profile(first_name=first, last_name=last, email=useremail, issue=userissue)
        print(p)
        db.session.add(p)
        db.session.commit()
        return redirect('/')

@app.route('/issue')
def issue():
    profiles = Profile.query.all()
    return render_template('issue.html', profiles=profiles)

@app.route('/delete/<int:id>')
def erase(id):
    data = Profile.query.get(id)
    db.session.delete(data)
    db.session.commit()
    return redirect('/issue')

if __name__ == "__main__":
    app.run(debug=True)