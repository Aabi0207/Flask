import random
from flask import Flask
app = Flask(__name__)

random_num = random.randint(0, 9)

@app.route("/")
def guess_a_number():
    return "<h1>Guess a Number from 0 to 9.</h1>" \
           "<img src='https://media.giphy.com/media/3o7aCSPqXE5C6T8tBC/giphy.gif' width=200 alt='A gif of a number'>"

@app.route("/<int:num>")
def is_guessed_num_right(num):
    if num == random_num:
        return "<h1 style='color:blue'>You are right</h1>" \
               "<img src='https://media.giphy.com/media/4T7e4DmcrP9du/giphy.gif' width=200 alt='A cute puppy'>"
    elif num < random_num:
        return "<h1 style='color:Red'>Too Low</h1>" \
               "<img src='https://media.giphy.com/media/jD4DwBtqPXRXa/giphy.gif' width=200 alt='A Puppy'>"
    else:
        return "<h1 style='color:Green'>Too High</h1>" \
               "<img src='https://media.giphy.com/media/3o6ZtaO9BZHcOjmErm/giphy.gif' width=200 alt='A Puppy'>"

if __name__ == "__main__":
    app.run(debug=True)