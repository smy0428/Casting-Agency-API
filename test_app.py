import unittest
from models import setup_db, db, Actor, Movie
from app import create_app
from flask_sqlalchemy import SQLAlchemy
import json


#----------------------------------------------------------------------------#
# Tokens need uddat if expired.
#----------------------------------------------------------------------------#

CASTING_ASSISTANT_TOKEN  = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik5FLTlYVVd4S0dnY1hWbEZBY1o5dSJ9.eyJpc3MiOiJodHRwczovL3BldGVyLWNvZmZlZS1zaG9wLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjM4MTBiNzhmMThhYTAwNjg5ZDdlOTAiLCJhdWQiOiJjYXN0aW5nX2FnZW5jeSIsImlhdCI6MTU5NzU3MTg0NCwiZXhwIjoxNTk3NjU4MjQ0LCJhenAiOiJhcE9lY1NJcEY4azV6SVplODdUMzJCS1hqdVZKNUx0WSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.Na9D0GaLj5ftRVaUFKkyz207MjXCvntlFDYFNV7arBhnXktfLPTD8CmTjKUl7BW_6N7I4bVOXCpOjcjKo3_PYNvetzoMJVljzcxb0KkM-z2YcI0uDlcILvRbhRxU0zVOIo1gjZGoHRkGBeGHmPE5FSMdeA4Om85yzdRh_fSnHmrF3Cp1j9JfEHCye4IxjDpxcMEZAKlJJp8hCn7CAsgaVVL6ShaWLcOWb9a96LygnoPoAfjdpiWOgHgeBt0RSv-HUBAIHFhomjWmZ_058g-Rz6LwhXm5umuZavcW3G5Ozg4cs6Tt3w-m1QG3k1gX9BQVQayBVLRyx2GpbWL-q4YrfA'
CASTING_DIRECTOR_TOKEN   = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik5FLTlYVVd4S0dnY1hWbEZBY1o5dSJ9.eyJpc3MiOiJodHRwczovL3BldGVyLWNvZmZlZS1zaG9wLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjMzYjRhNmQyZjFjZDAwMzdlZmVmYjUiLCJhdWQiOiJjYXN0aW5nX2FnZW5jeSIsImlhdCI6MTU5NzU3MjA1MywiZXhwIjoxNTk3NjU4NDUzLCJhenAiOiJhcE9lY1NJcEY4azV6SVplODdUMzJCS1hqdVZKNUx0WSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiXX0.nCC3Nl5pjGAOtpAOoY1H2IaH5U8V-6LLOZTFqipVB5553V4MOCkJ068Q7QzmmerctXryCOrFBGAatuf6bNZYb59vaZX0khLq5FLz1TpM3HYtZIofe6DeHoAcEGCyaLjF0p_EH39wJBx8Oo1pQ7QutEKi8a6ClFf1m39vU6BYTfghi5l-kTEo4Arr_-xEPfXzrXB5nLZGHm5rqIMsv6f76cRUHnhMpvykk1L1WC_EAcVyUTUj-7yCwRDnE87VrfIUGntsxeQlAc3Lzexym8-1-OFYBJrfJjYf8hZGtA1gly-BOMtBDEjSz8ffvPAC4z_wwzWsZn5uLLH4tLKuhv4myQ'
EXECUTIVE_PRODUCER_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik5FLTlYVVd4S0dnY1hWbEZBY1o5dSJ9.eyJpc3MiOiJodHRwczovL3BldGVyLWNvZmZlZS1zaG9wLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjMzYjQ5MDY4ZGU5OTAwMzc0NzE1ZTQiLCJhdWQiOiJjYXN0aW5nX2FnZW5jeSIsImlhdCI6MTU5NzU3MjE1NiwiZXhwIjoxNTk3NjU4NTU2LCJhenAiOiJhcE9lY1NJcEY4azV6SVplODdUMzJCS1hqdVZKNUx0WSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.MWo-Ygknc4Jn-5b8zDqy2us4qXT3r6hr7Vby6-FWMHRF65tUg_EKa3tmyJAlVon4KgHdBnRUy_y3zirsySj0H5-PlxdhRHqvIiLqRvpbSH_Q016UGhp6YOfuluNqYf4SiPqhkq_kvtmNzl4kyew4rM1U6Vu0s3f_8gYEPqD4x7EZOlmybgF5gFLn1zZ_i-yl1If5IOXQx_tyPiLLP-NA9_MN_S6LyhvZ9LIzsHqipPAlTIuw3sqH9PyNmKclPtSQWV0DtkT3wl3O_Io7TX4C8E4AZpYJNRNHjoXnpl_u75YZxJrqlHPa5R1_RjOLhpsTLLtgvItzHHst_MPk7W0vJA'

ASSISTANT_HEADER  = {'Authorization': 'Bearer ' + CASTING_ASSISTANT_TOKEN}
DIRECTOR_HEADER   = {'Authorization': 'Bearer ' + CASTING_DIRECTOR_TOKEN}
PRODUCER_HEADER = {'Authorization': 'Bearer ' + EXECUTIVE_PRODUCER_TOKEN}

BEYOND_VALID_ID = 9999

#----------------------------------------------------------------------------#
# This class represents Casting_Agency test case.
#----------------------------------------------------------------------------#

class CastingAgencyTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.database_name = "casting_agency_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # everytime drop and create new tables
        db.drop_all()
        db.create_all()

        self.new_actor = {
            'name': 'Billy Thornton',
            'age': 65,
            'gender': 1
        }

        self.new_movie = {
            'title': 'Taitanic',
            'release_date': '1997-12-19'
        }

        self.update_actor = {
            'name': 'Scarlett Johansson',
            'age': 35,
            'gender': 2
        }

        self.update_movie = {
            'title': 'Transformers',
            'release_date': '2007-07-03'
        }
        

    def tearDown(self):
        db.session.commit()
        pass
    

    def test_get_actors(self):
        res = self.client.get('/actors', headers=ASSISTANT_HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
    
    def test_401_get_actors_no_token(self):
        res = res = self.client.get('/actors')

        self.assertEqual(res.status_code, 401)
    
    def test_get_movies(self):
        res = self.client.get('/movies', headers=ASSISTANT_HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_401_get_movies_no_token(self):
        res = res = self.client.get('/movies')
        self.assertEqual(res.status_code, 401)
    
    def test_post_actors(self):
        res = self.client.post('/actors', json=self.new_actor, headers=DIRECTOR_HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actors']['name'], self.new_actor['name'])
    
    def test_403_post_actors_unauthorized(self):
        res = self.client.post('/actors', json=self.new_actor, headers=ASSISTANT_HEADER)
        self.assertEqual(res.status_code, 403)
    
    def test_post_movies(self):
        res = self.client.post('/movies', json=self.new_movie, headers=PRODUCER_HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['movies']['title'], self.new_movie['title'])
    
    def test_403_post_movies_unauthorized(self):
        res = self.client.post('/movies', json=self.new_movie, headers=DIRECTOR_HEADER)
        self.assertEqual(res.status_code, 403)
    
    def test_update_actors(self):
        res_actor = self.client.post('/actors', json=self.new_actor, headers=DIRECTOR_HEADER)
        actor_id = json.loads(res_actor.data)['actors']['id']

        res = self.client.patch('/actors/{}'.format(actor_id), json=self.update_actor, headers=DIRECTOR_HEADER)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actors']['name'], self.update_actor['name'])
    
    def test_404_update_actor_beyond_valid_id(self):
        res = self.client.patch('/actors/{}'.format(BEYOND_VALID_ID), json=self.update_actor, headers=DIRECTOR_HEADER)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
    
    def test_update_movies(self):
        res_movie = self.client.post('/movies', json=self.new_movie, headers=PRODUCER_HEADER)
        movie_id = json.loads(res_movie.data)['movies']['id']

        res = self.client.patch('/movies/{}'.format(movie_id), json=self.update_movie, headers=DIRECTOR_HEADER)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['movies']['title'], self.update_movie['title'])
    
    def test_422_update_movie_empty_json(self):
        res_movie = self.client.post('/movies', json=self.new_movie, headers=PRODUCER_HEADER)
        movie_id = json.loads(res_movie.data)['movies']['id']

        res = self.client.patch('/movies/{}'.format(movie_id), json={}, headers=DIRECTOR_HEADER)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
    
    def test_delete_actors(self):
        res_actor = self.client.post('/actors', json=self.new_actor, headers=DIRECTOR_HEADER)
        actor_id = json.loads(res_actor.data)['actors']['id']

        res = self.client.delete('/actors/{}'.format(actor_id), headers=DIRECTOR_HEADER)
        data = json.loads(res.data)
        actor_not_exsited = Actor.query.get(actor_id)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actor_id'], actor_id)
        self.assertEqual(actor_not_exsited, None)

    def test_404_delete_actors_beyond_valid_id(self):
        res = self.client.delete('/actors/{}'.format(BEYOND_VALID_ID), headers=DIRECTOR_HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_delete_movies(self):
        res_movie = self.client.post('/movies', json=self.new_movie, headers=PRODUCER_HEADER)
        movie_id = json.loads(res_movie.data)['movies']['id']

        res = self.client.delete('/movies/{}'.format(movie_id), headers=PRODUCER_HEADER)
        data = json.loads(res.data)
        movie_not_exsited = Movie.query.get(movie_id)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['movie_id'], movie_id)
        self.assertEqual(movie_not_exsited, None)
    
    def test_403_delete_movies_beyond_unauthorized(self):
        res = self.client.delete('/movies/{}'.format(BEYOND_VALID_ID), headers=ASSISTANT_HEADER)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)


#----------------------------------------------------------------------------#
# Make the tests conveniently executable.
#----------------------------------------------------------------------------#

if __name__ == "__main__":
    unittest.main()