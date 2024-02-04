from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    favorite = db.relationship("Favorite", backref= "user")   


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
        }

class People(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(150), nullable = False)
    height = db.Column(db.Integer, nullable = False)
    mass = db.Column(db.Integer, nullable = False)
    hair_color = db.Column(db.String(100), nullable = False)
    skin_color = db.Column(db.String(100), nullable = False)
    eye_color = db.Column(db.String(100), nullable = False)
    brth_year = db.Column(db.Date, nullable = False)
    create = db.Column(db.Date, nullable = False)
    edited = db.Column(db.Date, nullable = False)
    homeworld = db.Column(db.String(100), nullable = False)
    url = db.Column(db.String(200), nullable = False)
    description = db.Column(db.String(500), nullable = False)
    favorite = db.relationship("Favorite",backref= "people")
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "birth_year": self.brth_year,
            "create": self.create,
            "edited": self.edited,
            "homeworld": self.homeworld,
            "url": self.url,
            "desciption": self.description    
        }

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    diameter = db.Column(db.Integer, nullable = False)
    rotation_period = db.Column(db.Integer, nullable = False)
    orbital_period = db.Column(db.Integer, nullable = False)
    gravity = db.Column(db.Integer, nullable = False)
    population = db.Column(db.Integer, nullable = False )
    climate = db.Column(db.String(100), nullable = False )
    terrain = db.Column(db.String(100), nullable = False)
    surface_water = db.Column(db.String(100), nullable = False)
    creted = db.Column(db.Date, nullable = False)
    edited = db.Column(db.Date, nullable = False)
    name = db.Column(db.String(150), nullable = False)
    url = db.Column(db.String(150), nullable = False)
    description = db.Column(db.String(500), nullable = False)
    favorite = db.relationship("Favorite",backref= "planet")
    
    def serialize(self):
        return {
            "id": self.id,
            "diameter": self.diameter,
            "rotacion_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "gravity": self.gravity,
            "population": self.population,
            "climate": self.climate,
            "terain": self.terrain,
            "surface_water": self.surface_water,
            "create": self.creted,
            "edited": self.edited,
            "name": self.name,
            "url": self.url,
            "description": self.description,
        }


class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    people_id = db.Column(db.Integer, db.ForeignKey("people.id"), nullable=True)  
    planet_id = db.Column(db.Integer, db.ForeignKey("planet.id"), nullable=True)  
 

   
    