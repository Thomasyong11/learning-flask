from main_path import app
import sqlalchemy

try:
    db_uri = "mysql://%s:@localhost/%s" % (app.config["DB_USERNAME"], app.config["BLOG_DATABASE_NAME"])
    engine = sqlalchemy.create_engine(db_uri)
    conn = engine.connect()
    conn.execute("commit")
    conn.execute('DROP DATABASE ' + app.config["BLOG_DATABASE_NAME"])
    print("connected")
except Exception as e:
    print("Database exist")
    print(str(e))
    print(e.__class__)

from main_path import db

# Add models here
from user.models import *
from blog.models import *

db.create_all()
