# Flask Development

### Documentation 

[Flask Installation](https://flask.palletsprojects.com/en/3.0.x/installation/)  
[Flask Tutorial](https://flask.palletsprojects.com/en/3.0.x/tutorial/) for a blog demonstration. 
[Flask Quickstart](https://flask.palletsprojects.com/en/3.0.x/quickstart/) for a quick application overview



# Framework Terminalogy

## Blueprints

collections of code within modules that will deliver content specific tasks such as in this project with `authentication`.

```python
# creates a blueprint named auth
# the url_prefix will be applied to all URs associated with the blueprint
bp = Blueprint('auth', __name__, url_prefix='/auth')
```

Blueprints will have a `url_prefix` that will dictate it's service endpoint for the API

## Views

these are endpoints of the application. They retain the Standard HTTP methos. However there is a Template based MVC structure within Flask that allows for complex logic to host base templates.
Below is an example of a route specified with a returned `render_template` call to render a Login View.

```python

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
    
```

## Jinja Templating

Jinja looks and behaves mostly like Python. Special delimiters are used to distinguish Jinja syntax from the static data in the template. Anything between {{ and }} is an expression that will be output to the final document. {% and %} denotes a control flow statement like if and for. Unlike Python, blocks are denoted by start and end tags rather than indentation since static text within a block could change indentation.

```html
<!doctype html>
<title>{% block title %}{% endblock %} - Flaskr</title>
<link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
<nav>
  <h1>Flaskr</h1>
  <ul>
    {% if g.user %}
      <li><span>{{ g.user['username'] }}</span>
      <li><a href="{{ url_for('auth.logout') }}">Log Out</a>
    {% else %}
      <li><a href="{{ url_for('auth.register') }}">Register</a>
      <li><a href="{{ url_for('auth.login') }}">Log In</a>
    {% endif %}
  </ul>
</nav>
<section class="content">
  <header>
    {% block header %}{% endblock %}
  </header>
  {% for message in get_flashed_messages() %}
    <div class="flash">{{ message }}</div>
  {% endfor %}
  {% block content %}{% endblock %}
</section>
```

## Running the Tutorial Application

```shell
# change directory into the flaskr project
flask --app flaskr run
```

## Installable Project

Making your project installable means that you can build a *wheel* file and install that in another environemnt
