'''Test User Views'''

import os
from unittest import TestCase

from models import db, User

# make a test database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

from app import app, CURR_USER_KEY