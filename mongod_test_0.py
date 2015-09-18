__author__ = 'OTurki'

from Model.User import  User
from DAO.GenericDAO import GenericDAO

#
# def connectToDatabaseServer() :
#     # Connexion au serveur de Mongo DB
#     db_conn=None
#
#     try:
#         db_conn=pymongo.MongoClient()
#         print("Connected successfully!!!")
#         print(db_conn)
#     except pymongo.errors.ConnectionFailure :
#         print("Could not connect to MongoDB: %s" % e)
#
#     #function result
#     return db_conn
#
# def connectToDatabase(db_conn,database_name) :
#
#     # Connexion a la base du projet
#
#     db = db_conn[database_name]
#
#     #function result
#     return db
#
# def getCollection(db, collection_name) :
#
#     #Connexion a la collection
#
#     collection = db[collection_name]
#
#     #function result
#     return collection
#
# def getAllUsers(users_collection) :
#
#     for user in users_collection.find():
#         print(user)

#for user in users_collection.find() :
#print(user["userPseudo"])


genericDAO = GenericDAO()

collectionName = "users"

# tester la méthode insertObject
#
# inserer un user test dans la collection

# import base64
# from base64 import decodebytes
#
# imageToSave = open("image_test.jpg", "rb")
#
# encodedImage = base64.b64encode(imageToSave.read())
#
# # fileToSave = open("temp_images/image_test_2.jpg","wb")
# #
# # fileToSave.write(decodebytes(encodedImage))
#
#
# userToInsert = User("login1097", "1097", encodedImage, "nom 1097", "prénom 1097", 1, "user1097@gmail.com", "France")
#
#
# print ("\n Résultat insertion :\n", genericDAO.insertObject(collectionName, userToInsert.parseToDict()))


# tester la méthode UpdateObjects
#
# criteria = {"userLogin" : "login1092"}
# update = {"userLogin" : "login1092.2"}
#
# updateResult = genericDAO.updateObjects(collectionName, criteria, update)
# print ("\n Résultat mise à jour : \n", updateResult)

# tester la méthode getAllRecords
#
usersList = GenericDAO.getAllObjects(collectionName)

for user in usersList:
    print(user)

# tester la méthode getObjects
# criteria = {"userPseudo" : "pseudo test 4"}
#
# usersToRemoveList = genericDAO.getObjects(collectionName, criteria)
#
# if (len(usersToRemoveList) > 0) :
#     # tester la méthode removeOneObject
#
#     userToRemoveTest = User.parseToUser(usersToRemoveList[0])
#     removeResult = genericDAO.removeOneObjectFromCollection(collectionName, userToRemoveTest._id)
#
#     print("\n Résultat suppression : \n", removeResult)
#
# else :
#     print("\n Pas d'éléments à supprimer")


# tester la méthode getOneObject
#
# userGetOneTest = GenericDAO.getOneObject(collectionName, {"userLogin" : "login1092"} )
#
# print("\n userGetOneTest : \n", userGetOneTest)


# Données test, à examiner plus tard
# pref1 = {}
# pref1["produit"]="yaourt glacé"
# pref1["prix"] =  11.5
#
# pref2 = {}
# pref2["produit"]="donut"
# pref2["prix"] =  3.25
#
# prefs = []
# prefs.append(pref1)
# prefs.append(pref2)




