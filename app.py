"""Blogly application."""

from flask import Flask, render_template, request, redirect, flash
from models import db, connect_db, User, Post
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SECRET_KEY'] = "chickensarecool12341"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
debug = DebugToolbarExtension(app)


connect_db(app)
db.create_all()

@app.route('/')
def root():
    """root route"""
    posts = Post.query.order_by(Post.created_time.desc()).limit(5).all()
    print(posts)
    return render_template('home.html', posts=posts)

@app.route('/users')
def show_users():
    users = User.query.all()
    return render_template('all_users.html', users=users)

@app.route('/users/new')
def show_new_user_form():
    """Shows new user form"""
    return render_template('add_user.html')

@app.route('/users/<int:user_id>')
def user_details(user_id):
    """Get details for single user"""
    user = User.query.get_or_404(user_id)
    return render_template('user_details.html', user=user)

@app.route('/users/<int:user_id>/edit')
def show_edit_user(user_id):
    """Edit specific user id"""
    user = User.query.get_or_404(user_id)
    return render_template('edit_user.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def edit_user(user_id):
    user = User.query.get(user_id)

    first_name = request.form["firstname"]
    last_name = request.form["lastname"]
    image_url = request.form["profilepicture"]

    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url if image_url else None

    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """Delete specific user_id"""
    user = User.query.filter_by(id=user_id)
    user_name = user.one().get_full_name() # get full name before deleting so we can show msg
    db.session.delete(user)
    db.session.commit()

    flash(f"Successfully deleted user {user_name}")
    return redirect('/users')

@app.route('/users/new', methods=['POST'])
def add_user():
    """Adds new user to db"""
    first_name = request.form["firstname"]
    last_name = request.form["lastname"]
    image_url = request.form["profilepicture"]
    new_user = User(
        first_name=first_name, 
        last_name=last_name, 
        image_url=image_url if image_url else None
    )
    db.session.add(new_user)
    db.session.commit()
    return redirect('/users')

# Posts routes
@app.route('/users/<int:user_id>/posts/new')
def show_new_post_form(user_id):
    """shows user new post form"""
    user = User.query.get(user_id)
    return render_template('new_post.html', user=user)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def submit_new_post(user_id):
    title = request.form["title"]
    content = request.form["content"]
    new_post = Post(title=title, content=content, user_id=user_id)
    db.session.add(new_post)
    db.session.commit()
    return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    post = Post.query.get(post_id)
    return render_template('post.html', post=post)

@app.route('/posts/<int:post_id>/edit')
def show_edit_post(post_id):
    post = Post.query.get(post_id)
    return render_template('edit_post.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def edit_post(post_id):
    post = Post.query.get(post_id)
    post.title = request.form['title']
    post.content = request.form['content']
    db.session.add(post)
    db.session.commit()

    return redirect(f'/posts/{post.id}')

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    """deletes post given post_id"""
    post = Post.query.get(post_id)
    user_id = post.user_id # get user_id before deleting post
    db.session.delete(post)
    db.session.commit()
    flash('Successfully deleted post')
    return redirect(f'/users/{user_id}')