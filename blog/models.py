from main_path import db, uploaded_images
from datetime import datetime


class Blog(db.Model):
    blog_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    admin = db.Column(db.Integer, db.ForeignKey('user.user_id'))

    def __init__(self, name, admin):
        self.name = name
        self.admin = admin

    def __repr__(self):
        return "<Name %r>" % self.name


class Category(db.Model):
    category_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name


class Post(db.Model):
    post_id = db.Column(db.Integer, primary_key=True)
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.blog_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    title = db.Column(db.String())
    body = db.Column(db.Text)
    image = db.Column(db.String(255))
    slug = db.Column(db.String(256), unique=True)
    published_date = db.Column(db.DateTime)
    live = db.Column(db.Boolean)

    @property
    def imagesrc(self):
        return uploaded_images.url(self.image)

    category_id = db.Column(db.Integer, db.ForeignKey('category.category_id'))
    category = db.relationship("Category", backref=db.backref("posts", lazy="dynamic"))

    def __init__(self, blog_id, user_id, title, body, category, slug, image=None, published_date=None, live=True):
        self.blog_id = blog_id
        self.user_id = user_id
        self.title = title
        self.body = body
        self.category = category
        self.slug = slug
        self.image = image
        if published_date is None:
            self.published_date = datetime.utcnow()
        self.live = live

    def __repr__(self):
        return "<Post %r>" % self.title
