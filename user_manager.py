# Image Filter and Format Converter Web Application
# Class: CST 205
# Abstract: This file will handle the checks n stuff for user log in
#           This file will import the file that holds userData
# Author: Daniel Rodas
# Date: 5/14/2025
# Lecture: CST 205 APIs

import json
import os

base_directory = os.path.dirname(os.path.abspath(__file__))
user_file = os.path.join(base_directory, 'user_data.json')

data = json.load(open(user_file))


def test_lookInJson():
    for user in data:
        print(f'{user["userName"]}')

def checkDupe(tempUserName):
    # reload json incase new info
    with open(user_file, 'r') as file:
        data = json.load(file)

    # checks for duplicates True = dupe, False = no dupe
    for user in data:
        print(f'CHECKING: {tempUserName}')
        if user["userName"] == tempUserName:
            return True
    return False

def addUser(newUserName, newPassword):
    new_user = {
        "userName": newUserName,
        "password": newPassword
    }

    with open(user_file, "r") as file:
        users = json.load(file)

    users.append(new_user)

    with open(user_file, "w") as file:
        json.dump(users, file, indent=2)


def checkLogin(inputUserName, inputPassword):
    data = json.load(open(user_file))
    for user in data:
        if inputUserName == user["userName"] and inputPassword == user["password"]:
            return user["userName"]
    return None
