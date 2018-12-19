from flask import session, flash, render_template

from functools import wraps

def check_logged_in(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'logged_in' in session:
            return func(*args, **kwargs)
        flash('You must log in to access this feature')
        return render_template('/index.html',)
    return wrapper

