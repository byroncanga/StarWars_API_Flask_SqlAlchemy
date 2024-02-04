"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planet, Favorite
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def get_user():
    user_query =User.query.all()
    user_serialize = [user.serialize() for user in user_query]
    response_body = {
        "user": user_serialize
    }
    
    return jsonify(response_body),200
 
   
@app.route("/people", methods=["GET"])
def get_people():
    
    people_query = People.query.all()
    people_serialize = [people.serialize() for people in people_query]
    response_body = {
        "people": people_serialize
    }
    
    return jsonify(response_body), 200

@app.route("/people/<int:people_id>", methods=["GET"])
def get_people_id(people_id):
    
    people_filter = People.query.filter_by(id = people_id).one_or_none()
    
    if people_filter is None:
        return "People is not found"
    
    return jsonify({
        "people": [people_filter.serialize()]
    }), 201
    

@app.route("/favorite/people/<int:people_id>", methods=["POST"])
def people_favorite(people_id):
    
    body = request.json
    user_id = body.get("user_id", None)
    
    response = User.query.filter_by(id = user_id).one_or_none()
    if response == None:
        return jsonify({
            "error": "usuario es requerido"
        }), 400
        
    response_people = People.query.filter_by(id = people_id).one_or_none()
    if response_people == None:
        return jsonify({
            "error": "Personaje es requerido"
        }), 400
        
    existing_Favorite = Favorite.query.filter_by(user_id = user_id, people_id = people_id).first()
    if existing_Favorite:
        return jsonify({
            "error": "personaje ya esta agregado en favoritos"
        }), 400
        
    new_favorite = Favorite(user_id = user_id, people_id = people_id)
    
    db.session.add(new_favorite)
    try:
        db.session.commit()
        return "agregado correctamente"
    except Exception as error:
        db.session.rolback()
        return jsonify({"error": str(error)}), 500
    
    
@app.route("/planet", methods=["GET"])
def get_planet():
    
    planet_query = Planet.query.all()
    planet_serialize = [planet.serialize() for planet in planet_query]
    response_body = {
        "planet": planet_serialize
    }
    
    return jsonify(response_body), 200
    

@app.route("/planet/<int:planet_id>", methods=["GET"])
def get_planet_id(planet_id):
    
    planet_filter = Planet.query.filter_by(id = planet_id).one_or_none()
    
    if planet_filter is None:
        return "planet is not found"
    
    return jsonify({
        "planet": [planet_filter.serialize()]
    }), 201
    
@app.route("/favorite/planet/<int:planet_id>", methods = ["POST"])
def planet_favorite(planet_id):
    body = request.json
    user_id = body.get("user_id", None)
    response = User.query.filter_by(id = user_id).one_or_none()
    
    if response is None:
        return jsonify({"error": "user_id es requerido"}), 400
    
    response_planet = Planet.query.filter_by(id = planet_id).one_or_none()
    if response_planet is None:
        return jsonify({"error": "planeta es requerido"}), 400
    
    
    existing_favorite = Favorite.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if existing_favorite:
        return jsonify({"error": "Este planeta ya está en tus favoritos"}), 400

    new_favorite = Favorite(user_id=user_id, planet_id=planet_id)
    db.session.add(new_favorite)
    try:
        db.session.commit()
        return "favorito agregado"
    except Exception as error:
        db.session.rollback()
        print(error) 
        return jsonify({"error": str(error)}), 500 
    

@app.route("/favorite/planet/<int:planet_id>", methods = ["DELETE"])
def del_planet(planet_id):
    
    body = request.json
    user_id = body.get("user_id", None)
    
    user_filter = User.query.filter_by(id = user_id).one_or_none()
    if user_filter == None:
        return jsonify({
            "error": "usuario no encontrado"
        }), 401
    planet_filter = Planet.query.filter_by(id = planet_id).one_or_none()
    if planet_filter == None:
        return jsonify({
            "error": "planeta no encontrado"
        }), 400

    db.session.delete(planet_filter)
    
    try:
        db.session.commit()
        return jsonify({
            "status": "planeta borrado"
        }),200
    except Exception as error:
        db.session.rollback()
        return jsonify({
            "error": "error del servidor"
        }), 500
        

@app.route("/favorite/people/<int:people_id>", methods = ["DELETE"])
def del_people(people_id):
    
    body = request.json
    user_id = body.get("user_id", None)
    
    filter_user = User.query.filter_by(id = user_id).one_or_none()
    
    if filter_user == None:
        return jsonify({
            "error": "usuario no encontrado"
        }), 400

    filter_people = People.query.filter_by(id = people_id).one_or_none()
    
    if filter_people == None:
        return jsonify({
            "error": "Personaje no encontrado"
        }),400
    
    db.session.delete(filter_people)

    try:
        db.session.commit()
        return jsonify({
            "status": "Personaje eliminado"
        }),200
    except Exception as error:
        db.session.rolback()
        return jsonify({
            "error": "error de servidor"
        }), 500
    
    

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
   