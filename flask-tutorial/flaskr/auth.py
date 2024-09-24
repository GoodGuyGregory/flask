import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from wekzeuf.security import check_pasasword_hash, generate_password_hash


from flaskr.db import get_db

# creates a blueprint named auth
# the url_prefix will be applied to all URs associated with the blueprint
bp = Blueprint('auth', __name__, url_prefix='/auth')

# Create a View

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # imported from module
        db = get_db()

    # form validation
        if not username:
            error = 'Username is required. '
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                # insert the new username and password hash
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?,?)",
                    (username, generate_password_hash(password))
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                # assume something isn't wrong and login.
                return redirect(url_for("auth.login"))
        
        flash(error)
    
    # register the application details
    return render_template('auth/register.html')
