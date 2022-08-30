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

{% if user.id == g.user.id %}
              <form method="POST" action="/messages/{{ msg.id }}/like" class="messages-like">
                <button class="
                  btn 
                  btn-sm 
                  {{'btn-primary'}}"
                >
                  <i class="fa fa-thumbs-up"></i> 
                </button>
              </form>
              {% endif %}