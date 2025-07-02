from flask import Flask, request, render_template, redirect, url_for, session
from models import db, User

app = Flask(__name__) # Object of Flask class

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SECRET_KEY'] = 'asdsd'  # Required for session management

# Connect to the database & make in context & create the database
db.init_app(app)
app.app_context().push()
db.create_all() # create or update the database schema


def get_current_user():
    id = session.get('id', None)  # return None or 4
    if id:
        return User.query.get(id)  # return <user1> == whole row
    return None

@app.route('/')
def home():
    user = get_current_user()  # Get the current user from session
    name = user.name
    email = user.email

    return render_template('home.html', name=name, email=email)

@app.route('/access')
def access():
    return render_template('access.html')

@app.route('/login', methods=['POST'])
def login():

    email = request.form.get('email')
    password = request.form.get('password')

    # u = User.query.filter_by(email=email, password=password) # [..,..,..]
    u = User.query.filter_by(email=email, password=password).first() # <user1>

    # from database it will search that email and password
    if u and u.email==email and u.password==password:
        session['id'] = u.id # Login
        return redirect(url_for('home')) # Return to Home Page
   
    return redirect(url_for('access')) # return to access page again


@app.route('/register', methods=['POST'])
def register():
    # Get Data
    name = request.form.get('name')
    email = request.form.get('email')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')

    # Validate the data
    # Check if user already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return redirect(url_for('access'))

    # Check if passwords match
    if password1 != password2:
        return redirect(url_for('access'))

    # Create new user
    new_user = User(name=name, email=email, password=password1)
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('access'))

@app.route('/logout')
def logout():
    session.pop('id', None)
    return redirect(url_for('access'))  # Redirect to access page after logout

if __name__ == '__main__':
    app.run(debug=True)

    # print(__name__) # __name__ if directly executed
# # if you import then that name would be not __main__