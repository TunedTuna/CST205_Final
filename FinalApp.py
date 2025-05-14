from flask import Flask, render_template, flash, redirect, send_file, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired
from datetime import datetime
from flask import *
import os
import io
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
import json
# from user_manager import... [this will import methods from the user_manager.py]
import user_manager
from image_saver import get_image_download
from flask_bootstrap import Bootstrap5
from PIL import Image
from user_history import log_user_action



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
    user_data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'user_data.json')
    with open(user_data_path, "r") as file:
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

@app.route('/edit', methods=['GET', 'POST'])  # editing the image
@login_required
def edit_image():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file uploaded"

        image = request.files['file']

        if image.filename == '':
            return "No file selected"

        filter_names = {
            "1": "Sepia",
            "2": "Negative",
            "3": "Grayscale"
        }

        selectedfilter = request.form.get("filter")
        filter_name = filter_names.get(selectedfilter, "Unknown")


        img = Image.open(image)
        img = img.convert("RGB")
        width, height = img.size

        if selectedfilter == "1":  # sepia filter
            for x in range(width):
                for y in range(height):
                    pixel = img.getpixel((x, y))
                    if pixel[0] < 63:
                        r, g, b = int(pixel[0] * 1.1), pixel[1], int(pixel[2] * 0.9)
                    elif 62 < pixel[0] < 192:
                        r, g, b = int(pixel[0] * 1.15), pixel[1], int(pixel[2] * 0.85)
                    else:
                        r = int(pixel[0] * 1.08)
                        g, b = pixel[1], int(pixel[2] * 0.5)

                    img.putpixel((x, y), (r, g, b))


        elif selectedfilter == "2":  # negative filter
            negativelist = [((255 - p[0]), (255 - p[1]), (255 - p[2])) for p in img.getdata()]
            img.putdata(negativelist)

        elif selectedfilter == "3":  # grayscale filter
            grayscalelist = [((p[0]*299 + p[1]*587 + p[2]*114) // 1000,) * 3 for p in img.getdata()]
            img.putdata(grayscalelist)

        # Save using original filename
        filename = image.filename
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        img.save(file_path)

        log_user_action(current_user.id, f"Applied {filter_name} filter", filename)

        print(f"File saved to {file_path}")
        return redirect(url_for('results', filename=filename))

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



@app.route('/download/<filename>/<file_type>')
@login_required
def download_image(filename, file_type):
    path = os.path.join('static/uploads', filename)

    if not os.path.exists(path):
        return "Image not found", 404
    image = Image.open(path)

    img_io, mimetype, download_name = get_image_download(
        image=image,
        file_type=file_type,
        filename=filename.rsplit('.', 1)[0]
    )

    log_user_action(current_user.id, f"Downloaded image as {file_type.upper()}", filename)


    return send_file(img_io, mimetype=mimetype, as_attachment=True, download_name=download_name)


@app.route('/profile', methods=('GET','POST'))
@login_required
def profile():
    history = []
    try:
        with open(os.path.join(os.path.dirname(__file__), 'user_history.json'), 'r') as file:
            all_history = json.load(file)
            history = all_history.get(current_user.id, [])
    except FileNotFoundError:
        pass
    return render_template('profile.html', history=history)


if __name__ == "__main__":
    app.run(debug=True)
