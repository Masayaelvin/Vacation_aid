import unittest
from flask import json
from bk_config import app, db
from models import User

class RoutesTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        db.create_all()
        self.user = User(user_name='testuser', email='test@example.com', password='password', user_id='12345', role='host')
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_current_user(self):
        # Simulate login and get token
        response = self.app.post('/login', json={'email': 'test@example.com', 'password': 'password'})
        token = json.loads(response.data)['token']

        # Test get current user
        response = self.app.get('/current_user', headers={'Authorization': token})
        self.assertEqual(response.status_code, 200)
        self.assertIn('user_id', json.loads(response.data))
        self.assertIn('username', json.loads(response.data))
        self.assertIn('email', json.loads(response.data))
        self.assertIn('role', json.loads(response.data))

    def test_add_listing_as_host(self):
        # Simulate login and get token
        response = self.app.post('/login', json={'email': 'test@example.com', 'password': 'password'})
        token = json.loads(response.data)['token']

        # Test adding a listing
        response = self.app.post('/add_listing', headers={'Authorization': token}, json={
            'title': 'Test Property',
            'description': 'A nice place to stay',
            'location': 'Test Location',
            'price_per_night': 100
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('Property listing added successfully', json.loads(response.data)['message'])

    def test_add_listing_as_non_host(self):
        # Change user role to non-host
        self.user.role = 'guest'
        db.session.commit()

        # Simulate login and get token
        response = self.app.post('/login', json={'email': 'test@example.com', 'password': 'password'})
        token = json.loads(response.data)['token']

        # Test adding a listing
        response = self.app.post('/add_listing', headers={'Authorization': token}, json={
            'title': 'Test Property',
            'description': 'A nice place to stay',
            'location': 'Test Location',
            'price_per_night': 100
        })
        self.assertEqual(response.status_code, 403)
        self.assertIn('Only hosts can add listings.', json.loads(response.data)['message'])

if __name__ == '__main__':
    unittest.main()
