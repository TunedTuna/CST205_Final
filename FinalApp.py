from flask import Flask, render_template, flash, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired
from datetime import datetime
from flask import *
import os

# from user_manager import... [this will import methods from the user_manager.py]
import user_manager

from flask_bootstrap import Bootstrap5

# create an instance of Flask
app= Flask(__name__)

app.config['SECRET_KEY']= 'csumb-otter'
bootstrap = Bootstrap5(app)
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

class UserDataInput(FlaskForm):
    userName= StringField(
        'User Name',
        validators=[DataRequired()]
    )
    userPassword = PasswordField(
        "Password",
        validators=[DataRequired()]
    )

userDataList= []

def store_user(userName,userPassword):
    userDataList.append(dict(
        name=userName,
        password= userPassword,
        date = datetime.today()

    ))


#  route stuff
@app.route('/signUp',methods=('GET','POST'))
def signUp():

    form = UserDataInput()
    if form.validate_on_submit(): #when user hits "enter"
        print(f'Form submitted username: {form.userName.data}')

        if not user_manager.checkDupe(form.userName.data):
            # user is UNIQUE-ish store them in "DB"
            user_manager.addUser(form.userName.data,form.userPassword.data)
            store_user(form.userName.data,form.userPassword.data)
            return redirect('/home')
        else:
            # display error
            #reload page to refresh input?
            print("whoopsies, user exists...")
            return redirect('/signUp')
           
        
    return render_template('createAccount.html',form=form)

@app.route('/',methods=('GET','POST'))
def logIn():
    form= UserDataInput()
    if form.validate_on_submit():
        return redirect('/home')
    return render_template('logIn.html',form=form)
    
@app.route('/home')
def home():
    return render_template('home.html')

@app.route("/upload")
def main():
    return render_template("upload.html")

@app.route("/success", methods=["POST"])
def success():
    if 'file' not in request.files:
        return "No file uploaded"

    image = request.files['file']
    if image.filename == '':
        return "No file selected"

    file_path = os.path.join(UPLOAD_FOLDER, image.filename)
    image.save(file_path)
    print(f"File saved to {file_path}")
    return render_template("acknowledgement.html", filename=image.filename)




if __name__ == "__main__":
    app.run(debug=True)
