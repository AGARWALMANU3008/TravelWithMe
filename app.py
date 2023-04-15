from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

app=Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

class TRAVELLORS(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100))
    email=db.Column(db.String(200))
    destination=db.Column(db.String(200))
    month=db.Column(db.String(20))

class HOUSING(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    location=db.Column(db.String(100))
    cost=db.Column(db.Integer)
    rooms=db.Column(db.Integer)
    description=db.Column(db.String(20))

with app.app_context():
    db.create_all()
    
@app.route("/",methods=["GET","POST"])
def buddies():
    if request.method=="POST":
        loc=request.form["destination"]
        month=request.form["month"]
        name=request.form["name"]
        email=request.form["email"]
        buddy = TRAVELLORS(destination=loc, name=name, email=email, month=month)
        db.session.add(buddy)
        db.session.commit()

    all_buddies = TRAVELLORS.query.all() 
    return render_template("home.html",all_buddies=all_buddies)


@app.route("/host",methods=["POST","GET"])

def list_housing():
    
    if request.method=="POST":
        loc=request.form["location"]
        desc=request.form["description"]
        rooms=request.form["rooms"]
        cost=request.form["cost"]
        house=HOUSING(location=loc,description=desc,rooms=rooms,cost=cost)
        db.session.add(house)
        db.session.commit()
    return render_template("host.html")


@app.route("/lookup",methods=["POST","GET"])

def look_housing():
    houses=HOUSING.query.all()
    return render_template("lookup.html",houses=houses)
    
if __name__=="__main__":
    app.run()