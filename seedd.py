from app import app
from models import HealthIssues, Outfits, Users, UsersHealth, db, connect_db


db.drop_all()
db.create_all()

h1 = HealthIssues(
    name="Asthma and allergies",
    description="Thunder storms,Season change,Hot temp",
    weathereffects="rain, hot temp",
)
h2 = HealthIssues(
    name="Joint pain",
    description="Low barometric, low temperature, rain",
    weathereffects="if lower than 1013mb",
)

h3 = HealthIssues(
    name="Headaches",
    description="Low barometric, low temperature, rain",
    weathereffects="if lower than 1013mb",
)
h4 = HealthIssues(
    name="Heart attack",
    description="Temp drops a few degrees more at risk",
    weathereffects="cold",
)
h5 = HealthIssues(
    name="Diabetes",
    description="cold fronts, low pressure",
    weathereffects="if lower than 1013mb and cold",
)

u1 = Users(
    username ="nikkij",
    password ="Secret98",
    email = "nikkij@mail.com",
    first_name = "Nikki",
    last_name = "Jankowski",
)

o1 = Outfits(
    top ="Tank top or tshirt",
    bottom ="Shorts, skirt, or thin pants",
    accessories ="if sunny out bring a hat, flip flops or sneakers",
)
o2 = Outfits(
    top ="Sweater, turtleneck, longsleeve shirt",
    bottom ="pants",
    accessories ="grab a beanie, jacket, or scarf to stay more warm, sneakers, boots, or snow boots",
)
o3 = Outfits(
    top ="Tshirt, blouse, tank top",
    bottom ="pants, skirt, shorts if you can handle a little cold",
    accessories ="grab a jacket to prepare if the temp cools, sneakers",
)

db.session.add_all([h1,h2,h3,h4,h5,u1,o1,o2,o3])
db.session.commit()
#'btn-secondary' 