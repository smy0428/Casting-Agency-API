# Full Stack Casting Agency API Backend

## About

The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

## API Reference

### Endpoints

`GET '/actors'`
- Fetches a list of actors
- Request arguments: None
- Example response:
```
{
    'success': True,
    'actors':[
        {
            'id': 1,
            'name': 'Billy Thornton',
            'age': 65,
            'gender': 1
        },
        {
            'id': 2,
            'name': 'Scarlett Johansson',
            'age': 35,
            'gender': 2
        }
    ] 
}
```

`GET '/movies'`
- Fetches a list of movies
- Request arguments: None
- Example response:
```
{
    'success': True,
    'movies':[
        {
            'id': 1,
            'title': 'Titanic',
            'release_date': '1997-12-19'
        },
        {
            'id': 2,
            'title': 'Transformers',
            'release_date': '2007-07-03'
        }
    ] 
}
```

`POST '/actors'`
- Add a new actor in the database
- Request arguments: {name: string, age: int, gender: int}
- Example argument:
```
{
    'name': 'Billy Thornton',
    'age': 65,
    'gender': 1
}
```
- Example response:
```
{
    'success': True,
    'actors':
    {
        'id': 1,
        'name': 'Billy Thornton',
        'age': 65,
        'gender': 1
    }
}
```

`POST '/movies'`
- Add a new movie in the database
- Request arguments: {title: string, release_date: string}
- Example argument:
```
{
    'title': 'Titanic',
    'release_date': '1997-12-19'
}
```
- Example response:
```
{
    'success': True,
    'movies':
    {
        'id': 1,
        'title': 'Titanic',
        'release_date': '1997-12-19'
    }
}
```

`PATCH '/actors/<int:actor_id>'`
- Update an actor in the database based on the actor_id
- Request arguments (optional): {name: string, age: int, gender: int}
- Example argument:
```
{
    'name': 'Scarlett Johansson',
    'age': 35,
    'gender': 2
}
```
- Example response:
```
{
    'success': True,
    'actors': 
    {
        'id': 1,
        'name': 'Scarlett Johansson',
        'age': 35,
        'gender': 2
    }
}
```

`PATCH '/movies/<int:movie_id>'`
- Update an movie in the database based on the movie_id
- Request arguments (optional): {title: string, release_date: string}
- Example argument:
```
    'title': 'Transformers',
    'release_date': '2007-07-03'
}
```
- Example response:
```
{
    'success': True,
    'movies': 
    {
        'id': 1,
        'title': 'Transformers',
        'release_date': '2007-07-03'
    }
}
```

`DELETE '/actors/<int:actor_id>'`
- Delete an actor from the database based on the actor_id
- Request arguments: actor_id
- Example response:
```
{
    'success': True,
    'actor_id': 2
}
```

`DELETE '/movies/<int:movie_id>'`
- Delete an movie from the database based on the movie_id
- Request arguments: movie_id
- Example response:
```
{
    'success': True,
    'movie_id': 2
}
```

### Error Handling

Errors are returned as JSON objects in the following format:
```
{
    'success': False,
    'error': 404,
    'message': 'Resource not found.'
}
```

## Testing

### Test API locally using command line tool

- Tokens in test_app.py need update if expired.
- To run the tests locally, run
```
dropdb casting_agency_test
createdb casting_agency_test
python test_app.py
```

### Test remote server using Postman

- Import the postman collection: postman_test_run/Capstone_Casting_Agency.postman_collection.json
- This collection has 3 roles.
- Casting_Assistant:
    - `get:actors`, `get:movies`
- Casting_Director:
    - `get:actors`, `get:movies`, `post:actors`, `patch:actors`, `patch:movies` `delete:actors`
- Executive Producer (all permissions):
    - `get:actors`, `get:movies`, `post:actors`, `post:movies`, `patch:actors`, `patch:movies`, `delete:actors`, `delete:movies`
- Right-clicking the collection folder for Casting_Assistant, Casting_Director and Executive_Producer, navigate to the authorization tab, and replace the JWT in the token field if expired.
- Run the collection and correct any errors.

## Installation

The following section explains how to set up and run the project locally.

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

#### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

### Database Setup in Postgres

With Postgres running, create a database:

```bash
createdb Casting_Agency
```

### Running the server

From within the root directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `app.py` directs flask to run the application from `app.py` file. 