from flask import render_template, Blueprint


bp = Blueprint("home", __name__)


@bp.route("/")
def home() -> str:
    return render_template("pages/index.html")
