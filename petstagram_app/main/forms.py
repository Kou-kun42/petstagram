from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    DateField,
    SelectField,
    SubmitField,
    TextAreaField
)
from wtforms.ext.sqlalchemy.fields import (
    QuerySelectField,
    QuerySelectMultipleField
)
from flask_login import current_user
from wtforms.validators import DataRequired, Length, ValidationError
from petstagram_app.models import Game, Console, Collection


class GameForm(FlaskForm):
    """Form to create a game."""
    title = StringField(
        'Game Title',
        validators=[DataRequired(), Length(min=3, max=80)]
        )
    release_date = DateField('Date Released')
    console = QuerySelectField(
        'Console',
        query_factory=lambda: Console.query, allow_blank=False
        )
    collections = QuerySelectMultipleField(
        'Add to Collection',
        query_factory=lambda: Collection.query.filter_by(user=current_user.id)
        )
    submit = SubmitField('Submit')


class ConsoleForm(FlaskForm):
    """Form to create a console."""
    name = StringField(
        'Console Name',
        validators=[DataRequired(), Length(min=3, max=80)]
        )
    submit = SubmitField('Submit')


class CollectionForm(FlaskForm):
    """Form to create a collection."""
    name = StringField(
        'Collection Name',
        validators=[DataRequired(), Length(min=3, max=120)]
        )
    submit = SubmitField('Submit')
