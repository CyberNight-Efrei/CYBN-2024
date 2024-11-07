import functools

from flask import redirect, url_for, request

from src.auth.user import User


def require_anonymous(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        sess = request.cookies.get("session")

        try:
            u = User.from_b64(sess.encode())
            if u:
                return redirect(url_for("user.home"))
            else:
                return view(**kwargs)

        except Exception as e:
            print("require_anonymous", e)
            return view(**kwargs)

    return wrapped_view
