import random

from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy

'''
Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy()
db.init_app(app)


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


# HTTP GET - Read Record
@app.route("/random", methods=["GET", "POST"])
def random_get():
    with app.app_context():
        all_cafes = db.session.execute(db.select(Cafe)).scalars().all()
        random_cafe = random.choice(all_cafes)
        list_of_variables = vars(random_cafe).pop('_sa_instance_state')
    return {random_cafe.name: vars(random_cafe)}
    # OR USE
    # return {column.name: getattr(self, column.name) for column in self.__table__.columns}


@app.route("/all")
def all():
    with app.app_context():
        all_cafes = db.session.execute(db.select(Cafe)).scalars().all()
        cafes_list = []
        for cafe in all_cafes:
            list_of_variables = vars(cafe).pop('_sa_instance_state')
            cafes_list.append(vars(cafe))
    return {"cafes": cafes_list}

# or
# @app.route("/all")
# def get_all_cafes():
#     result = db.session.execute(db.select(Cafe).order_by(Cafe.name))
#     all_cafes = result.scalars().all()
#     #This uses a List Comprehension but you could also split it into 3 lines.
#     return jsonify(cafes=[cafe.to_dict() for cafe in all_cafes])


@app.route("/search")
def search():
    location = request.args.get("loc")
    with app.app_context():
        all_cafes = db.session.execute(db.select(Cafe).where(Cafe.location == location)).scalars().all()
        if all_cafes == []:
            return "<h1>Sorry we don't have any cafes at that location.</h1>"
        else:
            cafes_list = []
            for cafe in all_cafes:
                list_of_variables = vars(cafe).pop('_sa_instance_state')
                cafes_list.append(vars(cafe))
            return {"cafes": cafes_list}


@app.route("/add", methods=["POST"])
def post_new_cafe():
    new_cafe = Cafe(
        name=request.form.get("name"),
        map_url=request.form.get("map_url"),
        img_url=request.form.get("img_url"),
        location=request.form.get("loc"),
        has_sockets=bool(request.form.get("sockets")),
        has_toilet=bool(request.form.get("toilet")),
        has_wifi=bool(request.form.get("wifi")),
        can_take_calls=bool(request.form.get("calls")),
        seats=request.form.get("seats"),
        coffee_price=request.form.get("coffee_price"),
    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={"success": "Successfully added the new cafe."})


@app.route("/update_price/<int:id>", methods=["PATCH"])
def update_price(id):
    required_record = db.session.get(Cafe, id)
    if required_record:
        required_record.coffee_price = request.args.get("new_price")
        db.session.commit()
        return jsonify(response={"success": "Successfully changed the price of the coffee."})
    else:
        return jsonify(error={"not_found": "Sorry a cafe with that id was not found in the database."}), 404


@app.route("/report-closed/<int:cafe_id>", methods=["DELETE"])
def delete_cafe(cafe_id):
    api_key = request.args.get("api_key")
    if api_key == "TopSecret":
        cafe = db.session.get(Cafe, cafe_id)
        if cafe:
            db.session.delete(cafe)
            db.session.commit()
            return jsonify(response={"success": "Successfully deleted the cafe from the database."}), 200
        else:
            return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."}), 404
    else:
        return jsonify(error={"Forbidden": "Sorry, that's not allowed. Make sure you have the correct api_key."}), 403


## HTTP POST - Create Record

## HTTP PUT/PATCH - Update Record

## HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True)
