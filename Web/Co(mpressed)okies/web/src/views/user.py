import base64
import hashlib
from flask import (
    render_template,
    Blueprint,
    session,
    g,
    request,
    redirect,
    url_for,
    Response,
    make_response,
)

from src.auth.user import User
from src.middlewares.require_anonymous import require_anonymous
from src.middlewares.require_auth import require_auth
from src.db import query_db

bp = Blueprint("user", __name__)


@bp.before_app_request
def load_logged_in_user():
    if user_id := session.get("user_id") is None:
        g.user = None
    else:
        print(user_id)


@bp.route("/")
@require_auth
def home() -> str:
    user = User.from_b64(request.cookies.get("session").encode())
    return render_template("pages/user/index.html", user=user)


@bp.route("/login", methods=("GET", "POST"))
@require_anonymous
def login() -> Response | str:
    errors = {"nickname": [], "password": []}

    if request.method == "POST":
        if (
            not isinstance((nickname := request.form.get("nickname")), str)
            or not nickname.strip()
        ):
            errors["nickname"].append("Pseudo requis")

        if (
            not isinstance((password := request.form.get("password")), str)
            or not password.strip()
        ):
            errors["password"].append("Mot de passe requis")

        if not any(errors.values()):
            nickname = nickname.strip()
            password = hashlib.sha256(password.strip().encode()).hexdigest()

            if (
                user := query_db(
                    "select * from users where nickname = ? and password = ?",
                    (nickname, password),
                    one=True,
                )
            ) is not None:
                u = User(
                    nickname=user[1],
                    first_name=user[2],
                    last_name=user[3],
                    role=user[4],
                )
                sess = base64.b64encode(u.export().read())
                if not User.is_safe(sess):
                    return render_template("pages/error.html")

                response = make_response(redirect(url_for("admin.home")))
                response.set_cookie("session", sess.decode())
                return response
            else:
                errors["password"].append("Pseudo ou mot de passe invalide")

    return render_template("pages/user/login.html", errors=errors)


@bp.route("/register", methods=("GET", "POST"))
@require_anonymous
def register() -> Response | str:
    errors = {
        "first_name": [],
        "last_name": [],
        "nickname": [],
        "password": [],
    }

    if request.method == "POST":
        if (
            not isinstance((nickname := request.form.get("nickname")), str)
            or not nickname.strip()
        ):
            errors["nickname"].append("Pseudo requis")

        if (
            not isinstance((first_name := request.form.get("first_name")), str)
            or not first_name.strip()
        ):
            errors["first_name"].append("Prénom requis")

        if (
            not isinstance((last_name := request.form.get("last_name")), str)
            or not last_name.strip()
        ):
            errors["last_name"].append("Nom requis")

        if (
            not isinstance((password := request.form.get("password")), str)
            or not password.strip()
        ):
            errors["password"].append("Mot de passe requis")

        if not any(errors.values()):
            nickname = nickname.strip()

            if (
                query_db(
                    "select * from users where nickname = ?",
                    (nickname,),
                    one=True,
                )
                is None
            ):
                first_name = first_name.strip()
                last_name = last_name.strip()
                password = password.strip()

                query_db(
                    "insert into users (nickname, first_name, last_name, role, password) values (?, ?, ?, ?, ?)",
                    (
                        nickname,
                        first_name,
                        last_name,
                        "user",
                        hashlib.sha256(password.encode()).hexdigest(),
                    ),
                )
                return redirect(url_for("user.login"))
            else:
                errors["nickname"].append("Pseudo déjà utilisé ")

    return render_template("pages/user/register.html", errors=errors)


@bp.route("/logout")
def logout() -> Response:
    session.clear()
    return redirect(url_for("user.login"))
