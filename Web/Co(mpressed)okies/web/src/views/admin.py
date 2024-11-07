import inspect
import os

from flask import render_template, Blueprint, request

from src.middlewares.require_admin import require_admin
from src.auth.user import User

bp = Blueprint("admin", __name__)


@bp.route("/")
@require_admin
def home() -> str:
    user = User.from_b64(request.cookies.get("session").encode())
    flag1 = os.getenv(
        "FLAG1",
        "le flag devrait être ici, si tu vois ce message, ouvre un ticket",
    )

    user_code = inspect.getsource(User)
    return render_template(
        "pages/admin/index.html", user=user, flag1=flag1, user_code=user_code
    )
