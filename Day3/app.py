from flask import Flask, request, render_template, redirect, url_for, session, flash
from models import db, User, Song
import os
from functools import wraps

app = Flask(__name__) # Object of Flask class

# For Database 
'''
1) Config --> uri
2) db = SQLAlchemy() ---> Getting from models
3) app and db setup
'''

# __________Database_____________
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SECRET_KEY'] = 'asdsd'  # Required for session management

# Connect to the database & make in context & create the database
db.init_app(app)
app.app_context().push()
db.create_all() # create or update the database schema
# __________Database End_____________









# RBAC
#Function
def isUser(): # return true/false
    return True if get_current_user() != None else False

def isCreator():
    u = get_current_user()
    if u and u.isCreator: return True
    return False

def isAdmin():
    u = get_current_user()
    if u and u.isAdmin: return True
    return False

#Decorator
def user_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            
            curr_id = session.get('id', None)
            curr_user_obj = User.query.filter_by(id=curr_id).first()

            # login
            if curr_user_obj:
                return fn(*args, **kwargs)
            else:
                flash('You are not LoggedIn!', 'danger')
                return redirect(url_for('access'))

        return decorator

    return wrapper

def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            curr_id = session.get('id', None)
            curr_user_obj = User.query.filter_by(id=curr_id).first()

            # login and admin
            if curr_user_obj and curr_user_obj.isAdmin:
                return fn(*args, **kwargs)
            else:
                flash('You are not Admin!', 'danger')
                return redirect(url_for('access'))

        return decorator

    return wrapper

def creator_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            curr_id = session.get('id', None)
            curr_user_obj = User.query.filter_by(id=curr_id).first()

            # login and creator
            if curr_user_obj and curr_user_obj.isCreator:
                return fn(*args, **kwargs)
            else:
                flash('You are not Creator!', 'danger')
                return redirect(url_for('access'))

        return decorator

    return wrapper

#_________
def get_current_user():
    id = session.get('id', None)  # return None or 4
    if id:
        return User.query.get(id)  # return <user1> == whole row
    return None

@app.route('/')
@user_required()
def home():
    user = get_current_user()  # None or <userobj>
    name, email = (None, None)
    if user:
        name = user.name
        email = user.email

    return render_template('home.html', name=name, email=email, user=user)

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
        flash('Login Successfull', 'success')
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
        flash('User Already Exist', 'danger')
        return redirect(url_for('access'))

    # Check if passwords match
    if password1 != password2:
        flash('Password Do not Matched', 'danger')
        return redirect(url_for('access'))

    # Create new user
    new_user = User(name=name, email=email, password=password1)
    db.session.add(new_user)
    db.session.commit()

    flash('User Created. Please Login Now', 'success')
    return redirect(url_for('access'))

@app.route('/logout')
def logout():
    session.pop('id', None)
    flash('Logout Successfull', 'success')
    return redirect(url_for('access'))  # Redirect to access page after logout


# Playlist
@app.route('/adsfhadsf')
@user_required()
def playlist():
    return "We will soon make it"

# Song Page

@app.route('/songs')
@creator_required()
def songs():
    user = get_current_user()
    songs = user.songs
    
    song = None
    song_id = request.args.get('song_id')
    if song_id:
        song = Song.query.filter_by(id=song_id).first()
    

    return render_template('songs.html', user=user, songs=songs, song=song)

@app.route('/upload_song', methods=['POST'])
@creator_required()
def upload_song():
    user = get_current_user()

    # get song data
    name = request.form.get('name')
    lyrics = request.form.get('lyrics')
    duration = request.form.get('duration')
    date = request.form.get('date')

    file = request.files.get('file')

    # Validation
    if not file or not name:
        flash('FileName and file need to be provided', 'danger')
        return redirect(url_for('songs'))

    # save info in db
    songobj = Song(name=name, lyrics=lyrics, duration=duration, date=date, user_id=user.id)
    db.session.add(songobj)
    db.session.commit()

    # save songfile in local storage
    filename=f'{songobj.id}.mp3'
    file.save(os.path.join('./static/songs/', filename))
    # file.save(f'./static/songs/{filename}')

    flash('Song Created Successfully', 'success')
    return redirect(url_for('songs'))


@app.route('/update_song')
@creator_required()
def update_song():
    song_id = request.args.get('song_id')
    songobj = Song.query.filter_by(id=song_id).first()
    return render_template('update_song.html', song=songobj)

@app.route('/update_song_details', methods=['POST'])
@creator_required()
def update_song_details():
    # get song data
    song_id = request.args.get('song_id')
    name = request.form.get('name')
    lyrics = request.form.get('lyrics')
    duration = request.form.get('duration')
    date = request.form.get('date')

    # update info in db
    songobj = Song.query.filter_by(id=song_id).first()
    songobj.name= name
    songobj.duration= duration
    songobj.lyrics= lyrics
    songobj.date= date
    db.session.commit()

    flash('Song Updated Successfully', 'success')
    return redirect(url_for('songs'))


@app.route('/delete_song')
@creator_required()
def delete_song():
    song_id = request.args.get('song_id')

    user = get_current_user()

    songobj = Song.query.filter_by (id = song_id).first()

    if not (songobj.user_id == user.id):
        flash('You are not creator of this Song', 'danger')
        return redirect(url_for('songs'))


    db.session.delete(songobj)
    db.session.commit()

    os.remove(f'./static/songs/{song_id}.mp3')
    flash('Song deleted Successfully', 'success')
    return redirect(url_for('songs'))







if __name__ == '__main__':
    app.run(debug=True)

    # print(__name__) # __name__ if directly executed
# # if you import then that name would be not __main__