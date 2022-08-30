from email.headerregistry import Address
from http.client import responses
import os
from flask import Flask, render_template, request, flash, redirect, session, g, abort
#from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from survey import health_survey as survey
import requests
from models import Users, HealthIssues, Forecasts, Outfits, Locations, db, connect_db
from forms import UserAddForm, LoginForm, LocationForm, HealthForm

CURR_USER_KEY = "curr_user"

##/address/datetime?unitGroup=us&key
API_BASE_URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"

key = 'ZX7VPUYV36DXTCEP46UQJ6JD6'

RESPONSES_KEY = "responses"
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///healthstyleforecast'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
answerss = []
dieases = ["asthma and allergies","headaches","diabetes","arthritis","heart problems"]
connect_db(app)
db.create_all()


###########################################################################################
#sign up login

@app.before_request
def add_user_to_g():
    
    
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = Users.query.get(session[CURR_USER_KEY])

    else:
        g.user = None

def do_login(user):
    session[CURR_USER_KEY] = user.username

@app.route('/signup', methods=["GET", "POST"])
def signup():
    form = UserAddForm()
    if form.validate_on_submit():
        try:
            user = Users.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
            )
            db.session.commit()
        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('users/signup.html', form=form)

        do_login(user)

        return redirect("/home")

    else:
        return render_template('users/signup.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/home")

        flash("Invalid credentials.", 'danger')
    
    return render_template('users/login.html', form=form)

@app.route('/')
def home():
    
    return render_template("welcome.html")


@app.route('/home')
def show_forecast_form():
    if g.user:
        user = g.user
        locations = (Locations
                    .query
                    .all())
   
    return render_template("home.html", user=user, locations=locations)

@app.route('/forecast')
def get_forecast():
    address = request.args["address"]
    x = requests.get(f"{API_BASE_URL}/{address}/today?unitGroup=us",
                params={'key': key,"include": "current","elements": "conditions","elements": "description","elements": "feelslike"})

    y = x.json()
  

    return render_template("showforecast.html", y=y, address=address)        

    


@app.route('/30dayforecast')
def get_30dayforecast():
    address = request.args["address"]
    x = requests.get(f"{API_BASE_URL}/{address}/next30days?unitGroup=us",
                params={'key': key,"include": "current","include": "days","elements": "conditions","elements": "datetime","elements": "feelslike"})

    y = x.json()
    return render_template("30dayforecast.html", y=y, address=address)

@app.route('/profile')
def profile():
    if g.user:
        user = g.user
        locations = (Locations
                    .query
                    .all())
    #print(session["responses"])
    arr = session["responses"]
    print(arr)
    dicc = dict(zip(dieases, arr))
    print(dicc)


    return render_template("users/profile.html", dicc=dicc, answerss=answerss, user=user, locations=locations, survey=survey)

@app.route('/addlocation', methods=["GET", "POST"])
def location():
    user = g.user
    form = LocationForm()

    if form.validate_on_submit():
        location = Locations(address=form.address.data)
        user.locations.append(location)
        db.session.commit()
      
        return redirect('/profile')
    
    return render_template("locations/new.html", user=user, form=form)

#@app.route('/addresslist')
#def list():
@app.route('/locations/<int:locations_id>', methods=["GET"])
def messages_show(locations_id):
    """Show a message."""
    user = g.user
    location = Locations.query.get_or_404(locations_id)
    x = requests.get(f"{API_BASE_URL}/{location.address}/today?unitGroup=us&include=hours&elements=datetime,temp,feelslike,humidity,dew,precip,precipprob,snow,snowdepth,preciptype,windgust,windspeed,winddir,pressure,visibility,cloudcover,solarradiation,solarenergy,uvindex,severerisk,conditions,icon",
                params={'key': key})

    y = x.json()
    print(location.address)
    liststuff = y.get('days')
   # hi = day.get('hours')
    info = []

    for data in liststuff:
         
        for deets in data:
            
            if deets == "hours":
                print(type(deets))
                hourdata = data.get(deets)
            elif deets == "datetime":
                date = data.get(deets)
            #print(deets) #name
            #print(hour.get(deets)) #value
    

    #print(info)
    return render_template('locations/show.html', date=date, hourdata=hourdata, y=y, user=user, location=location, liststuff=liststuff)


    #https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/SanDiego,CA//today?unitGroup=us&include=current&elements=description,conditions&key=ZX7VPUYV36DXTCEP46UQJ6JD6
    


    #https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/SanDiego,CA/next7days?unitGroup=us&key=ZX7VPUYV36DXTCEP46UQJ6JD6&include=days
    #https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/SanDiego,CA/today?unitGroup=us&key=ZX7VPUYV36DXTCEP46UQJ6JD6&include=hours


@app.route('/addhealth', methods=["GET", "POST"])
def addhealth():
    user = g.user
    form = HealthForm()

    if form.validate_on_submit():
        healthissue = HealthIssues(name=form.name.data,
                                    description=form.description.data,)
        user.healthissues.append(healthissue)
        db.session.commit()
      
        return redirect('/profile')
    
    return render_template("locations/new.html", user=user, form=form)


@app.route("/start", methods=["POST"])
def survey_todo():
    
    session[RESPONSES_KEY] = []
    return redirect("/questions/0")



@app.route("/questions/<int:qid>")
def show_question(qid):
    
    responses = session.get(RESPONSES_KEY)

    if (responses is None):
        # trying to access question page too soon
        return redirect("/")
    if(len(responses) == len(survey.questions)):
        
        for i in responses:
            answerss.append(i)
        print(answerss)
        return redirect("/profile")
    if(len(responses) != qid):
        flash(f"Invalid question id: {qid}.")
        return redirect(f"/questions/{len(responses)}")
    question = survey.questions[qid]
    return render_template("question.html", q_num=qid, question=question, survey=survey, responses=responses)

   
@app.route("/answer", methods=["POST"])
def answers():
    
    choice = request.form['answer']
    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses
    
    return redirect(f"/questions/{len(responses)}")

@app.route("/done")
def finished():
    
    return render_template("done.html", survey=survey, responses=responses)