from app import db


actor_movies = db.Table(
    'actor_movies',
    db.Column(
        'actor_id',
        db.Integer,
        db.ForeignKey('actors.id'),
        primary_key=True
    ),
    db.Column(
        'movie_id',
        db.Integer,
        db.ForeignKey('movies.id'),
        primary_key=True
    )
)


class Movie(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    release_date = db.Column(db.DateTime, nullable=False)

    actors = db.relationship(
        'Actor',
        secondary=actor_movies,
        backref=db.backref('movies', lazy=True)
    )

    def __repr__(self):
        return f'<Movie: {self.title}>'

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
            'actors': [actor.name for actor in self.actors]
        }


class Actor(db.Model):
    __tablename__ = 'actors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(), nullable=False)

    def __repr__(self):
        act_gen = 'Actress' if self.gender == 'Female' else 'Actor'
        return f'<{act_gen}: {self.name}>'

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'gender': self.gender,
            'age': self.age,
            'movies': [movie.title for movie in self.movies]
        }
