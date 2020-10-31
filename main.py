from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
import json
from flask_marshmallow import Marshmallow


app = Flask(__name__)
ma = Marshmallow(app)

CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Danidoaidoos@1@localhost/Hotel'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    firstname = db.Column(db.String(80),  nullable=False)
    lastname = db.Column(db.String(80),  nullable=False)
    telephone = db.Column(db.String(10),  nullable=False)
    password = db.Column(db.String(10),  nullable=False)

    def __repr__(self):
        return '<User %r>' % self.email


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    firstname = db.Column(db.String(80),  nullable=False)
    lastname = db.Column(db.String(80),  nullable=False)
    address = db.Column(db.String(80),  nullable=False)
    telephone = db.Column(db.String(20),  nullable=False)
    start = db.Column(db.DateTime, nullable=True)
    stop = db.Column(db.DateTime, nullable=True)
    price = db.Column(db.Float, nullable=False)
    roomType= db.Column(db.String(80),  nullable=False)

class BookingSchema(ma.Schema):
    class Meta:
        model = Booking
        fields = ("id","firstname","lastname","email","start","stop","telephone","price","roomType","address")




db.create_all()


@app.route("/booking", methods=["POST", "GET"])
def booking():
    if(request.method == "POST"):
        try:
            data = request.get_json()
            book = Booking(firstname=data["firstname"], lastname=data["lastname"],
                           email=data["email"], address=data["address"], telephone=data["telephone"], start=data["start"],
                           stop=data["stop"], price=data["price"],roomType=data["roomType"])
            db.session.add(book)
            db.session.commit()
            info = Booking.query.all()
            print(info[0].firstname)
            booking_schema = BookingSchema(many=True)
            output = booking_schema.dump(info)
            return jsonify({"message": "Successfull", "success":True,"booking":output})
        except Exception as err:
            print(err)
            return jsonify({"message": "Error occured", "success": False})
    else:
        try:
            data =[]
            info = Booking.query.all()
            booking_schema = BookingSchema(many=True)
            output = booking_schema.dump(info)
            # print(output)
            return jsonify(output)
        except Exception as err:
            print(err)
            return jsonify({"message": "Error occured", "success": False})

@app.route("/booking/<id>",methods=["DELETE"])
def checkout(id):
    try:
        me = Booking.query.filter_by(id=id).first()
        db.session.delete(me)
        db.session.commit()
        info = Booking.query.all()
        booking_schema = BookingSchema(many=True)
        output = booking_schema.dump(info)

        return jsonify(output)

    except Exception as err:
        print(err)
        return jsonify({"message": "Error occured", "success": False})

@app.route("/signup", methods=["POST"])
def signup():
    try:
        data = request.get_json()
        user = User(email=data["email"],
                    firstname=data["firstname"], lastname=data["lastname"], telephone=data["telephone"], password=data["password"])
        db.session.add(user)
        db.session.commit()
        return jsonify({"registered": True, "logged": True})
    except Exception as err:
        print(err)
        return jsonify({"message": "Error occured", "exist": True, "logged": False})


@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        user = User.query.filter_by(email=data["email"]).first()
        print(user)
        if user is None:
            return jsonify({"message": "Account doesn't exist", "exist": False, "logged": False})
        else:
            if(data["password"] == user.password):
                info = {
                    "firstname": user.firstname,
                    "lastname": user.lastname,
                    "email": user.email,
                    "password": user.password,
                    "telephone": user.telephone
                }
                return jsonify({"registered": True, "logged": True, **info, "invalid": False, "exist": True})
            else:
                return jsonify({"message": "Invalid email or password", "invalid": True, "exist": True, "logged": False})

    except Exception as err:
        print(err)
        return jsonify({"message": "Error occured"})


if __name__ == "__main__":
    app.run(debug=True)
