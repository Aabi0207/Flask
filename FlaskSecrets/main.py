from flask import Flask, render_template
# import os
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField, validators
from wtforms.validators import DataRequired, Email, length
from flask_bootstrap import Bootstrap5


class MyForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), length(min=8, max=15)])
    login = SubmitField("Log in")


def is_login_correct(email, password):
    return email == "admin@email.com" and password == "12345678"


SECRET_KEY = "@Aabi0207"


'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''


app = Flask(__name__)
app.secret_key = SECRET_KEY
bootstrap = Bootstrap5(app)

@app.route("/")
def home():
    return render_template('index.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    correct_login = True
    form = MyForm()
    if form.validate_on_submit():
        if is_login_correct(form.email.data, form.password.data):
            return render_template("success.html")
        else:
            return render_template("denied.html")
    return render_template("login.html", form=form)


if __name__ == '__main__':
    app.run(debug=True)
