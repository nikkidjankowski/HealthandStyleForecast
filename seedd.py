from app import app
from models import HealthIssues, Users, db, connect_db


db.drop_all()
db.create_all()

h1 = HealthIssues(
    name="Asthma and allergies",
    description="Thunder storms,Season change,Hot temp",
    weathereffects="rain, hot temp",
)

h3 = HealthIssues(
    name="Headaches",
    description="Low barometric, low temperature, rain",
    weathereffects="if lower than 1013mb",
)
h4 = HealthIssues(
    name="Heart attack",
    description="Temp drops a few degrees more at risk",
    weathereffects=5,
)
h5 = HealthIssues(
    name="Diabetes",
    description="cold fronts, low pressure",
    weathereffects="if lower than 1013mb and cold",
)
h2 = HealthIssues(
    name="Joint pain",
    description="Low barometric, low temperature, rain",
    weathereffects="if lower than 1013mb",
)

u1 = Users(
    username ="nikkij",
    password ="Secret98",
    email = "nikkij@mail.com",
    first_name = "Nikki",
    last_name = "Jankowski",
)

db.session.add_all([h1,h2,h3,h4,h5,u1])
db.session.commit()
#'btn-secondary' 