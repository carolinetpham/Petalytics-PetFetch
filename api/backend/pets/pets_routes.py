########################################################
# Sample pets blueprint of endpoints
# Remove this file if you are not using it in your project
########################################################
from flask import Blueprint, request, jsonify, make_response, current_app
import json
from backend.db_connection import db

pets = Blueprint('pets', __name__)

# Get all pets from the DB
@pets.route('/pets', methods=['GET'])
def get_pets():
    current_app.logger.info('pets_routes.py: GET /pets')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT petID, name, adoption_status,\
        species, breed, birthday, age, is_alive FROM pets')

    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Add a new pet to the DB
@pets.route('/pets', methods=['POST'])
def add_pet():
    current_app.logger.info('POST /pets route')
    pet_info = request.json
    petID = pet_info['petID']
    name = pet_info['name']
    status = pet_info['adoption_status']
    species = pet_info['species']
    breed = pet_info['breed']
    birthday = pet_info['birthday']
    age = pet_info['age']
    alive = pet_info['is_alive']

    query = 'INSERT INTO pets (petID, name, adoption_status, species, breed, birthday, age, is_alive) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
    data = (petID, name, status, species, breed, birthday, age, alive)
    cursor = db.get_db().cursor()
    r = cursor.execute(query, data)
    db.get_db().commit()
    return 'pet added!'  

# Update a pet in the DB
@pets.route('/pets', methods=['PUT'])
def update_pets():
    current_app.logger.info('PUT /pets route')
    pet_info = request.json
    # current_app.logger.info(pet_info)
    petID = pet_info['petID']
    name = pet_info['name']
    status = pet_info['adoption_status']
    species = pet_info['species']
    breed = pet_info['breed']
    birthday = pet_info['birthday']
    age = pet_info['age']
    alive = pet_info['is_alive']


    query = 'UPDATE pets SET name = %s, adoption_status = %s, species = %s, breed = %s, birthday = %s,\
             age = %s, is_alive = %s WHERE petID = %s'
    data = (name, status, species, breed, birthday, age, alive, petID)
    cursor = db.get_db().cursor()
    r = cursor.execute(query, data)
    db.get_db().commit()
    return 'customer updated!'

# Get pet detail for a pet with particular petID
@pets.route('/pets/<petID>', methods=['GET'])
def get_pet(petID):
    current_app.logger.info('GET /pets/<petID> route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT name, adoption_status, species, breed, birthday, age, is_alive FROM pets WHERE petID = ' + str(petID))

    theData = cursor.fetchall()

    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response
# Get all avilable Pets for potention adopter viewing
@pets.route('/pets/available', methods=['GET'])
def get_available_pets():
    current_app.logger.info('pets_routes.py: GET /pets/available')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT petID, name,\
        species, breed, age FROM pets WHERE is_alive = 1 AND adoption_status = 0')

    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Gets contact information
@pets.route('pets/contact', methods=['Get'])
def get_pet_contacts():
    current_app.logger.info('pets_routes.py: GET /pets/contact')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * \
                   FROM pets \
                        NATURAL JOIN pet_agencies \
                        NATURAL JOIN agencies \
                   ORDER BY entryDate DESC'
        )

    theData = cursor.fetchall()
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response    

# Delete a pet from the DB
@pets.route('/pets/<petID>', methods=['DELETE'])
def delete_pet(petID):
    current_app.logger.info('DELETE /pets/<petID> route')
    cursor = db.get_db().cursor()
    cursor.execute('DELETE FROM pets WHERE petID = %s', (petID,))
    db.get_db().commit()

    the_response = make_response('Pet deleted!')
    the_response.status_code = 200
    the_response.mimetype = 'text/plain'
    return the_response

# Gets all unadopted pets after a certain date
@pets.route('pets/date/<date>', methods=['Get'])
def get_date_pets(date):
    current_app.logger.info('pets_routes.py: GET /pets/date/<date>')
    cursor = db.get_db().cursor()
    current_app.logger.info(str(date))
    cursor.execute("SELECT p.petID, p.name, p.species, p.breed, pa.entryDate, pa.exitDate, a.agencyName\
                    FROM pets p\
                    JOIN pet_agencies pa ON p.petID = pa.petID\
                    JOIN agencies a ON pa.agencyID = a.agencyID\
                    WHERE pa.exitDate IS NULL\
                    AND pa.entryDate > %s",date)

    theData = cursor.fetchall()
    current_app.logger.info(theData)
    the_response = make_response(theData)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response   