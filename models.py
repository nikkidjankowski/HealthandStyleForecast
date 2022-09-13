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
        #print(dict(two))
        three = two.get('currentConditions')
        #print(three)
        for i in two:
            if i == 'currentConditions':
                
                info = two.get(i)
                #print(info)
                d = dict(info)
                #print(d.get('preciptype'))

    
        d = {
            'address':address,
            'description':two.get('description'),
            'temp':d.get('temp'),
            'feelslike':d.get('feelslike'),
            'conditions':d.get('conditions'),
            'uvindex':d.get('uvindex'),
            'precip':d.get('precip'),
            'pressure':d.get('pressure'),
            'preciptype':d.get('preciptype'),
            'precipprob':d.get('precipprob'),
        }
        return d
   
      

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
    @classmethod
    def whattowear(cls, username, conditions):
        clothes = []
        
        
        if conditions.get('temp') >= 80:
            u = list(db.session.query(Outfits.top,Outfits.bottom,Outfits.accessories).filter(Outfits.id == 1).first())
          
        elif conditions.get('temp') <= 50:
            u = list(db.session.query(Outfits.top,Outfits.bottom,Outfits.accessories).filter(Outfits.id == 2).first())
            
        else:
            u = list(db.session.query(Outfits.top,Outfits.bottom,Outfits.accessories).filter(Outfits.id == 3).first())
            
        u.append(conditions.get('address'))
        return u


       

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
    

class UsersHealth(db.Model):
    """Mapping user likes to warbles."""

    __tablename__ = 'usershealth' 


    username = db.Column(
        db.String(20),
        db.ForeignKey('users.username'), primary_key=True
    )

    healthissues_id = db.Column(
        db.Integer,
        db.ForeignKey('healthissues.id'), primary_key=True
    )

    issue = db.Column(db.Text)

    @classmethod
    def userhealth(cls, responses, username):
        
        
        newIndex = 0
        hissues = []
        name = []
        for i in responses:
            newIndex = newIndex + 1
            if i == 'Yes':
                #print(newIndex)
                diease = HealthIssues.query.get(newIndex)
                name.append(diease.name)
                issue = UsersHealth(username=username, healthissues_id=diease.id, issue=diease.name)
                hissues.append(issue)
    
        #print(name)
        db.session.add_all(hissues) 
        
        return hissues 

    @classmethod
    def warning(cls, username, dieases, currentconditions):
        
        
        
        newIndex = 0
        hindex = []
        alerts = []
        place = currentconditions.get('address')
        alerts.append(place)

        
        for i in dieases:
            for h in i:
                hindex.append(h)

        for num in hindex:
            if num == 1:
                if currentconditions.get('temp') >= 80:
                    al = 'The current temperature can cause issues for your Asthma and Allergies'
                    alerts.append(al)
                if currentconditions.get('precipprob') is not None:
                    al = 'The current rain could increase issues with your Asthma and Allergies'
                    alerts.append(al)
            if num == 2:
                if currentconditions.get('temp') <= 50: 
                    al = 'The current temperature can cause your Joint Pain to increase'
                    alerts.append(al)
                if currentconditions.get('pressure') < 1013.0:
                    al = 'The current atmospheric pressure can cause your Joint Pain to increase'
                    alerts.append(al)
                if currentconditions.get('precipprob') is not None:
                    al = 'The current rain could increase issues with your Joint Pain'
                    alerts.append(al)
            if num == 3:
                if currentconditions.get('temp') <= 50: 
                    al = 'The current temperature can cause your Headaches to increase'
                    alerts.append(al)
                if currentconditions.get('pressure') < 1013.0:
                    al = 'The current atmospheric pressure can cause your Headaches to increase'
                    alerts.append(al)
                if currentconditions.get('precipprob') is not None:
                    al = 'The current rain could increase issues with your Joint Pain'
                    alerts.append(al)
            if num == 4:
                if currentconditions.get('temp') <= 50: 
                    al = 'The current temperature can cause your heart problems to increase'
                    alerts.append(al)
            if num == 5:
                if currentconditions.get('temp') <= 50: 
                    al = 'The current temperature can cause your diabetes issues to increase'
                    alerts.append(al)
                if currentconditions.get('pressure') < 1013.0:
                    al = 'The current atmospheric pressure can cause your diabetes issues to increase'
                    alerts.append(al)
            
        
        return alerts
    @classmethod
    def idname(cls, username):
        em = UsersHealth.query.filter(UsersHealth.username == username).all()
        y = UsersHealth.query.filter_by(username=username)
        usersinfo = []
        x = db.session.query(UsersHealth.healthissues_id, UsersHealth.username).filter(UsersHealth.username == username).all()
        for i in x:
            for index in i:
                if type(index) is int:
                    usersinfo.append(index)

        return usersinfo
