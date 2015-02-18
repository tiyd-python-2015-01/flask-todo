import os
import to_do
import unittest
import tempfile
from hashlib import md5

class ToDoTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, to_do.app.config['DATABASE'] = tempfile.mkstemp()
        to_do.app.config['TESTING'] = True
        self.app = to_do.app.test_client()
        to_do.init_db()
        self.app.post('/create_user', data=dict(
            username="Ted",
            password="Ted"),
            follow_redirects=True)

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(to_do.app.config['DATABASE'])

    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password),
            follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def test_empty_db(self):
        rv = self.app.get('/', follow_redirects=True)
        assert 'Login' in str(rv.data)

    def test_create_user(self):
        rv = self.app.post('/create_user', data=dict(
            username="Ted2",
            password="Ted"),
            follow_redirects=True)
        assert 'Account successfully created!' in str(rv.data)

    def test_login_logout(self):
        rv = self.login('Ted', 'Ted')
        assert 'Login successful!' in str(rv.data)
        rv = self.logout()
        assert 'Have a nice day!' in str(rv.data)
        rv = self.login('Tedx', 'Ted')
        assert 'Invalid username' in str(rv.data)
        rv = self.login('Ted', 'defaultx')
        assert 'Invalid password' in str(rv.data)

    def test_add_remove_messages(self):
        self.login('Ted', 'Ted')
        rv = self.app.post('/add', data=dict(
            todo='Test'
        ), follow_redirects=True)
        assert 'Nothing to do!' not in str(rv.data)
        assert 'Test' in str(rv.data)
        rv = self.app.post('/remove', data=dict(
            item=1), follow_redirects=True)
        assert 'Item moved to completed list!' in str(rv.data)
        rv = self.app.get('/done')
        assert 'Test' in str(rv.data)

        
if __name__ == '__main__':
    unittest.main()
