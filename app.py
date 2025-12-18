from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, Flask! This is my assignment app."


@app.route("/create-user/<name>")
def get_user(name):
    return f"get user {name}", 200 


if __name__ == "__main__":
    app.run(debug=True)
