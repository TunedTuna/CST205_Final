from flask import Flask, render_template, flash, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired
from datetime import datetime
from flask import *
import os
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
import json
# from user_manager import... [this will import methods from the user_manager.py]
import user_manager
import image_saver
from flask_bootstrap import Bootstrap5
from PIL import Image

# create an instance of Flask
app= Flask(__name__)

app.config['SECRET_KEY']= 'csumb-otter'
bootstrap = Bootstrap5(app)
# UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')
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



# flask_login stuff
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/' 
# flask_login stuff - class?
class User(UserMixin):
    def __init__(self, userName):
        self.id= userName 

# flask_login stuff - their method?
@login_manager.user_loader
def load_user(user_id):
    with open("user_data.json", "r") as file:
        users = json.load(file)
        for user in users:
            if user["userName"] == user_id:
                print("im in loader!")
                return User(user_id)
    print("im out of  loader...")
    return None



# route stuff

@app.route('/signUp',methods=('GET','POST')) # SIGN UP PAGE
def signUp():

    form = UserDataInput()
    if form.validate_on_submit(): #when user hits "enter"
        print(f'Form submitted username: {form.userName.data}')

        if not user_manager.checkDupe(form.userName.data):
            print("✅ No duplicate found. Adding user.")
            # user is UNIQUE-ish store them in "DB"
            user_manager.addUser(form.userName.data,form.userPassword.data)
            # store_user(form.userName.data,form.userPassword.data)
            return redirect('/home')
        else:
            # display error
            #reload page to refresh input?
            print("whoopsies, user exists...")
            return redirect('/signUp')      
        
    return render_template('createAccount.html',form=form)



@app.route('/',methods=('GET','POST')) # main page (login)
def logIn():
    form= UserDataInput()
    if form.validate_on_submit():
        userName= user_manager.checkLogin(form.userName.data,form.userPassword.data)
        if userName:
            login_user(User(userName))
            print(f'LOGIN SUCCESSFUL: user_id = {userName}')

            return redirect('/home')
        else:
             flash("Invalid username or password")
    return render_template('logIn.html',form=form)



@app.route('/home', methods=['GET','POST']) # home page that user see after log in, can be accessed after logging in
@login_required
def home():
    return render_template('home.html')



@app.route('/edit', methods = ['GET', 'POST']) # editing the image
@login_required
def edit_image():

    # if request.method == 'POST':
    if request.method == 'POST':
     
        if 'file' not in request.files:
            return "No file uploaded"

        image = request.files['file']

        if image.filename == '':
            return "No file selected"

        selectedfilter = request.form.get("filter")
        selectedformat = request.form.get("format", "original")

        print(f"User selected filter {selectedfilter} and format {selectedformat}")

        image = request.files["file"]
       
        img = Image.open(image)
        file_path = os.path.join(UPLOAD_FOLDER, image.filename)
        img.save(file_path)
        print(f"File saved to {file_path}")

        img = img.convert("RGB")
        width, height = img.size
        width2, height2 = img.size # use later...

        file_path = os.path.join(UPLOAD_FOLDER, image.filename)

        if (selectedfilter == "1"): # sepia filter

            for x in range (width):

                for y in range (height):

                    pixel = img.getpixel((x, y))

                    if pixel[0] < 63:
                        r, g, b = int(pixel[0] * 1.1), pixel[1], int(pixel[2] * 0.9)

                    elif pixel[0] > 62 and pixel[0] < 192:
                        r,g,b = int(pixel[0] * 1.15), pixel[1], int(pixel[2] * 0.85)

                    else: # otherwise
                        r = int(pixel[0] * 1.08)
                        g,b = pixel[1], int(pixel[2] * 0.5)

                img.putpixel((x, y), (r, g, b))
        
        elif (selectedfilter == "2"): # negative filter
            negativelist = [((255 - p[0]), (255 - p[1]), (255 - p[2])) for p in img.getdata()]
            img.putdata(negativelist)

        elif (selectedfilter == "3"): # grayscale filter, luminosity method
            grayscalelist = [(((p[0]*299) + (p[1]*587) + (p[2]*114)) // 1000,) * 3 for p in img.getdata()]
            img.putdata(grayscalelist)

        if (selectedformat != "original"):

            filename2 = f"{os.path.splitext(image.filename)[0]}.{selectedformat.lower()}"

            file_path = os.path.join(UPLOAD_FOLDER, filename2)
            img.save(file_path, format=selectedformat.upper())
            

        else:
            filename2 = image.filename  
            file_path = os.path.join(UPLOAD_FOLDER, filename2)
            img.save(file_path)
        
            print(f"File saved to {file_path}")
            return redirect(url_for('results', filename= filename2))
    return render_template('upload.html')



@app.route('/results') # this where one see the image after editing
@login_required
def results():
    filename = request.args.get('filename')
    return render_template('results.html', filename=filename)



@app.route('/uploads')
@login_required
def uploaded_file(filename):
    return render_template(UPLOAD_FOLDER, filename)



@app.route('/profile', methods=('GET','POST'))
@login_required
def profile():
    return render_template('profile.html')

if __name__ == "__main__":
    app.run(debug=True)