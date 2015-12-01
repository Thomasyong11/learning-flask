from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate
from flaskext.markdown import Markdown
from flaskext.uploads import UploadSet, configure_uploads, IMAGES

# app config
app = Flask(__name__)
app.config.from_object("settings")
app.debug = True

# database
db = SQLAlchemy(app)

# db migration
migrate = Migrate(app, db)

# markdown
md = Markdown(app, extensions=["fenced_code", "tables"])

# images
uploaded_images = UploadSet("images", IMAGES)
configure_uploads(app, uploaded_images)

from blog import views
from user import views
