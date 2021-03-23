from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from datetime import date, datetime
from petstagram_app.models import Game, Console, Collection, User
from petstagram_app.main.forms import GameForm, ConsoleForm, CollectionForm
from petstagram_app import bcrypt
from petstagram_app import app, db


main = Blueprint("main", __name__)

##########################################
#           Routes                       #
##########################################


@main.route('/')
def homepage():

    context = {
        "consoles": Console.query.all(),
        "games": Game.query.all()
    }

    return render_template('home.html', **context)


@main.route('/create_game', methods=['GET', 'POST'])
@login_required
def create_game():
    form = GameForm()

    if form.validate_on_submit():
        new_game = Game(
            title=form.title.data,
            release_date=form.release_date.data,
            console=form.console.data,
            collections=form.collections.data
        )
        db.session.add(new_game)
        db.session.commit()

        flash('New game was created and added to collection successfully.')
        return redirect(url_for('main.game_detail', game_id=new_game.id))
    return render_template('create_game.html', form=form)


@main.route('/create_console', methods=['GET', 'POST'])
@login_required
def create_console():
    form = ConsoleForm()
    if form.validate_on_submit():
        new_console = Console(
            name=form.name.data
        )
        db.session.add(new_console)
        db.session.commit()

        flash('New console created successfully.')
        return redirect(url_for('main.homepage'))

    return render_template('create_console.html', form=form)


@main.route('/create_collection', methods=['GET', 'POST'])
@login_required
def create_collection():
    form = CollectionForm()
    if form.validate_on_submit():
        new_collection = Collection(
            name=form.name.data,
            user=current_user.id
        )
        db.session.add(new_collection)
        db.session.commit()

        flash('New collection created successfully.')
        return redirect(url_for('main.homepage'))

    return render_template('create_collection.html', form=form)


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
