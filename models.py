"""Models for Cupcake app."""
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import requests
from datetime import datetime


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
        db.String,
        nullable=True,
    )

    temp = db.Column(
        db.Float,
        nullable=True,
    )

    feelslike = db.Column(
        db.Float,
        nullable=True,
    )
    dew = db.Column(
        db.Float,
        nullable=True,
    )
    humidity = db.Column(
        db.Float,
        nullable=True,
    )
    precip = db.Column(
        db.Float,
        nullable=True,
    )
    precipprob = db.Column(
        db.Float,
        nullable=True,
    )
    snow = db.Column(
        db.Float,
        nullable=True,
    )
    snowdepth = db.Column(
        db.Float,
        nullable=True,
    )
    preciptype = db.Column(
        db.Float,
        nullable=True,
    )
    pressure = db.Column(
        db.Float,
        nullable=True,
    )
    visibility = db.Column(
        db.Float,
        nullable=True,
    )
    windspeed = db.Column(
        db.Float,
        nullable=True,
    )
    winddir = db.Column(
        db.Float,
        nullable=True,
    )
    cloudcover = db.Column(
        db.Float,
        nullable=True,
    )
    uvindex = db.Column(
        db.Float,
        nullable=True,
    )
    windgust = db.Column(
        db.Float,
        nullable=True,
    )
    solarradiation = db.Column(
        db.Float,
        nullable=True,
    )
    solarenergy = db.Column(
        db.Float,
        nullable=True,
    )
    location_id = db.Column(
        db.Integer,
        db.ForeignKey('locations.id', ondelete='CASCADE'),
        nullable=True,
    )
    locations = db.relationship('Locations')

    @classmethod
    def getforecast(cls, address):
        dayarray = []
        test = []
        API_BASE_URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"
        key = 'ZX7VPUYV36DXTCEP46UQJ6JD6'
        req = requests.get(f"{API_BASE_URL}/{address}/today?unitGroup=us&include=hours&elements=datetime,temp,feelslike,humidity,dew,precip,precipprob,snow,snowdepth,preciptype,windgust,windspeed,winddir,pressure,visibility,cloudcover,solarradiation,solarenergy,uvindex",
                params={'key': key})
        two = req.json()
        three = two.get('days')
        for data in three:
            for x in data:
                if x == "hours":
                    time = data.get(x)
                    for i in time:
                        if type(i) is dict:
                            dayarray.append(i)
        
        for x in dayarray:
            
            for i in x:
                if i == 'datetime':
                    cclock = (x.get(i))
                    s = datetime.strptime(cclock, "%H:%M:%S")
                    oo = s.strftime("%I:%M %p")
            
            forecast = Forecasts(
                datetime=oo,
                temp=(x.get('temp')),
                feelslike=(x.get('feelslike')),
                humidity=(x.get('humidity')),
                dew=(x.get('dew')),
                precip=(x.get('precip')),
                precipprob=(x.get('precipprob')),
                snow=(x.get('snow')),
                snowdepth=(x.get('snowdepth')),
                preciptype=(x.get('preciptype')),
                windgust=(x.get('windgust')),
                windspeed=(x.get('windspeed')),
                winddir=(x.get('winddir')),
                pressure=(x.get('pressure')),
                visibility=(x.get('visibility')),
                cloudcover=(x.get('cloudcover')),
                solarradiation=(x.get('solarradiation')),
                solarenergy=(x.get('solarenergy')),
                uvindex=(x.get('uvindex')),
            )
            test.append(forecast)
            
        #print(forecast)
        db.session.add_all(test)
        #db.session.commit()

        #print(test)
        return test

    @classmethod
    def getConditions(cls, address):
        API_BASE_URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"
        key = 'ZX7VPUYV36DXTCEP46UQJ6JD6'
        req = requests.get(f"{API_BASE_URL}/{address}/today?unitGroup=us&iconSet=icons2",
                params={'key': key})
        two = req.json()
        three = two.get('currentConditions')
        print(three)
        for i in two:
            if i == 'currentConditions':
                print(two.get(i))
                d 
        return three
        

   
      

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
