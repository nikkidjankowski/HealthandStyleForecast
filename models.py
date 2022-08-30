"""Models for Cupcake app."""
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


bcrypt = Bcrypt()
db = SQLAlchemy()


def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)

class Users(db.Model):
    """users Model"""

    __tablename__ = "users"
    username = db.Column(
        db.String(20),
        nullable=False,
        unique=True,
        primary_key=True,
    )
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    locations = db.relationship('Locations')

    @classmethod
    def signup(cls, username, email, password, first_name, last_name):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')
       
        user = Users(
            username=username,
            email=email,
            password=hashed_pwd,
            first_name=first_name,
            last_name=last_name,
        )
  

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """
        print(password)

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            print(user.password)
            print(password)
            if is_auth:
                return user





class Locations(db.Model):
    """locations model"""

    __tablename__ = "locations"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    address = db.Column(
        db.Text,
        nullable=False,
    )
    username = db.Column(
        db.String,
        db.ForeignKey('users.username', ondelete='CASCADE'),
        nullable=False,
    )
    #users = db.relationship('Users')


class Forecasts(db.Model):
    """forecasts model"""

    __tablename__ = "forecasts"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    datetime = db.Column(
        db.DateTime,
        nullable=False,
    )

    tempmax = db.Column(
        db.Float,
        nullable=False,
    )
    tempmin = db.Column(
        db.Float,
        nullable=False,
    )
    feelslike = db.Column(
        db.Float,
        nullable=False,
    )
    humidity = db.Column(
        db.Float,
        nullable=False,
    )
    precipitation = db.Column(
        db.Float,
        nullable=False,
    )
    snow = db.Column(
        db.Float,
        nullable=False,
    )
    pressure = db.Column(
        db.Float,
        nullable=False,
    )
    visiabilty = db.Column(
        db.Float,
        nullable=False,
    )
    uvindex = db.Column(
        db.Float,
        nullable=False,
    )
    conditions = db.Column(
        db.String(200),
        nullable=False,
    )
    description = db.Column(
        db.String(200),
        nullable=False,
    )
    location_id = db.Column(
        db.Integer,
        db.ForeignKey('locations.id', ondelete='CASCADE'),
        nullable=False,
    )
    locations = db.relationship('Locations')

class Outfits(db.Model):
    """outfits model"""

    __tablename__ = "outfits"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )
    top = db.Column(
        db.Text,
        nullable=False,
    )
    bottom = db.Column(
        db.Text,
        nullable=False,
    )
    accessories = db.Column(
        db.Text,
        nullable=False,
    )

class  HealthIssues(db.Model):
    """health issues model"""

    __tablename__ = "healthissues"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )
    name = db.Column(
        db.Text,
        nullable=False,
    )
    description = db.Column(
        db.Text,
        nullable=False,
    )
    weathereffects = db.Column(
        db.Text,
        nullable=False,
    )
