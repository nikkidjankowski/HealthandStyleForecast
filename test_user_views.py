"""User View tests."""

# run these tests like:
#
#    FLASK_ENV=production python -m unittest test_user_views.py


import os
from unittest import TestCase
from flask import session
from models import Users, HealthIssues, Forecasts, Outfits, Locations, UsersHealth, db, connect_db

os.environ['DATABASE_URL'] = "postgresql:///healthstyleforecast"


# Now we can import app

from app import app, CURR_USER_KEY, healthissues


# Don't have WTForms use CSRF at all, since it's a pain to test

app.config['WTF_CSRF_ENABLED'] = False

class UserViewsTestCase(TestCase):
    """Tests for views of API."""

    def setUp(self):
        """Make demo data."""
        db.drop_all()
        db.create_all()
        
        self.client = app.test_client()

        self.testuser = Users.signup(username="usertest",
                                    email="test@test.com",
                                    password="testuser",
                                    first_name="user",
                                    last_name="test")
     
        
        self.weatherissue = {
            'address': 'San Diego,CA',
            'description': 'cold and rainy',
            'temp': 50,
            'pressure': 1000.0,
            'precipprob': 1.0,
        } 
        

    def setup_likes(self):
        self.location = Locations(address="San Diego, CA",username=self.testuser.username)
        self.health1 = HealthIssues(
            name="Asthma and allergies",
            description="Thunder storms,Season change,Hot temp",
            weathereffects="rain, hot temp"
                    )
        self.health2 = HealthIssues(
                    name="Joint pain",
                    description="Low barometric, low temperature, rain",
                    weathereffects="if lower than 1013mb",
                )
        self.health3 = HealthIssues(
                    name="Headaches",
                    description="Low barometric, low temperature, rain",
                    weathereffects="if lower than 1013mb"
                )
        self.health4 = HealthIssues(
                    name="Heart attack",
                    description="Temp drops a few degrees more at risk",
                    weathereffects="cold"
                )
        self.health5 = HealthIssues(
                    name="Diabetes",
                    description="cold fronts, low pressure",
                    weathereffects="if lower than 1013mb and cold"
                )
        self.outfit1 = Outfits(
                    top ="Tank top or tshirt",
                    bottom ="Shorts, skirt, or thin pants",
                    accessories ="if sunny out bring a hat, flip flops or sneakers",
                )
        self.outfit2 = Outfits(
                    top ="Sweater, turtleneck, longsleeve shirt",
                    bottom ="pants",
                    accessories ="grab a beanie, jacket, or scarf to stay more warm, sneakers, boots, or snow boots",
                )
        self.outfit3 = Outfits(
                    top ="Tshirt, blouse, tank top",
                    bottom ="pants, skirt, shorts if you can handle a little cold",
                    accessories ="grab a jacket to prepare if the temp cools, sneakers",
                )
        
        self.issue = UsersHealth(username=self.testuser.username,healthissues_id=2,issue="joint pain")
        db.session.add_all([self.issue,self.location,self.health1,self.health2,self.health3,self.health4,self.health5,self.outfit1,self.outfit2,self.outfit3])
        

        db.session.commit()

    def tearDown(self):
        """Clean up fouled transactions."""

        res = super().tearDown()
        db.session.rollback()
        return res

    def test_view_profile(self):
        self.setup_likes()
        health = HealthIssues.query.filter(HealthIssues.id==self.issue.healthissues_id).one()
        
        location = Locations.query.filter(Locations.username==self.location.username).one()
       
        with self.client as c:
            with c.session_transaction() as ses:
                ses['curr_user'] = "usertest" 
            resp = c.get("/profile")
            self.assertEqual(resp.status_code, 200)
            html = resp.data
            self.assertIn("Hello user test!", str(html))
            self.assertIn(health.name, str(html))
            self.assertIn(location.address, str(html))
            
         #   import pdb
         #   pdb.set_trace()
       # <li><b>{{ i.name }}</b></li>
        
    def test_view_home(self):
        self.setup_likes()
        health = HealthIssues.query.filter(HealthIssues.id==self.issue.healthissues_id).one()
        
        location = Locations.query.filter(Locations.username==self.location.username).one()
        with self.client as c:
            with c.session_transaction() as ses:
                ses['curr_user'] = "usertest" 
            resp = c.get("/home")
            html = resp.data
            self.assertEqual(resp.status_code,200)
            self.assertIn(location.address, str(html))
        #    import pdb
  # pdb.set_trace()
    
    

    def test_currentcondition_api(self):
        self.setup_likes()
        location = Locations.query.filter(Locations.username==self.location.username).one()
        currentweather = Forecasts.getConditions(location.address)
        clothes = Outfits.whattowear(self.testuser.username,currentweather)
        warn = HealthIssues.query.filter(HealthIssues.id==self.issue.healthissues_id).one()
        
        dieases = []
            

        new = {
                warn.id :warn.name 
            }
        dieases.append(new)
        
        print(clothes)
     
        with self.client as c:
            with c.session_transaction() as ses:
                ses['curr_user'] = "usertest" 
            resp = c.get("/home") 
            self.assertEqual(resp.status_code, 200)
            html = resp.data
            #weather = Forecasts.getforecast(location.address)
            
            self.assertIn(currentweather["address"],str(html))
            self.assertIn(currentweather["description"],str(html))
            self.assertIn(str(currentweather["temp"]),str(html))
            self.assertIn("The current atmospheric pressure can cause your Joint Pain to increase", str(html))
            self.assertIn(clothes[1], str(html))
            
            
            
    def test_profile_views(self):
        self.setup_likes()
        location = Locations.query.filter(Locations.username==self.location.username).one()
         
        
        health = (HealthIssues
                        .query
                        .filter(HealthIssues.id == UsersHealth.healthissues_id, UsersHealth.username == self.testuser.username)
                        .one())
        print(health)
        #healthissue = health[0].name
        with self.client as c:
            with c.session_transaction() as ses:
                ses['curr_user'] = "usertest" 
            resp = c.get("/profile") 
            self.assertEqual(resp.status_code, 200)
            html = resp.data
            self.assertIn(str(location.address),str(html))
    

