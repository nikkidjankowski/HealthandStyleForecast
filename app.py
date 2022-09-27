from email.headerregistry import Address
from http.client import responses
import os
from flask import Flask, render_template, request, flash, redirect, session, g, abort
from sqlalchemy import null
#from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from survey import health_survey as survey
import requests
from models import Users, HealthIssues, Forecasts, Outfits, Locations, UsersHealth, db, connect_db
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
FAV_KEY = "fav"
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


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
    if RESPONSES_KEY in session:
        del session[RESPONSES_KEY]
        
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

        return redirect("/profile")

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

@app.route('/logout')
def logout():
    """Handle logout of user."""
    do_logout()
    flash("goodbye")

    return redirect("/login")

@app.route('/')
def home():
    
    return render_template("welcome.html")


@app.route('/home')
def show_forecast_form():
    loco = (Locations
                    .query
                    .filter(Locations.username == g.user.username)
                    .all())
    if len(loco) == 0:
        return render_template('homeerror.html')
    else:
        if g.user:
            user = g.user
            locations = (Locations
                        .query
                        .filter(Locations.username == user.username)
                        .all())
            currents = []

            for i in locations:
                current = Forecasts.getConditions(i.address)
                currents.append(current)
            u = db.session.query(UsersHealth.healthissues_id,UsersHealth.issue).filter(UsersHealth.username == user.username).all()
           


            firstforecast = currents[0]
            dieases = []
         
            for i in u:
                test = dict(i)

                new = {
                        test.get('healthissues_id') : test.get('issue')
                    }
                dieases.append(new)
          
            count = 0
            currenthealth = []
            outfits = []
       
            if len(currents) == 1:
                currentconditionshealth = UsersHealth.warning(user.username, dieases, firstforecast)
                clothes = Outfits.whattowear(user.username, firstforecast)
                currenthealth.append(currentconditionshealth)
                print(len(currenthealth))
                for i in currenthealth:
                
                    if len(i) == 1:
                        currenthealth.remove(i)
                if len(currenthealth) == 0:
                    currenthealth = 0
                return render_template("home.html", clothes=clothes, currenthealth=currenthealth, currentconditionshealth=currentconditionshealth, currents=currents, user=user, locations=locations)

            elif len(currents) > 1:
                while count <= (len(currents)-1):
                    currentconditionshealth = UsersHealth.warning(user.username, dieases, currents[count])
                    s = Outfits.whattowear(user.username, currents[count])
                    
                    currenthealth.append(currentconditionshealth)
                    outfits.append(s)
                    count = count + 1
                
                dieasesshown = list()
                #print(currenthealth, len(currenthealth))
               # print(currents, type(currents))
               # print(len(currenthealth), currents)
                for i in currenthealth:
                    #print(len(i))
                    if len(i) > 1:
                        dieasesshown.append(i) 
                #print(len(currenthealth))
                currenthealth = 0
                print(dieasesshown)
                return render_template("home.html", dieasesshown=dieasesshown, outfits=outfits, currentconditionshealth=currentconditionshealth, currents=currents, user=user, locations=locations)

            
            else:
                return render_template('homeerror.html')
            
            
            
          

@app.route('/profile')
def profile():
  
    if g.user:
        user = g.user
        locations = (Locations
                    .query
                    .filter(Locations.username == user.username)
                    .all())
        issues = (UsersHealth
                        .query
                        .filter(UsersHealth.username == user.username)
                        .all())

        health = (HealthIssues
                        .query
                        .filter(HealthIssues.id == UsersHealth.healthissues_id, UsersHealth.username == user.username)
                        .all())
     
        usersizehealth = len(issues)
    
    
      
           
       # y = UsersHealth.warning(user.username, dieases)


  #health=health,


        return render_template("users/profile.html",health=health, usersizehealth=usersizehealth, issues=issues, user=user, locations=locations, survey=survey)

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


@app.route('/locations/<int:locations_id>', methods=["GET"])
def messages_show(locations_id):
    """Show a message."""
    user = g.user
    location = Locations.query.get_or_404(locations_id)
    x = requests.get(f"{API_BASE_URL}/{location.address}/today?unitGroup=us&include=hours&elements=datetime,temp,feelslike,humidity,dew,precip,precipprob,snow,snowdepth,preciptype,windgust,windspeed,winddir,pressure,visibility,cloudcover,solarradiation,solarenergy,uvindex,severerisk,conditions,icon",
                params={'key': key})

    y = x.json()
   
    liststuff = y.get('days')
    address = location.address
    info = []
    testfunc = Forecasts.getforecast(address)
    #db.session.commit()
    current = Forecasts.getConditions(address)
  
    for data in liststuff:
         
        for deets in data:
            
            if deets == "hours":
            
                hourdata = data.get(deets)
            elif deets == "datetime":
                date = data.get(deets)
      

    return render_template('locations/show.html', date=date, hourdata=hourdata, y=y, user=user, location=location, liststuff=liststuff)


@app.route('/locations/<int:locations_id>/delete', methods=["POST"])
def location_destroy(locations_id):
    """Delete a message."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    loc = Locations.query.get_or_404(locations_id)
    

    db.session.delete(loc)
    db.session.commit()

    return redirect("/profile")

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
    user = g.user
    responses = session.get(RESPONSES_KEY)

    if (responses is None):
        # trying to access question page too soon
        return redirect("/")
    if(len(responses) == len(survey.questions)):
        x = UsersHealth.userhealth(session["responses"],user.username)
        db.session.commit()
        return redirect("/profile")
    if(len(responses) != qid):
        flash(f"Invalid question id: {qid}.")
        return redirect(f"/questions/{len(responses)}")
    question = survey.questions[qid]
    return render_template("question.html", q_num=qid, question=question, survey=survey)

   
@app.route("/answer", methods=["POST"])
def answers():
    
    choice = request.form['answer']
    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses
    
    return redirect(f"/questions/{len(responses)}")

@app.route("/done")
def finished():
    
    return render_template("done.html", survey=survey)

 
@app.route('/whattowear')
def whattowear():
    if g.user:
        user = g.user
        locations = (Locations
                    .query
                    .filter(Locations.username == user.username)
                    .all())
        currents = []
        for i in locations:
            current = Forecasts.getConditions(i.address)
            currents.append(current)
        u = db.session.query(UsersHealth.healthissues_id,UsersHealth.issue).filter(UsersHealth.username == user.username).all()
        #x = UsersHealth.warning(session["responses"],user.username)
       

     
        dieases = []
        for i in u:
            test = dict(i)

            new = {
                    test.get('healthissues_id') : test.get('issue')
                }
            dieases.append(new)
    
     
        #currentconditionshealth = UsersHealth.warning(user.username, dieases, currents[0])           
        count = 0
        currenthealth = []
        outfits = []
        if len(currents) == 1:
            currentconditionshealth = UsersHealth.warning(user.username, dieases, currents[0])
            clothes = Outfits.whattowear(user.username, currents[0])
            return render_template("whattowear.html", user=user, outfits=outfits, clothes=clothes)
        elif len(currents) > 1:
            while count <= (len(currents)-1):
                currentconditionshealth = UsersHealth.warning(user.username, dieases, currents[count])
                s = Outfits.whattowear(user.username, currents[count])
                currenthealth.append(currentconditionshealth)
                outfits.append(s)
                count = count + 1

      
        for i in currenthealth:
            if len(i) == 1:
                currenthealth.remove(i)
           

        firstlocation = currents[0].get('address')
        return render_template("whattowear.html", user=user, outfits=outfits)

@app.route('/healthissues')
def healthissues():
    if g.user:
        user = g.user
        locations = (Locations
                    .query
                    .filter(Locations.username == user.username)
                    .all())
        currents = []
        for i in locations:
            current = Forecasts.getConditions(i.address)
            currents.append(current)
        u = db.session.query(UsersHealth.healthissues_id,UsersHealth.issue).filter(UsersHealth.username == user.username).all()
        
       

     
        dieases = []
        for i in u:
            test = dict(i)

            new = {
                    test.get('healthissues_id') : test.get('issue')
                }
            dieases.append(new)
    
             
        count = 0
        currenthealth = []
        outfits = []
        if len(currents) == 1:
            currentconditionshealth = UsersHealth.warning(user.username, dieases, currents[0])
            clothes = Outfits.whattowear(user.username, currents[0])
            currenthealth.append(currentconditionshealth)
                
            for i in currenthealth:
                
                if len(i) == 1:
                    currenthealth.remove(i)
                return render_template("issues.html", user=user, currenthealth=currenthealth)
        elif len(currents) > 1:
            while count <= (len(currents)-1):
                currentconditionshealth = UsersHealth.warning(user.username, dieases, currents[count])
                s = Outfits.whattowear(user.username, currents[count])
                currenthealth.append(currentconditionshealth)
                outfits.append(s)
                count = count + 1
            dieasesshown = list()
                #print(currenthealth, len(currenthealth))
               # print(currents, type(currents))
               # print(len(currenthealth), currents)
            for i in currenthealth:
                    #print(len(i))
                if len(i) > 1:
                    dieasesshown.append(i)
                    currenthealth = 0 

        
           

        firstlocation = currents[0].get('address')
        return render_template("issues.html", user=user, dieasesshown=dieasesshown, currenthealth=currenthealth)