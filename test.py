from unittest import TestCase
from app import app
from flask import session, request
from boggle import Boggle


class FlaskTests(TestCase):

    # TODO -- write tests for every view function / feature!

    def setUp(self):
        """required setup before each test"""
        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
        
    def test_homepage(self):
        """test that the homepage is rendered correctly"""

        with app.test_client() as client:
            resp = client.get("/")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h2>Welcome to Boggle!</h2>', html)

    def test_game_start(self):
        """test session initation"""

        with app.test_client() as client:
            resp = client.get('/game-start')
            html = resp.get_data(as_text=True)

            self.assertIn("boggle-board", session.keys())
            self.assertEqual(resp.status_code, 302)

        with app.test_client() as client:
            resp = client.get('/game-start', follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)

    def test_game_play(self):
        """test proper render of page"""

        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['boggle-board'] = [
                    ['a','b','c','d','e'],
                    ['b','c','d','e','f'],
                    ['c','d','e','f','g'],
                    ['d','e','f','g','h'],
                    ['e','f','g','h','i']
                ]

            resp = client.get('/game-play')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("boggle-board", session.keys())
            self.assertIn('<table id="board">', html)

    def test_check_word(self):
        """check for front end and back end communcation as well as posting data"""

        with app.test_client() as client:
            with client.session_transaction() as session:
                session['boggle-board'] = [
                    ['T','E','S','T','T'],
                    ['T','E','S','T','T'],
                    ['T','E','S','T','T'],
                    ['T','E','S','T','T'],
                    ['T','E','S','T','T']]
                
            response = client.post('/check-word', json = {"word": "test"}, follow_redirects=True)
            results = response.get_json()
            
            self.assertEqual(results['result'], "ok")

            with client.session_transaction() as session:
                session['boggle-board'] = [
                    ['T','R','U','E','E'],
                    ['T','R','U','E','E'],
                    ['T','R','U','E','E'],
                    ['T','R','U','E','E'],
                    ['T','R','U','E','E']]

            response = client.post('/check-word', json = {'word': "fail"}, follow_redirects=True)
            results = response.get_json()
            self.assertEqual(results["result"], "not-on-board")

            response = client.post('/check-word', json = {"word" : "asdf;lkjw"})
            results = response.get_json()
            self.assertEqual(results['result'], "not-word")

            # response = client.post('/check-word', json = {"word" : ""})
            # results = response.get_json()
            # self.assertEqual(results['result'], 'not-word')

    def test_log_stats_without_prev_session(self):
        """test that app utilizses session storage and creates proper scores/info (no previous session data)"""

        # with no session cookie present, does it log data correctly?
        with app.test_client() as client:
            response = client.post('/log-stats', json={"score": "23"})
            result = response.get_json()

            self.assertEqual(session['plays'], 1)
            self.assertEqual(session['highscore'], 23)
            self.assertEqual(result['brokeRecord'], True)

    def test_log_stats_with_prev_session(self):
        """check that the function will compare current data with previously stored data."""
        
        with app.test_client() as client:
            with client.session_transaction() as session:
                session['highscore'] = 15
                session['plays'] = 3

            response = client.post('/log-stats', json = {"score": "20"})
            result = response.get_json()

            self.assertEqual(result['brokeRecord'], True)

            response = client.post('/log-stats', json = {"score" : "10"})
            result = response.get_json()

            print(result)
            self.assertEqual(result['brokeRecord'], False)