import functools

from flask import redirect, url_for, g


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("log_in"))
        return view(**kwargs)
    return wrapped_view