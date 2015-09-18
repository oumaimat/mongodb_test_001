__author__ = 'OTurki'

class User :

    _id = ""
    userLogin = ""
    userPwd = ""
    userProfilePicture = None
    userLastName = ""
    userName = ""
    userGender = ""
    userEmail = ""
    userCountry = ""
    userSubmittedChoices = []

    def __init__(self, userLogin, userPwd, userProfilePicture, userLastName, userName, userGender, userEmail, userCountry):
        self.userLogin = userLogin
        self.userPwd = userPwd
        self.userProfilePicture = userProfilePicture
        self.userLastName = userLastName
        self.userName = userName
        self.userGender = "M" if userGender == 0 else "F"
        self.userEmail = userEmail
        self.userCountry = userCountry



    def parseToDict(self):
        user = {}

        user["userLogin"] = self.userLogin
        user["userPwd"] = self.userPwd
        user["userProfilePicture"] = self.userProfilePicture
        user["userLastName"] = self.userLastName
        user["userName"] = self.userName
        user["userGender"] = self.userGender
        user["userEmail"] = self.userEmail
        user["userCountry"] = self.userCountry

        #Function return result
        return user

    def parseToUser(userDict):


        user = User(userDict["userLogin"], userDict["userPwd"], userDict["userProfilePicture"], userDict["userLastName"], userDict["userName"], userDict["userGender"], userDict["userEmail"], userDict["userCountry"])

        user._id = userDict["_id"]

        #Function return result
        return user