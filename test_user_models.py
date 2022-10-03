"""User models tests."""

# run these tests like:
#
#    FLASK_ENV=production python -m unittest test_user_models.py


import os
from unittest import TestCase
from flask import session
from models import Users, HealthIssues, Forecasts, Outfits, Locations, UsersHealth, db, connect_db

os.environ['DATABASE_URL'] = "postgresql:///healthstyleforecast"


# Now we can import app

from app import app, CURR_USER_KEY, healthissues


# Don't have WTForms use CSRF at all, since it's a pain to test

app.config['WTF_CSRF_ENABLED'] = False

class UserModelsTestCase(TestCase):
    """Tests for models of API."""

    def setUp(self):
        """Make demo data."""
        db.drop_all()
        db.create_all()
        
        self.client = app.test_client()

        self.testuser = Users.signup(username="usertest",
                                    email="test@test.com",
                                    password="testuser",
                                    first_name="user",
                                    last_name="test")



    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_user_model(self):
        """Does basic model work?"""

        u = Users(
            username="paulsmith",
                                    email="psmith@test.com",
                                    password="psmith",
                                    first_name="paul",
                                    last_name="smith"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.locations), 0)

    def test_location_model(self):
        """Does basic model work?"""
        u = Users(
            username="paulsmith",
                                    email="psmith@test.com",
                                    password="psmith",
                                    first_name="paul",
                                    last_name="smith"
        )

        db.session.add(u)
        db.session.commit()
        l = Locations(
            id=1,
            address="London,UK",
            username="paulsmith"
        )

        db.session.add(l)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.locations), 1)
     