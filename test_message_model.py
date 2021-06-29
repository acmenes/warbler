'''Test messages'''

import os
from unittest import TestCase
from sqlalchemy import exc
from sqlalchemy.sql.functions import user 

from models import db, User, Follows, Likes, Message

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

from app import app

db.create_all()

class UserModelTestCase(TestCase):
    '''Test views for message'''

    def setUp(self):
        '''Create test client and add sample data'''
        db.drop_all()
        db.create_all()

        self.uid = 99999

        u = User.signup("testuser", "testuser@testuser.com", "password", None)

        u.id = self.uid

        db.session.commit()

        self.u = User.query.get(self.uid)
        self.client = app.test_client()

    def tearDown(self):
        '''Tear down the test'''
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_message_model(self):
        '''does the message model work?'''

        m = Message(text="test message", user_id=self.uid)

        db.session.add(m)
        db.session.commit()

        self.assertEqual(len(self.u.messages), 1)
        self.assertEqual(self.u.messages[0].text, "test message")
    
    def test_message_likes(self):
        '''test that a user can like a message'''

        m1 = Message(text="message 1 text", user_id=self.uid)

        m2 = Message(text="message 2 text", user_id=self.uid)

        u = User.signup("testuser2", "user2@user.com", "password", None)
        uid = 1111
        u.id = uid

        db.session.add_all([m1, m2, u])
        db.session.commit()

        u.likes.append(m1)

        db.session.commit()

        l = Likes.query.filter(Likes.user_id == uid).all()
        self.assertEqual(len(l), 1)
        self.assertEqual(l[0].message_id, m1.id)


