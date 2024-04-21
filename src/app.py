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
from models import db, Users,Planets,Characters,Favorite
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

# Endpoint GET All Users
@app.route('/users', methods = ['GET'])
def handle_user():
    response_body = {}
    users = Users.query.all()
    response_body['results'] = [row.serialize() for row in users]
    response_body['message'] = 'Method GET Users'
    return jsonify (response_body),200


# Endpoint GET All Characters
@app.route('/people', methods=['GET'])
def handle_character():
    response_body = {}
    characters = Characters.query.all()
    response_body['results'] = [row.serialize() for row in characters]
    response_body['message'] = 'Method GET characters'
    return jsonify(response_body), 200

# Endpoint GET Character by ID
@app.route ('/people/<int:people_id>', methods = ['GET'])
def handle_character_id(people_id): 
    response_body = {}
    character = Characters.query.get(people_id)
    if not character:
         raise APIException('Character does not exist', status_code=400)
    response_body ['results'] = [character.serialize()]
    response_body['message'] = 'Method GET by ID an character'
    return jsonify (response_body) , 200

# Endpoint GET All Planets
@app.route('/planets', methods=['GET'])
def handle_planet():
    response_body = {}
    planets = Planets.query.all()
    response_body['results'] = [row.serialize() for row in planets]
    response_body['message'] = 'Method GET planets'
    return jsonify(response_body), 200

# Endpoint GET planets by ID
@app.route ('/planets/<int:planet_id>', methods = ['GET'])
def handle_planet_id(planet_id): 
    response_body = {}
    planet = Planets.query.get(planet_id)
    if not planet:
         raise APIException('Planet does not exist', status_code=400)
    response_body ['results'] = [planet.serialize()]
    response_body['message'] = 'Method GET by ID an planet'
    return jsonify (response_body) , 200

# Endpoint GET User Favorite
@app.route ('/users/<int:user_id>/favorite', methods = ['GET'])
def handle_favorite(user_id):
    response_body = {}
    user = Users.query.get(user_id)
    if not user:
        raise APIException('User does not exist', status_code=400)
    favorite = Favorite.query.filter_by(user_id=user_id)
    response_body['results'] = [row.serialize() for row in favorite]
    response_body['message'] = 'Method GET favorites'
    return jsonify(response_body), 200

# Endpoint Add Character to favorite
@app.route ('/users/<int:user_id>/favorite/character/<int:people_id>', methods = ['POST'])
def handle_add_character_favorite(user_id,people_id):
    user = Users.query.get(user_id)
    if not user:
        raise APIException('User does not exist', status_code=400)
    character = Characters.query.get(people_id)
    if not character:
        raise APIException('Character does not exist', status_code=400)
    favorite = Favorite (user_id = user_id , character_id = people_id)
    db.session.add(favorite)
    db.session.commit()
    response_body = {'msg': 'Character added in favorite'}
    return jsonify(response_body), 200

# Endpoint Add Planet to favorite
@app.route ('/users/<int:user_id>/favorite/planet/<int:planet_id>', methods = ['POST'])
def handle_add_planet_favorite(user_id, planet_id):
    user = Users.query.get(user_id)
    if not user:
        raise APIException('User does not exist', status_code=400)
    planet = Planets.query.get(planet_id)
    if not planet:
        raise APIException('Planet does not exist', status_code=400)
    favorite = Favorite (user_id = user_id , planet_id = planet_id)
    db.session.add(favorite)
    db.session.commit()
    response_body = {'msg': 'Planet added in favorite'}
    return jsonify(response_body), 200

# Endpoint Delete Character in Favorite
@app.route ('/users/<int:user_id>/favorite/character/<int:people_id>', methods = ['DELETE'])
def handle_delete_character(user_id,people_id):
    character_deleted = Favorite.query.filter_by(user_id = user_id , character_id = people_id).first()
    if not character_deleted:
        raise APIException('Character or user does not exist', status_code=400)
    db.session.delete(character_deleted)
    db.session.commit()
    response_body = {'msg':'Character deleted'}
    return jsonify (response_body) , 200

# Endpoint Delete Planet in Favorite
@app.route ('/users/<int:user_id>/favorite/planet/<int:planet_id>', methods = ['DELETE'])
def handle_delete_planet(user_id,planet_id):
    planet_deleted = Favorite.query.filter_by(user_id = user_id , planet_id = planet_id).first()
    if not planet_deleted:
        raise APIException('Planet or user does not exist', status_code=400)
    db.session.delete(planet_deleted)
    db.session.commit()
    response_body = {'msg':'Planet deleted'}
    return jsonify (response_body) , 200

# Endpoint Post Planet
@app.route ('/planets', methods=['POST'])
def handle_create_planet():
    data = request.json
    if 'name' not in data or 'climate' not in data or 'diameter' not in data or 'planetDesc' not in data or 'rotation_period' not in data or 'orbital_period' not in data or 'gravity' not in data or 'population' not in data or 'terrain' not in data or 'surface_water' not in data:
        raise APIException('Some fields are missing', status_code=400)
    new_planet = Planets(
        name=data['name'],
        climate=data['climate'],
        diameter=data['diameter'],
        planetDesc=data['planetDesc'],
        rotation_period=data['rotation_period'],
        orbital_period=data['orbital_period'],
        gravity=data['gravity'],
        population=data['population'],
        terrain=data['terrain'],
        surface_water=data['surface_water']
    )
    db.session.add(new_planet)
    db.session.commit()
    return jsonify(new_planet.serialize()), 201

# Endpoint Put Planet
@app.route ('/planets/<int:planet_id>', methods = ['PUT'])
def update_planet(planet_id):
    planet = Planets.query.get(planet_id)
    if not planet:
         raise APIException('Planet does not exist', status_code=400)
    data = request.json
    if 'name' in data:
        planet.name = data['name']
    if 'climate' in data:
        planet.climate = data['climate']
    if 'diameter' in data:
        planet.diameter = data['diameter']
    if 'planetDesc' in data:
        planet.planetDesc = data['planetDesc']
    if 'rotation_period' in data:
        planet.rotation_period = data['rotation_period']
    if 'orbital_period' in data:
        planet.orbital_period = data['orbital_period']
    if 'gravity' in data:
        planet.gravity = data['gravity']
    if 'population' in data:
        planet.population = data['population']
    if 'terrain' in data:
        planet.terrain = data['terrain']
    if 'surface_water' in data:
        planet.surface_water = data['surface_water']
    
    db.session.commit()

    return jsonify({'message': 'Planet updated successfully'}), 200

# Endpoint Delete Planet
@app.route ('/planets/<int:planet_id>', methods = ['DELETE'])
def delete_planet(planet_id):
    planet_deleted = Planets.query.filter_by(id = planet_id).first()
    if not planet_deleted:
        raise APIException('Planet does not exist', status_code=400)
    db.session.delete(planet_deleted)
    db.session.commit()
    response_body = {'msg':'Planet deleted'}
    return jsonify (response_body) , 200

# Endpoint Post Character
@app.route ('/people', methods=['POST'])
def handle_create_character():
    data = request.json
    if 'name' not in data or 'birth_year' not in data or 'eye_color' not in data or 'characterDesc' not in data or 'height' not in data or 'mass' not in data or 'gender' not in data or 'hair_color' not in data or 'skin_color' not in data:
        raise APIException('Some fields are missing', status_code=400)
    new_character = Characters(
        name=data['name'],
        birth_year=data['birth_year'],
        eye_color=data['eye_color'],
        characterDesc=data['characterDesc'],
        height=data['height'],
        mass=data['mass'],
        gender=data['gender'],
        hair_color=data['hair_color'],
        skin_color=data['skin_color'],
    )
    db.session.add(new_character)
    db.session.commit()
    return jsonify(new_character.serialize()), 201

# Endpoint Put Character
@app.route ('/people/<int:people_id>', methods = ['PUT'])
def update_character(people_id):
    character = Characters.query.get(people_id)
    if not character:
         raise APIException('Character does not exist', status_code=400)
    data = request.json
    if 'name' in data:
        character.name = data['name']
    if 'birth_year' in data:
        character.birth_year = data['birth_year']
    if 'eye_color' in data:
        character.eye_color = data['eye_color']
    if 'characterDesc' in data:
        character.characterDesc = data['characterDesc']
    if 'height' in data:
        character.height = data['height']
    if 'mass' in data:
        character.mass = data['mass']
    if 'gender' in data:
        character.gender = data['gender']
    if 'hair_color' in data:
        character.hair_color = data['hair_color']
    if 'skin_color' in data:
        character.skin_color = data['skin_color']
    
    db.session.commit()

    return jsonify({'message': 'Character updated successfully'}), 200

# Endpoint Delete Character
@app.route ('/people/<int:people_id>', methods = ['DELETE'])
def delete_character (people_id):
    character_deleted = Characters.query.filter_by(id = people_id).first()
    if not character_deleted:
        raise APIException('Character does not exist', status_code=400)
    db.session.delete(character_deleted)
    db.session.commit()
    response_body = {'msg':'Character deleted'}
    return jsonify (response_body) , 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
