from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from datetime import date, datetime
from petstagram_app.models import Post, User
from petstagram_app.main.forms import PostForm
from petstagram_app import bcrypt
from petstagram_app import app, db


main = Blueprint("main", __name__)

##########################################
#           Routes                       #
##########################################


@main.route('/')
def homepage():
    posts = Post.query.all()
    posts.reverse()

    return render_template('home.html', posts=posts)


@main.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()

    if form.validate_on_submit():
        new_post = Post(
            title=form.title.data,
            message=form.message.data,
            photo_url=form.photo_url.data,
            user=User.query.get(current_user.id).username
        )
        db.session.add(new_post)
        db.session.commit()

        flash('New post was created successfully.')
        return redirect(url_for('main.homepage'))
    return render_template('create_post.html', form=form)


@main.route('/post/<post_id>', methods=['GET', 'POST'])
@login_required
def post_detail(post_id):
    post = Post.query.get(post_id)
    form = PostForm(obj=post)

    if form.validate_on_submit():
        post.title = form.title.data
        post.message = form.message.data
        post.photo_url = form.photo_url.data

        db.session.commit()

        flash('Post was updated successfully.')
        return redirect(url_for('main.post_detail', post_id=post_id))

    return render_template('post_detail.html', post=post, form=form)


@main.route('/user/<user_id>')
@login_required
def user(user_id):
    username = User.query.get(user_id).username
    posts = Post.query.filter_by(user=username)
    return render_template('user.html', posts=posts)
