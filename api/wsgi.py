from flask import Flask, request

app = Flask(__name__)


@app.route("/user", methods=["POST"])
def create_user():
    """Create a new user."""
    pass


@app.route("/login")
def login():
    """Exchange credentials for a JWT."""
    pass
