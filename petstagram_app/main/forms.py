from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    DateField,
    SelectField,
    SubmitField,
    TextAreaField
)
from flask_login import current_user
from wtforms.validators import DataRequired, Length, ValidationError, URL
from petstagram_app.models import Post


class PostForm(FlaskForm):
    """Form to create a post."""
    title = StringField(
        'Post Title',
        validators=[DataRequired(), Length(min=3, max=80)]
        )
    message = StringField(
        'Post Message',
        validators=[DataRequired(), Length(min=3, max=280)]
        )
    photo_url = StringField(
        'Picture URL',
        validators=[DataRequired(), URL()]
        )
    submit = SubmitField('Submit')
