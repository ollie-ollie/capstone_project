from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from werkzeug.utils import import_string

from auth import requires_auth
from config import Production, Development, Testing
from exceptions import RequestBodyError, AuthError, NoResultFound, BadRequest
from utils import (
    validate_post_request_body_actor,
    validate_patch_request_body_actor,
    validate_body_movie
)

# ---------------------------------------------------------------------------#
# App Config.
# ---------------------------------------------------------------------------#

app = Flask(__name__)

setting = 'config.' + os.environ.get('APP_SETTING', 'Development')
cfg = import_string(setting)()
app.config.from_object(cfg)

CORS(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models import Movie, Actor


@app.after_request
def after_request(response):
    response.headers.add(
        'Acces-Control-Allow-Headers',
        'Content-Type, Authorization'
    )
    response.headers.add(
        'Acces-Control-Allow-Methods',
        'GET, POST, PATCH, DELETE, OPTIONS'
    )

    return response

# ---------------------------------------------------------------------------#
# Routes.
# ---------------------------------------------------------------------------#


@app.route('/', methods=['GET'])
def index():
    recent_movies = Movie.query.order_by(Movie.id.desc()).limit(10).all()
    recent_actors = Actor.query.order_by(Actor.id.desc()).limit(10).all()

    return jsonify({
        'success': True,
        'actors': [actor.serialize() for actor in recent_actors],
        'movies': [movie.serialize() for movie in recent_movies]
    })


@app.route('/actors/<int:actor_id>', methods=['GET'])
@requires_auth(permission='read:actor')
def get_actor(payload, actor_id):
    actor = Actor.query.filter(Actor.id == actor_id).one()

    return jsonify({
        'success': True,
        'actor': actor.serialize()
    })


@app.route('/movies/<int:movie_id>', methods=['GET'])
@requires_auth(permission='read:movie')
def get_movie(payload, movie_id):
    movie = Movie.query.filter(Movie.id == movie_id).one()

    return jsonify({
        'success': True,
        'movie': movie.serialize()
    })


@app.route('/actors', methods=['POST'])
@requires_auth(permission='create:actor')
def create_actor(payload):
    body = request.get_json()
    validate_post_request_body_actor(body)

    try:
        actor = Actor(
            name=body['name'],
            age=body['age'],
            gender=body['gender']
        )
        actor.insert()

        return jsonify({
            'success': True
        })

    except Exception:
        abort(422)


@app.route('/actors/<int:actor_id>', methods=['PATCH'])
@requires_auth(permission='update:actor')
def update_actor(payload, actor_id):
    body = request.get_json()
    validate_patch_request_body_actor(body)

    actor = Actor.query.filter(Actor.id == actor_id).one()

    try:
        if 'name' in body:
            actor.name = body['name']
        if 'age' in body:
            actor.age = body['age']
        if 'gender' in body:
            actor.gender = body['gender']
        actor.update()

        return jsonify({
            'success': True
        })

    except Exception:
        abort(422)


@app.route('/actors/<int:actor_id>', methods=['DELETE'])
@requires_auth(permission='delete:actor')
def delete_actor(payload, actor_id):
    actor = Actor.query.filter(Actor.id == actor_id).one()

    try:
        actor.delete()

        return jsonify({
            'success': True,
            'deleted': actor_id
        })

    except Exception:
        abort(422)

# ---------------------------------------------------------------------------#
# Error handlers.
# ---------------------------------------------------------------------------#


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "Unprocessable"
        }), 422


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Not found"
        }), 404


@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": "Unauthorized"
        }), 401


@app.errorhandler(403)
def forbidden(error):
    return jsonify({
        "success": False,
        "error": 403,
        "message": "Forbidden"
        }), 403


@app.errorhandler(AuthError)
def auth_error_handler(error):
    return jsonify({
        "success": False,
        "error": error.error['code'],
        "message": error.error['description']
        }), error.status_code


@app.errorhandler(RequestBodyError)
def request_body_error(error):
    return jsonify({
        "success": False,
        "error": error.error['code'],
        "message": error.error['description']
        }), error.status_code


@app.errorhandler(BadRequest)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": 'Bad request'
        }), 400


@app.errorhandler(NoResultFound)
def no_result_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": 'No resource found'
        }), 404


if __name__ == '__main__':
    app.run()

# def create_app(test_config=None):
#   # create and configure the app


#   return app

# APP = create_app()

# if __name__ == '__main__':
#     APP.run(host='0.0.0.0', port=8080, debug=True)
