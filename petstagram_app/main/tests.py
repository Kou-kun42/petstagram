import os
import unittest
from datetime import date
from petstagram_app import app, db, bcrypt
from petstagram_app.models import Game, Console, Collection, User

"""
Run these tests with the command:
python -m unittest petstagram_app.main.tests
"""

#################################################
# Setup
#################################################


def login(client, username, password):
    return client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)


def logout(client):
    return client.get('/logout', follow_redirects=True)


def create_games():
    a1 = Console(name='PS6')
    b1 = Game(
        title='Game Title',
        release_date=date(1960, 7, 11),
        console=a1
    )
    db.session.add(b1)

    b2 = Game(
        title='Game Title2',
        release_date=date(1960, 7, 11),
        console=a1
    )
    db.session.add(b2)
    db.session.commit()


def create_user():
    # Creates a user with username 'me1' and password of 'password'
    password_hash = bcrypt.generate_password_hash('password').decode('utf-8')
    user = User(username='me1', password=password_hash)
    db.session.add(user)
    db.session.commit()

#################################################
# Tests
#################################################


class MainTests(unittest.TestCase):

    def setUp(self):
        """Executed prior to each test."""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

    def test_homepage_logged_out(self):
        """Test that the games show up on the homepage."""
        # Set up
        create_games()
        create_user()

        # Make a GET request
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Check that page contains all of the things we expect
        response_text = response.get_data(as_text=True)
        self.assertIn('Game Title', response_text)
        self.assertIn('Game Title2', response_text)
        self.assertIn('Log In', response_text)
        self.assertIn('Sign Up', response_text)

        # Check that the page doesn't contain things we don't expect
        # (these should be shown only to logged in users)
        self.assertNotIn('Create Game', response_text)
        self.assertNotIn('Create Console', response_text)
        self.assertNotIn('Create Collection', response_text)

    def test_homepage_logged_in(self):
        """Test that the games show up on the homepage."""
        # Set up
        create_games()
        create_user()
        login(self.app, 'me1', 'password')

        # Make a GET request
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Check that page contains all of the things we expect
        response_text = response.get_data(as_text=True)
        self.assertIn('Game Title', response_text)
        self.assertIn('Game Title2', response_text)
        self.assertIn('me1', response_text)
        self.assertIn('Log Out', response_text)
        self.assertIn('Create Game', response_text)
        self.assertIn('Create Console', response_text)
        self.assertIn('Create Collection', response_text)

        # Check that the page doesn't contain things we don't expect
        # (these should be shown only to logged out users)
        self.assertNotIn('Log In', response_text)
        self.assertNotIn('Sign Up', response_text)

    def test_game_detail_logged_in(self):
        """Test that the game appears on its detail page."""
        create_games()
        create_user()
        login(self.app, 'me1', 'password')

        # Make a GET request to the URL /game_detail/1, check to see that the
        # status code is 200
        response = self.app.get('/game_detail/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response_text = response.get_data(as_text=True)
        self.assertIn('Game Title', response_text)
        self.assertIn("PS6", response_text)
        self.assertIn('July 11, 1960', response_text)

    def test_update_game(self):
        """Test updating a game."""
        # Set up
        create_games()
        create_user()
        login(self.app, 'me1', 'password')

        # Make POST request with data
        post_data = {
            'title': 'Changed',
            'publish_date': '1960-07-12',
            'console': "PS5"
        }
        self.app.post('/game_detail/1', data=post_data)

        # Make sure the game was updated as we'd expect
        game = Game.query.get(1)
        self.assertEqual(game.title, "Game Title")
        self.assertEqual(game.release_date, date(1960, 7, 11))

    def test_create_collection(self):
        """Test creating a collection."""
        # Set up
        create_games()
        create_user()
        login(self.app, 'me1', 'password')

        # Make POST request with data
        post_data = {
            'name': 'Test'
        }
        self.app.post('/create_collection', data=post_data)

        # Make sure collection was updated as we'd expect
        created_collection = Collection.query.filter_by(name='Test').one()
        self.assertIsNotNone(created_collection)

    def test_create_game_logged_out(self):
        """
        Test that the user is redirected when trying to access the create game
        route if not logged in.
        """
        # Set up
        create_games()
        create_user()

        # Make GET request
        response = self.app.get('/create_game')

        # Make sure that the user was redirecte to the login page
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login?next=%2Fcreate_game', response.location)

    def test_create_console(self):
        """Test creating an console."""
        create_games()
        create_user()
        login(self.app, 'me1', 'password')

        # Make a POST request to the /create_console route
        post_data = {
            'name': 'PS7',
        }
        self.app.post('/create_console', data=post_data)

        # Verify that the console was updated in the database
        created_console = Console.query.filter_by(name='PS7').one()
        self.assertIsNotNone(created_console)
