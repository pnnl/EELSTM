import unittest
from app import app,db
from app.models import User

class UserModelCase(unittest.TestCase):
    def setUp(self) -> None: #Every time before test run the setUp method
        # create a fake database which has the same structure and data as the true one
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self) -> None: #After the test clear the session and empty the database
        db.session.remove()
        db.drop_all()

    def test_test(self): #test the test itself
        self.assertEqual(1,1)

    def test_password_hashing(self): #test password_hashing
        u = User(username='Jerry')
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))


if __name__ == '__main__':
    unittest.main(verbosity=2)