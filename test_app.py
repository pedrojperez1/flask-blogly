from unittest import TestCase
from app import app
from models import db, User

# Use test db and avoid cluttering tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class FlaskTests(TestCase):

    def setUp(self):
        """Add sample user"""
        User.query.delete()
        user = User(first_name="TestUser", last_name="Jones")
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        """Clean up failed transactions after test"""
        db.session.rollback()


    def test_users_route(self):
        with app.test_client() as client:
            res = client.get('/users')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('TestUser Jones', html)


    def test_user_details(self):
        test_user = User.query.first()
        with app.test_client() as client:
            res = client.get(f'/users/{test_user.id}')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn(f'<div class="h1">{test_user.first_name} {test_user.last_name}</div>', html)

    
    def test_show_user_edit(self):
        test_user = User.query.first()
        with app.test_client() as client:
            res = client.get(f'/users/{test_user.id}/edit')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<div class="h1">Edit user</div>', html)

    def test_new_user(self):
        with app.test_client() as client:
            res = client.post(
                '/users/new', 
                data=dict(
                    firstname='New',
                    lastname='Challenger',
                    profilepicture='www.google.com'
                ),
                follow_redirects=True
            )
            html = res.get_data(as_text=True)
            print(res)

            self.assertEqual(res.status_code, 200)
            self.assertIn('New Challenger', html)