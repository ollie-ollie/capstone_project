import os
from datetime import datetime as dt
import json
import unittest

from app import app, db
from config import Testing
from models import Movie, Actor


class TestCastingAgency(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.app.config.from_object(Testing())
        self.client = self.app.test_client

        db.drop_all()
        db.create_all()

        self.body_actor = {
            'name': 'Aacc',
            'age': 30,
            'gender': 'Female'
        }

        for _ in range(3):
            self.test_actor = Actor(**self.body_actor)
            self.test_actor.insert()

        self.test_movie = Movie(
            title='A title',
            release_date=dt.now()
        )
        self.test_movie.insert()

        self.DIRECTOR_TOKEN = os.getenv('DIRECTOR_TOKEN')
        self.AGENT_TOKEN = os.getenv('AGENT_TOKEN')
        self.auth_header_director = {
            'Authorization': f'Bearer {self.DIRECTOR_TOKEN}'
        }
        self.auth_header_agent = {
            'Authorization': f'Bearer {self.AGENT_TOKEN}'
        }

    def tearDown(self):
        pass

    def test_get_public_if_success(self):
        res = self.client().get('/')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue('actors' in data)
        self.assertTrue('movies' in data)

    def test_get_actor_if_success(self):
        with self.subTest('test when user is director'):
            res = self.client().get(
                '/actors/1',
                headers=self.auth_header_director
            )
            data = json.loads(res.data)
            print(data)
            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertTrue('actor' in data)

        with self.subTest('test when is agent'):
            res = self.client().get(
                '/actors/1',
                headers=self.auth_header_agent
            )
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertTrue('actor' in data)

    def test_get_actor_if_failure_actor_not_found(self):
        res = self.client().get(
            '/actors/100',
            headers=self.auth_header_director
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'No resource found')

    def test_get_actor_if_failure_authorization(self):
        res = self.client().get('/actors/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Authorization header is expected.')

    def test_get_movie_if_success(self):
        res = self.client().get(
            '/movies/1',
            headers=self.auth_header_director
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue('movie' in data)

    def test_get_movie_if_failure_movie_not_found(self):
        res = self.client().get(
            '/movies/100',
            headers=self.auth_header_director
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'No resource found')

    def test_get_movie_if_failure_no_permission(self):
        res = self.client().get(
            '/movies/1',
            headers=self.auth_header_agent
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')

    def test_create_actor_if_success(self):
        res = self.client().post(
            '/actors',
            headers=self.auth_header_director,
            json=self.body_actor
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_create_actor_if_failure_wrong_request_body(self):
        res = self.client().post(
            '/actors',
            headers=self.auth_header_director,
            json={}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(
            data['message'],
            'Request body was empty or valid keys are missing'
        )

    def test_create_actor_if_failure_no_permission(self):
        res = self.client().post(
            '/actors',
            headers=self.auth_header_agent,
            json=self.body_actor
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')

    def test_patch_actor_if_success(self):
        res = self.client().patch(
            '/actors/1',
            headers=self.auth_header_director,
            json={'name': 'other name'}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_patch_actor_if_failure_wrong_body(self):
        res = self.client().patch(
            '/actors/1',
            headers=self.auth_header_director,
            json={}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(
            data['message'],
            'Request body was empty or valid keys are missing'
        )

    def test_patch_actor_if_failure_not_found(self):
        res = self.client().patch(
            '/actors/100',
            headers=self.auth_header_director,
            json={'name': 'other name'}
        )
        data = json.loads(res.data)
        print(data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'No resource found')

    def test_patch_actor_if_failure_no_permission(self):
        res = self.client().patch(
            '/actors/1',
            headers=self.auth_header_agent,
            json=self.body_actor
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')

    def test_delete_actor_if_success(self):
        res = self.client().delete(
            '/actors/2',
            headers=self.auth_header_director
        )
        data = json.loads(res.data)
        print(data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'] == 2)

    def test_delete_actor_if_failure_not_found(self):
        res = self.client().delete(
            '/actors/100',
            headers=self.auth_header_director
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'No resource found')

    def test_delete_actor_if_failure_no_permission(self):
        res = self.client().delete(
            '/actors/1',
            headers=self.auth_header_agent
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')


if __name__ == 'main':
    unittest.main()
