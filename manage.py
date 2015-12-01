from main_path import app
from flask.ext.script import Manager, Server
from flask.ext.migrate import MigrateCommand


manager = Manager(app)

# manager commands
manager.add_command("runserver", Server(use_debugger=True, use_reloader=True, host="localhost", port="5000"))
manager.add_command("db", MigrateCommand)

if __name__ == "__main__":
    manager.secret_key = app.config["SECRET_KEY"]

    manager.run()
