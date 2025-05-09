# this file will handle the checks n stuff for user log in
# this file will import the file that holds userData
# CST 205 APIs
import json
data= json.load(open('user_data.json'))



def test_lookInJson():
    for user in data:
        print(f'{user["userName"]}')