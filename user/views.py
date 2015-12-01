from main_path import app, db
from flask import render_template, redirect, session, request, url_for
from user.form import RegisterForm, LoginForm
from user.models import User
from user.decorators import login_required
import bcrypt


@app.route('/login/', methods=("POST", "GET"))
def login_page():
    form = LoginForm()

    error = ""

    if request.method == "GET" and request.args.get("next"):
        session["next"] = request.args.get("next")

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.hashpw(form.password.data, user.password) == user.password:
                session["username"] = form.username.data
                session["is_author"] = user.is_author
                if "next" in session:
                    next_page = session.get("next")
                    session.pop("next")
                    return redirect(next_page)
                return redirect(url_for("index_page"))
            else:
                error = "Invalid password"
                return render_template("user/login.html", form=form, error=error)
        else:
            error = "Invalid username"
            return render_template("user/login.html", form=form, error=error)
    return render_template("user/login.html", form=form)


@app.route('/register', methods=('GET', 'POST'))
def register_page():
    form = RegisterForm()

    if form.validate_on_submit():
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(form.password.data, salt)
        user = User(form.fullname.data, form.email.data, form.username.data, hashed_password, False)
        try:
            db.session.add(user)
            db.session.flush()
            db.session.commit()
            session["username"] = form.username.data
            return redirect(url_for("login_page"))
        except Exception as e:
            db.session.rollback()
            print(e)
            error = "Choose a unique username and email"
            return render_template("user/register.html", form=form, error=error)
        return redirect(url_for("index_page"))
    return render_template('user/register.html', form=form)


@app.route("/logout/")
def logout():
    session.pop("username")
    session.pop("is_author")
    return redirect(url_for("index_page"))


@app.route('/success/')
@login_required
def success_page():
    return render_template("blog/index.html")
