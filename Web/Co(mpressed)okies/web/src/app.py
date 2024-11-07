from flask import Flask, g

from src.views import home, admin, user

app = Flask(__name__, instance_relative_config=True)


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)

    if db is not None:
        db.close()

app.register_blueprint(home.bp, url_prefix="/")
app.register_blueprint(admin.bp, url_prefix="/administration")
app.register_blueprint(user.bp, url_prefix="/user")
