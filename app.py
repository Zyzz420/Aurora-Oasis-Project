from flask import Flask, render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_jwt_extended import  JWTManager, jwt_required, create_access_token,get_jwt_identity
from auth import init_db
app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///aurora.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
app.config['SECRET_KEY'] = 'guess'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class SongForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    artist = StringField('Artist', validators=[DataRequired()])
    submit = SubmitField('Add Song')

def exists(item, playlist):
    for playlist_item in playlist.items:
        if playlist_item.song_id == item.song_id:
            return True
    return False

@app.route('/profiles')
def profiles():
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/profile/<int:user_id>')
def profile(user_id):
    user = User.query.filter_by(id=user_id).first_or_404()
    songs = Song.query.all()
    playlist = Playlist.query.get(user.playlist_id)
    return render_template('profile.html', user=user, songs=songs, playlist=playlist)

@app.route('/add_item/<int:user_id>/<int:song_id>/<int:playlist_id>')
def add_item(user_id, song_id, playlist_id):
    user = User.query.filter_by(id=user_id).first_or_404()
    playlist = Playlist.query.filter_by(id=playlist_id).first()
    item = Item.query.filter_by(playlist_id=playlist.id, song_id=song_id).first()
    if not exists(item, playlist):
        song = Song.query.get(song_id)
        new_item = Item(playlist_id=playlist.id, song_id=song.id)
        db.session.add(new_item)
        song.n += 1
        db.session.commit()
        flash('Song added to playlist')
    else:
        flash('Song already exists in playlist')
    return redirect(url_for('profile', user_id=user.id))

@app.route('/remove_item/<int:user_id>/<int:item_id>')
def remove_item(user_id, item_id):
    delete_item = Item.query.get(item_id)
    db.session.delete(delete_item)
    db.session.commit()
    flash('Song removed from playlist')
    return redirect(url_for('profile', user_id=user_id))

@app.route('/dashboard')
def dashboard():
    songs = Song.query.all()
    return render_template('dashboard.html', songs=songs)

@app.route('/add_song', methods=['GET', 'POST'])
def add_song():
    form = SongForm()
    if form.validate_on_submit():
        new_song = Song(title=form.title.data, artist=form.artist.data)
        db.session.add(new_song)
        db.session.commit()
        flash('Song added to library')
        return redirect(url_for('dashboard'))
    return render_template('add_song.html', form=form)

@app.route('/delete_song/<int:song_id>')
def delete_song(song_id):
    delete_song = Song.query.get(song_id)
    db.session.delete(delete_song)
    db.session.commit()
    flash('Song deleted from library')
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    from models import User, Song, Playlist, Item
    from auth import init_db

    init_db()

    app.run(debug=True)