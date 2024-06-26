from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model):
    __table_name__='users'
    id = db.Column(db.Integer, primary_key=True)
    user_name= db.Column(db.String(30),unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    
    def __repr__(self):
        return f'<User %r>' % self.user_name

    def serialize(self):
        return {
            "id": self.id,
            "user_name":self.user_name,
            "email": self.email,
        }
    
class Planets (db.Model):
    __table_name__='planets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    climate = db.Column(db.String(50), nullable=False)
    diameter = db.Column (db.String(20), nullable=False)
    planetDesc = db.Column (db.String(250), nullable=False)
    rotation_period = db.Column (db.String(20), nullable=False)
    orbital_period = db.Column (db.String(20), nullable=False)
    gravity = db.Column (db.String(20), nullable=False)
    population = db.Column (db.String(20), nullable=False)
    terrain = db.Column (db.String(20), nullable=False)
    surface_water = db.Column (db.String(20), nullable=False)

    def __repr__(self):
        return f'<Planet %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name":self.name,
            "climate": self.climate,
            "diameter": self.diameter,
            "planetDesc": self.planetDesc,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "gravity": self.gravity,
            "population": self.population,
            "terrain": self.terrain,
            "surface_water": self.surface_water
        }
    
class Characters (db.Model):
    __table_name__ ='characters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    birth_year = db.Column(db.String(50))
    eye_color = db.Column (db.String(20))
    characterDesc=db.Column (db.String(250))
    height= db.Column(db.String(20))
    mass= db.Column(db.String(20))
    gender= db.Column(db.String(20))
    hair_color= db.Column(db.String(20))
    skin_color= db.Column(db.String(20))
    def __repr__(self):
        return f'<Character %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name":self.name,
            "birth_year": self.birth_year,
            "eye_color": self.eye_color,
            "characterDesc": self.characterDesc,
            "height": self.height,
            "mass": self.mass,
            "gender": self.gender,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color
        }

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship(Users)
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'))
    planet = db.relationship(Planets)
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'))
    character = db.relationship(Characters)
    

    def __repr__(self):
        return '<Favorite %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
            "character_id": self.character_id
        }
