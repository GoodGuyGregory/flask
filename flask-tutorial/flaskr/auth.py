import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash


from flaskr.db import get_db

# creates a blueprint named auth
# the url_prefix will be applied to all URs associated with the blueprint
bp = Blueprint('auth', __name__, url_prefix='/auth')


# Create a View *Decorator*
# This once Checks to ensure the Authentication is required

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        # checks for the user scope within the requests
        if g.user is None:
            return redirect(url_for('auth.login'))
        
        return view(**kwargs)
    return wrapped_view


# Create a View

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # imported from module
        db = get_db()
        # initialize Error
        error = None

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

@bp.route('/login', methods=('GET','POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        # assign the found user:
        # fetchone and fetchall are common for this task
        user = db.execute(
            'SELECT * from user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username'
            # compare the password form the user
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password'
        
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))
        # basically seals the data so that it is imutable
        flash(error)

    return render_template('auth/login.html')
    

    # before app requests registers a specific function 
    # that runs before the view function no matter what URL is requested.

    # this checks if a User is stored in the session    
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * from user WHERE id = ?', (user_id,)
        ).fetchone()


# logout - removes the user from the session of the application
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))