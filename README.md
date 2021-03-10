# Casting Agency app

This repository provides the backbone for the backend of a casting agency application. The application is served by a database that stores information on actors/actress and movies. Two types of user have access to the application beyond the public homepage: agents and directors.


The purpose of this app is to demonstrate newly acquired skills to develop a simple app with the Flask micro-framework. It requires Python 3.6 or higher.

The app is currently deployed on Heroku, you can access it at https://castag-herokuapp.herokuapp.com/.

## Authorization

Authorization is provided through the third-party service **Auth0**. 

You need a valid token to access the app's API (except for the one public endpoint), for one of the two existing roles: **casting director**, or **casting agent**. The director has access to all the endpoints, and the agent can only retrieve information about actors.
Valid tokens for each of these roles are currently included in the `setup.sh` file for the project validation. They are to be exported as environment variables when the app is tested locally.

## API endpoints

#### GET `/`

This is the homepage endpoint. It is public. It retrieves information about the most recent actors and movies entered in the database.

*request parameters*: None.

*sample request*:

```bash
curl -X GET 'https://castag-herokuapp.herokuapp.com/'
```

#### GET `/actors/<actor_id>`

This endpoint retrieves information about a specific actor/actress. It is available to the agent and the director roles.

*request parameters*: `actor_id`, an integer.

*sample request*:
```bash
curl -X GET 'https://castag-herokuapp.herokuapp.com/actors/<actor_id>' \
-H 'Authorization: Bearer <VALID_TOKEN>'
```

#### GET `movies/<movie_id>

This endpoint retrieves information about a specific movie. It is available to the director only.

*request parameters*: `movie_id`, an integer.

*sample request*:
```bash
curl -X GET 'https://castag-herokuapp.herokuapp.com/movies/<movie_id>' \
-H 'Authorization: Bearer <VALID_TOKEN>'
```

#### POST `/actors`

This endpoint creates a new entry for an actor in the database. It is available to the director only.

*request body*: a JSON object with the following keys: `{"name": <str>, "age": <int>, "gender": <str>}`.

*sample request*:
```bash
curl -X POST 'https://castag-herokuapp.herokuapp.com/actors' \
-H 'Authorization: Bearer <VALID_TOKEN>' \
-H 'Content-Type: application/json'
-d '{"name": "actor", "age": 30, "gender": "Female"}'
```

#### PATCH `/actors/<actor_id>`

This endpoint updates an entry for an actor in the database. It is available to the director only.

*request parameter*: `actor_id`, an integer.

*request body*: a JSON object with **at least one** the following keys: `{"name": <str>, "age": <int>, "gender": <str>}`.

*sample request*:
```bash
curl -X PATCH 'https://castag-herokuapp.herokuapp.com/actors' \
-H 'Authorization: Bearer <VALID_TOKEN>' \
-H 'Content-Type: application/json'
-d '{"name": "actor"}'
```

#### DELETE `/actors/<actor_id>`

This endpoint deletes an entry for an actor in the database. It is available to the director only.

*request parameter*: `actor_id`, an integer.

*sample request*:
```bash
curl -X DELETE 'https://castag-herokuapp.herokuapp.com/actors' \
-H 'Authorization: Bearer <VALID_TOKEN>' \
-H 'Content-Type: application/json'
```

## Local installation and use

In order to test or run the app locally, first set up a Python virtual environment with the library of your choice, then install dependencies with:
```bash
pip3 install -r requirements.txt
```

Then create one database for running the app and one for testing:
```bash
createdb casting_agency
createdb casting_agency_test
```

Then set environment variables with `setup.sh`:
```bash
source setup.sh
```
This script defines environment variables for the application configuration, auth0 configuration, and - temporarily - tokens that are used in the testing script.
**NB**: the default local setting is a testing environment. Production and Development settings are associated with deployment on Heroku. This can be modified in the `config.py` file as needed.

The app can then be run with the following command:
```bash
FLASK_APP=app.py flask run
```

### Tests
Tests can be run with the following command:
```bash
pytest test_app.py
```