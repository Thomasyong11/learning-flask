from functools import wraps
from flask import session, redirect, request, url_for, abort


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("username") is None:
            return redirect(url_for("login_page", next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def author_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("is_author") is None:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function
