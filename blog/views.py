from main_path import app, uploaded_images
from flask import render_template, redirect, url_for, flash, session, request
from blog.form import SetupForm, PostForm
from user.models import User
from blog.models import Blog, Category, Post
from main_path import db
from user.decorators import author_required, login_required
import bcrypt
from slugify import slugify


POST_BY_PAGE = app.config["POST_BY_PAGE"]


@app.route("/")
@app.route("/index/")
@app.route("/index/<int:page>")
def index_page(page=1):
    blog = Blog.query.first()
    post = Post.query.filter_by(live=True).order_by(Post.published_date.desc()).paginate(page, POST_BY_PAGE, False)
    return render_template("blog/index.html", blog=blog, post=post)


@app.route("/admin/")
@app.route("/admin/<int:page>")
@login_required
@author_required
def admin_page(page=1):
    post = Post.query.filter_by(live=True).order_by(Post.published_date.desc()).paginate(page, POST_BY_PAGE, False)
    return render_template("blog/admin.html", post=post)


@app.route("/setup/", methods=("POST", "GET"))
def setup_page():
    blog = Blog.query.count()

    if blog:
        return redirect(url_for("admin_page"))

    form = SetupForm()

    error = ""

    if form.validate_on_submit():
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(form.password.data, salt)
        user = User(form.fullname.data, form.email.data, form.username.data, hashed_password, True)
        try:
            db.session.add(user)
            db.session.flush()
        except Exception as e:
            print(e)
            error = "Choose a unique username and email"
            return render_template("blog/setup.html", form=form, error=error)

        if user.user_id:
            blog = Blog(form.name.data, user.user_id)
            db.session.add(blog)
            db.session.flush()
        else:
            db.session.rollback()

        if user.user_id and blog.blog_id:
            db.session.commit()
            flash("Blog created")
            return redirect(url_for("admin_page"))
        else:
            db.session.rollback()
            error = "Error creating blog"
    return render_template("blog/setup.html", form=form, error=error)


@app.route("/post/", methods=("GET", "POST"))
@author_required
def post_page():
    form = PostForm()

    if form.validate_on_submit():
        # import pdb; pdb.set_trace()
        image = request.files.get("image")
        filename = None

        try:
            filename = uploaded_images.save(image)
        except Exception as e:
            flash("The image was not uploaded! ")
            print(e)

        if form.new_category.data:
            new_category = Category(form.new_category.data)
            db.session.add(new_category)
            db.session.flush()
            category = new_category
        else:
            category = form.category.data

        try:
            blog = Blog.query.first()
            blog_id = blog.blog_id
            user = User.query.filter_by(username=session["username"]).first()
            author = user.user_id
            print(str(author))
            title = form.title.data
            body = form.body.data
            slug = slugify(form.title.data)
            post = Post(blog_id, author, title, body, category, slug, filename)
            db.session.add(post)
            db.session.commit()
            return redirect(url_for("article_page", slug=slug))
        except Exception as e:
            print(e)
            error = "error found while committing to database"
            return render_template("blog/post.html", form=form, error=error)
    return render_template("blog/post.html", form=form, action="new")


@app.route("/edit/<int:post_id>", methods=("GET", "POST"))
def edit_page(post_id):
    post = Post.query.filter_by(post_id=post_id).first_or_404()
    form = PostForm(obj=post)

    if form.validate_on_submit():
        original_image = post.image
        form.populate_obj(post)

        if form.image.has_file():
            image = request.files.get("image")
            try:
                filename = uploaded_images.save(image)
            except:
                flash("The image was not uploaded")

            if filename:
                post.image = filename
        else:
            post.image = original_image

        if form.new_category.data:
            new_category = Category(form.new_category.data)
            db.session.add(new_category)
            db.session.flush()
            post.category = new_category
        db.session.commit()
        return redirect(url_for("article_page", slug=post.slug))
    return render_template("blog/post.html", form=form, action="edit", post=post)


@app.route("/delete/<int:post_id>", methods=("GET", "POST"))
def delete(post_id):
    post = Post.query.filter_by(post_id=post_id).first_or_404()
    post.live = False
    db.session.commit()
    flash("Article deleted")
    return redirect(url_for("admin_page"))


@app.route("/article/<slug>")
def article_page(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    return render_template("blog/article.html", post=post)
