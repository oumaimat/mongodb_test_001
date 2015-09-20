__author__ = 'OTurki'

import pymongo
from gridfs import GridFS
from PIL import Image
import base64
from base64 import decodebytes
import os

class ConnectionToDatabase :

    database = None
    fs = None


    #penser � cr�er un pool de connections r�utilisables vers la base
    #solution actuelle non envisageable en prod

    def __init__(self):
        self.connectToDatabase()


    def connectToDatabase(self) :
        # Connexion au serveur de Mongo DB
        db_conn=None

        # url = os.environ["OPENSHIFT_MONGODB_DB_URL"]

        # test

        try:
            # db_conn=pymongo.MongoClient("mongodb://admin:3usRy1SmJ8gH@127.0.0.1:37391/")
            db_conn=pymongo.MongoClient()
            print("Connected successfully!!!")
            print(db_conn)
        except pymongo.errors.ConnectionFailure :
            print("Could not connect to MongoDB: %s")


        # Connexion a la base du projet
        #db = db_conn["mongodbtest0"]
        db = db_conn["project_database"]


        #Initialisation des variables globales
        ConnectionToDatabase.database = db
        ConnectionToDatabase.fs = GridFS(db)

    def getCollection(self, collection_name):

        #Connexion a la collection
        collection = ConnectionToDatabase.database[collection_name]

        #function result
        return collection

class ConnectionToLocationDatabase :

    database = None
    fs = None
    collection = None

    #penser � cr�er un pool de connections r�utilisables vers la base
    #solution actuelle non envisageable en prod

    def __init__(self):
        self.connectToDatabase()


    def connectToDatabase(self) :
        # Connexion au serveur de Mongo DB
        db_conn=None

        # url = os.environ["OPENSHIFT_MONGODB_DB_URL"]

        try:
            db_conn=pymongo.MongoClient()
            print("Connected successfully!!!")
            print(db_conn)
        except pymongo.errors.ConnectionFailure :
            print("Could not connect to MongoDB: %s")


        # Connexion a la base du projet
        #db = db_conn["mongodbtest0"]
        db = db_conn["GPSLocationDB"]


        #Initialisation des variables globales
        ConnectionToLocationDatabase.database = db
        ConnectionToLocationDatabase.fs = GridFS(db)
        ConnectionToLocationDatabase.collection = db.get_collection("steeds")

class GenericDAO :

    connectionToDatabase = ConnectionToDatabase()

    # Ins�rer un enregistrement dans une collection
    def insertObject(self, collectionName, object):

        collection =  GenericDAO.connectionToDatabase.getCollection(collectionName)

        # Enregistrer l'image dans GridFS si l'utilisateur a uploadé son image
        if (collectionName == "users") and (object["userProfilePicture"] != None ) :

            fileName = object["userLogin"]

            object["userProfilePicture"] = self.buildGridFsImage(object["userProfilePicture"], fileName)

        insertionResult = collection.insert(object)

        return insertionResult

    # Supprimer un enregistrement dans une collection
    def removeOneObject(self, collectionName, objectID ):

        collection =  GenericDAO.connectionToDatabase.getCollection(collectionName)
        removeResult = collection.remove(objectID)

        return removeResult

    # Supprimer un ou plusieurs enregistrements dans une collection
    def removeObjects(self, collectionName, objectCriteria):

        collection =  GenericDAO.connectionToDatabase.getCollection(collectionName)
        removeResult = collection.remove(objectCriteria)

        return removeResult

    # Mettre � jour un ou plusieurs enregistrements dans une collection
    def updateObjects(self, collectionName, objectCriteria, objectUpdate):

        collection =  GenericDAO.connectionToDatabase.getCollection(collectionName)

        # Mettre le update operator � $set
        addedUpdateOperator = {"$set": objectUpdate}
        updateResult = collection.update_many(objectCriteria, addedUpdateOperator)

        return updateResult

    # Si utilisée, il faut limiter le nombre d'enregistrements retourné (exemple 100)
    def getAllObjects(collectionName):

        collection = GenericDAO.connectionToDatabase.getCollection(collectionName)

        if(collectionName == "users") :
            recordsList = list(collection.find({}, {"userPwd" : False}))
        else :
             recordsList = list(collection.find())

        return recordsList

    # Extraire un enregistrement
    def getOneObject(collectionName, objectCriteria):

        collection = GenericDAO.connectionToDatabase.getCollection(collectionName)

        if(collectionName == "users") :
            foundObject = collection.find_one(objectCriteria, {"userPwd" : False})

            if foundObject != None and foundObject["userProfilePicture"] != None:
                foundObject["userProfilePicture"] = GenericDAO.getGridFsImage(foundObject["userProfilePicture"])
        else :
            foundObject = collection.find_one(objectCriteria)

        return foundObject

    # Extraire un ou plusieurs enregistrements
    def getObjects(collectionName, objectCriteria):

        collection = GenericDAO.connectionToDatabase.getCollection(collectionName)

        if(collectionName == "users") :
            foundObjects = list(collection.find(objectCriteria, {"userPwd" : False}))

            if foundObjects != None :
                for user in foundObjects :
                    if user["userProfilePicture"] != None :
                        user["userProfilePicture"] = GenericDAO.getGridFsImage(user["userProfilePicture"])

        else :
            foundObjects = list(collection.find(objectCriteria))

        return foundObjects

    #Insérer un enregistrement contenant une image dans la base
    def buildGridFsImage(self, encodedImage, fileName):

        # Créer un fichier image temporaire à partir des Bytes
        imageToSave = open("temp_images/"+fileName+".jpg","wb+")
        imageToSave.write(decodebytes(encodedImage))

        # Insérer le fichier image temporaire dans GridFS
        imageID = ConnectionToDatabase.fs.put(imageToSave, content_type="image/jpeg")

        imageToSave.close()

        # Supprimer le fichier image temporaire du disque
        os.remove("temp_images/"+fileName+".jpg")

        return imageID


    #Lire un enregistrement contenant une image dans la base
    def getGridFsImage(imageID):

        # Récupérer l'objet Image depuis l'ID de l'image
        gridFsRes = ConnectionToDatabase.fs.get(imageID)


        # Encoder l'image en un format de Bytes qui pourra être envoyé par le webservice
        encodedImage = base64.b64encode(gridFsRes.read())

        # imageToShow.show()

        return encodedImage




class GenericLocationDAO :

    connectionToLocationDatabase = ConnectionToLocationDatabase()

    # Extraire les livreurs les plus proches d'une localisation dans un rayon de 500 metres
    def getObjects(self, userCoordinates):

        locationDict = {"location" :
                            {"$near": {
                              "$geometry" : {
                                  "type" : "Point",
                                  "coordinates" : userCoordinates
                              }  ,
                                "$maxDistance" : 500
                            }
                             }
                        }

        collection1 = GenericLocationDAO.connectionToLocationDatabase.collection

        foundObjects = list(collection1.find(locationDict, limit=10))

        return foundObjects