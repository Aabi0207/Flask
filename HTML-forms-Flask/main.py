# importing Flask and other modules
from flask import Flask, request, render_template

# Flask constructor
app = Flask(__name__)

# A decorator used to tell the application
# which URL is associated function

@app.route("/")
def home():
    return render_template("index.html")


@app.route('/login', methods=["GET", "POST"])
def handel_data():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        text = "Your name is " + username + email
        aa = request.form["username"]
    return render_template("login_details.html", display=text, aa=aa)


if __name__=='__main__':
    app.run(debug=True)
