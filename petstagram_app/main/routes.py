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

    return render_template('home.html', posts=Post.query.all())


@main.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()

    if form.validate_on_submit():
        new_post = Post(
            title=form.title.data,
            message=form.message.data,
            photo_url=form.photo_url.data,
            user=current_user
        )
        db.session.add(new_post)
        db.session.commit()

        flash('New post was created successfully.')
        return redirect(url_for('main.user', user_id=current_user.id))
    return render_template('create_post.html', form=form)


@main.route('/post/<post_id>', methods=['GET', 'POST'])
@login_required
def post(post_id):
    post = Post.query.get(post_id)
    form = PostForm(obj=game)

    if form.validate_on_submit():
        post.title = form.title.data
        post.message = form.message.data
        post.photo_url = form.photo_url.data

        db.session.commit()

        flash('Post was updated successfully.')
        return redirect(url_for('main.post', post_id=post_id))

    return render_template('post.html', post=post, form=form)


@main.route('/user/<user_id>')
@login_required
def collections(user_id):
    posts = Post.query.filter_by(user=user_id)
    return render_template('collections.html', posts=posts)
