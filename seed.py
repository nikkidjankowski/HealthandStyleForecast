from app import app
from models import Users, HealthIssues, Forecasts, Outfits, Locations, db, connect_db

db.drop_all()
db.create_all()

u1 = Users(
    username ="nikkij",
    password = "12345",
    email ="nikkij@email.com",
    first_name = "nikki",
    last_name = "jankowski",
    )

l1 = Locations(
    address="San Diego, CA",
    username="nikkij",
)



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


@classmethod
def getforecast(cls, address):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """
        API_BASE_URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"

        key = 'ZX7VPUYV36DXTCEP46UQJ6JD6'
        req = requests.get(f"{API_BASE_URL}/{address}/today?unitGroup=us&include=hours&elements=datetime,temp,feelslike,humidity,dew,precip,precipprob,snow,snowdepth,preciptype,windgust,windspeed,winddir,pressure,visibility,cloudcover,solarradiation,solarenergy,uvindex,severerisk,conditions,icon",
                params={'key': key})



   
      

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

    @classmethod
    def getforecast(cls, address):
        dayarray = []
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
                            for u in i:
                                print(u)
        forecast = Forecasts(
            datetime=datetime,
            temp=temp,
            feelslike=feelslike,
            humidity=humidity,
            dew=dew,
            precip=precip,
            precipprob=precipprob,
            snow=snow,
            snowdepth=snowdepth,
            preciptype=preciptype,
            windgust=windgust,
            windspeed=windspeed,
            winddir=winddir,
            pressure=pressure,
            visibility=visibility,
            cloudcover=cloudcover,
            solarradiation=solarradiation,
            solarenergy=solarenergy,
            uvindex=uvindex,
        )



                                
        forecast = Forecasts(
            datetime=datetime,
            temp=temp,
            feelslike=feelslike,
            humidity=humidity,
            dew=dew,
            precip=precip,
            precipprob=precipprob,
            snow=snow,
            snowdepth=snowdepth,
            preciptype=preciptype,
            windgust=windgust,
            windspeed=windspeed,
            winddir=winddir,
            pressure=pressure,
            visibility=visibility,
            cloudcover=cloudcover,
            solarradiation=solarradiation,
            solarenergy=solarenergy,
            uvindex=uvindex,
        )
  

        db.session.add(user)