# this file will handle the checks n stuff for user log in
# this file will import the file that holds userData
#Lecture: CST 205 APIs
import json
data= json.load(open('user_data.json'))



def test_lookInJson():
    for user in data:
        print(f'{user["userName"]}')

def checkDupe(tempUserName):
    # reload json incase new info
    with open('user_data.json', 'r') as file:
        data = json.load(file)
    # data= json.load(open('user_data.json'))

    # checks for duplicates True = dupe, False = no dupe
    for user in data:
        print(f'CHECKING: {tempUserName}')
        if user["userName"] == tempUserName :
            return True
    return False

def addUser(newUserName, newPassword):
    new_user={
        "userName":newUserName,
        "password":newPassword
    }
    #lecture: The Python Programming Language (Part 3)
    with open("user_data.json", "r") as file:
        users = json.load(file)

    users.append(new_user)

    with open("user_data.json", "w") as file:
        json.dump(users, file, indent=2)

def checkLogin(inputUserName,inputPassword):
    # if user exists, return their userName else return none
    data= json.load(open('user_data.json'))
    for user in data:
        if inputUserName == user["userName"] and inputPassword==user["password"]:
            return user["userName"]
    return None