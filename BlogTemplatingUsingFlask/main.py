from flask import Flask, render_template
import requests

app = Flask(__name__)

blog_url = "https://api.npoint.io/c790b4d5cab58020d391"
blog_data = requests.get(blog_url).json()


@app.route('/')
def home():
    return render_template("index.html", posts=blog_data)

@app.route("/blog/<num>")
def get_blog(num):
    return render_template("post.html", posts=blog_data[int(num)-1])


if __name__ == "__main__":
    app.run(debug=True)
