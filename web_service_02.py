__author__ = 'OTurki'

from DAO.GenericDAO import GenericDAO, GenericLocationDAO

from flask import Flask, jsonify, request
from bson.objectid import ObjectId

import json
import datetime


class MongoJsonEncoder(json.JSONEncoder):
    def default(self, objectToEncode):
        if isinstance(objectToEncode, (datetime.datetime, datetime.date)):
            return objectToEncode.isoformat()
        elif isinstance(objectToEncode, ObjectId):
            return str(objectToEncode)
        elif isinstance(objectToEncode, bytes) :
            return str(objectToEncode)
        return json.JSONEncoder.default(self, objectToEncode)

app = Flask(__name__)

genericDAO = GenericDAO()
genericLocationDAO = GenericLocationDAO()


@app.route('/')
def api_root():
    return 'Welcome to app 1'

# Recuperer la liste de tous les utilisateurs
@app.route('/deliverus/get/users', methods=['GET'])
def get_users():
    collectionName = "users"

    usersList = GenericDAO.getAllObjects(collectionName)

    res = json.dumps(usersList, cls=MongoJsonEncoder)

    return res

# Recuperer un ou plusieurs utilisateur avec un ensemble de criteres
@app.route('/deliverus/get/user', methods=['POST'])
def get_user():

    request_data = request.json

    collectionName = "users"

    user = GenericDAO.getObjects(collectionName, request_data)

    res = json.dumps(user, cls=MongoJsonEncoder)

    return res

# Proceder a l'authentification de l'utilisateur
@app.route('/deliverus/authentification/user', methods=['POST'])
def get_authentification_user():

    request_data = request.json

    collectionName = "users"

    # Le hashage se fera a une etape ulterieure
    user = GenericDAO.getOneObject(collectionName, request_data)

    res = json.dumps(user, cls=MongoJsonEncoder)

    return res


# Verifier l'existence du pseudo d'un utilisateur
@app.route('/deliverus/register/verif_login', methods=['POST'])
def verif_login_existence():

    request_data = request.json

    collectionName = "users"

    user = GenericDAO.getOneObject(collectionName, request_data)

    result = {}
    # exist prend True si login existant et False sinon
    if(user == None) :
        result["login_exists"] = False
    else :
        result["login_exists"] = True

    res = json.dumps(result, cls=MongoJsonEncoder)

    return res

# Enregistrer un utilisateur
# Penser a refaire les tests cote client (longueur du pwd, champs non vides,...)
@app.route('/deliverus/register/user', methods=['POST'])
def register_user():

    request_data = request.json

    #   La verification des champs doit se faire a ce niveau, renvoyer une erreur si un test echoue

    collectionName = "users"

    insertionRes = genericDAO.insertObject(collectionName, request_data)

    result = {}
    # exist prend True si insertion OK et False sinon
    if(insertionRes == None) :
        result["insertion_OK"] = False
    else :
        result["insertion_OK"] = True

    res = json.dumps(result, cls=MongoJsonEncoder)

    return res

# Mise à jour d'un utilisateur
# Penser a refaire les tests cote client (vérification de l'identité de l'utilisateur qui demande la mise à jour)
@app.route('/deliverus/update/user', methods=['POST'])
def update_user():

    data1 = request.data
    data2 = data1.split(b"&")
    param1 = data2[0]
    param2 = data2[1]

    request_data_1 = json.loads(param1.decode('utf-8'))
    request_data_2 = json.loads(param2.decode('utf-8'))

    collectionName = "users"

    updateRes = genericDAO.updateObjects(collectionName, request_data_1, request_data_2)

    result = {}
    # exist prend True si insertion OK et False sinon
    if(updateRes.raw_result["nModified"] == 0) :
        result["update_OK"] = False
    else :
        result["update_OK"] = True

    res = json.dumps(result, cls=MongoJsonEncoder)

    return res

# Chercher le livreur le plus proche de l'adresse de la course de l'utilisateur
@app.route('/deliverus/get/steed', methods=['POST'])
def get_nearest_steed():

    request_data = request.json

    request_data_2 = [request_data["lng"], request_data["lat"]]

    nearestSteed = genericLocationDAO.getObjects(request_data_2)

    res = json.dumps(nearestSteed, cls=MongoJsonEncoder)

    return res


# Main application
if __name__ == '__main__':
     app.run()


