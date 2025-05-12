# this file will take user id and add to their "History"

import json
data= json.load(open('history_data.json'))

def test_look_in_json():
    data= json.load(open('history_data.json'))
    for userName in data:
        print(f'{userName}')
        for rec in data[userName]:
            print(f'\t {data[userName]}')

def display_user_history(username):
    data= json.load(open('history_data.json'))
    return data[username]

def add_to_user_history(username,date, filter):

    add_rec={
        "date":date,
        "filter":filter
    }
    # open json
    with open("history_data.json","r") as file:
        user_rec = json.load(file)
        
    if username not in user_rec:
        user_rec[username] =[]

    # add to this user history
    user_rec[username].append(add_rec)
    
    with open("history_data.json","w") as file:
        json.dump(user_rec,file,indent=2)

