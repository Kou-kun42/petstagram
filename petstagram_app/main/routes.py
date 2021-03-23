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

    return render_template('home.html', Post.query.all())


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



@main.route('/game_detail/<game_id>', methods=['GET', 'POST'])
def game_detail(game_id):
    game = Game.query.get(game_id)
    form = GameForm(obj=game)

    if form.validate_on_submit():
        game.title = form.title.data
        game.release_date = form.release_date.data
        game.console = form.console.data
        game.collections = form.collections.data

        db.session.commit()

        flash('Game was updated successfully.')
        return redirect(url_for('main.game_detail', game_id=game_id))

    return render_template('game_detail.html', game=game, form=form)


@main.route('/console_detail/<console_id>', methods=['GET', 'POST'])
def console_detail(console_id):
    console = Console.query.get(console_id)
    form = ConsoleForm(obj=console)

    if form.validate_on_submit():
        console.name = form.name.data

        db.session.commit()

        flash('Console was renamed successfully.')
        return redirect(url_for('main.console_detail', console_id=console_id))

    return render_template('console_detail.html', console=console, form=form)


@main.route('/collections/<user_id>')
@login_required
def collections(user_id):
    collects = Collection.query.filter_by(user=user_id)
    return render_template('collections.html', collects=collects)


@main.route('/collection/<collection_id>', methods=['GET', 'POST'])
@login_required
def collection_detail(collection_id):
    collection = Collection.query.get(collection_id)
    form = CollectionForm(obj=collection)

    if form.validate_on_submit():
        collection.name = form.name.data

        db.session.commit()

        flash('Collection name changed successfully.')
        return redirect(
            url_for('main.collection_detail', collection_id=collection_id))

    return render_template(
        'collection_detail.html', collection=collection, form=form)
