from flask import Flask, render_template, flash, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired
from datetime import datetime

from flask_bootstrap import Bootstrap5

# create an instance of Flask
app= Flask(__name__)

app.config['SECRET_KEY']= 'csumb-otter'
bootstrap = Bootstrap5(app)

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
@app.route('/',methods=('GET','POST'))
def signIn():
    form = UserDataInput()
    if form.validate_on_submit():
        store_user(form.userName,form.userPassword)
        return redirect('/idk')
    return render_template('index.html',form=form)


