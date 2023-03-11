from flask import Flask, url_for, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)


def migrate(db: SQLAlchemy, *models):
    db.drop_all()
    db.create_all()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)


class Role(db.Model):
    role_name = db.Column(db.String(100), primary_key=True)


@app.route("/")
def index():
    users = [x.username for x in User.query.all()]  or "There are no users"
    return render_template("index.html", users=users)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        new_user = User(username = request.form["username"])
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("register.html")

if __name__ == "__main__":
    app.run()
    # migrate(db)
