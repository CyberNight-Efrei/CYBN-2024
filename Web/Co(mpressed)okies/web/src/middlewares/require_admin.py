import functools

from flask import redirect, url_for, request

from src.auth.user import User


def require_admin(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        sess = request.cookies.get("session")

        try:
            u = User.from_b64(sess.encode())
            if u and u.role == "admin":
                return view(**kwargs)
            else:
                return redirect(url_for("user.login"))

        except Exception as e:
            print("require_admin", e)
            return redirect(url_for("user.login"))

    return wrapped_view
