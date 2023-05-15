"""
API to send password reset emails
"""
from flask import Flask, request, jsonify
import re

app = Flask(__name__)

# -------------------
# Application Routes
# -------------------
@app.route('/')
def home():
    """
    response description for $api/ endpoint
    """
    res = {
        "message":"Running API to send Twitter password reset emails.",
        "endpoints": {
            "/send" : "Send password reset email for Twiiter account.",
        },
    }
    return jsonify(res)

@app.route('/send')
def send():
    """
    endpoint: send password reset emails
    """
    try:
        email = request.args.get('email')
        username = request.args.get('username')
        
        # check email regex, if it is valid or not
        regex_email = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        
        if not re.fullmatch(regex_email, email):
            raise InvalidEmail
        
        # catch if the length of username is more than 15
        # characters (specified in the bounty requirements)
        if len(username)>15:
            raise UsernameExceedLimit
        
        status = send_password_reset_email(email, username)
        res = {
            "status": status,
            "message": "completed request"
        }
        return jsonify(res)
    except Exception as error:
        res = {
            "status": "error_message",
            "error": str(error),
        }
        return jsonify(res)

# ----------------------------
# Sending Password Reset Email
# ----------------------------
def send_password_reset_email(email: str, username: str) -> bool:
    """
    Send Password Reset Email Logic
    """
    req = email+username

    return req

# -----------------
# Custom Exceptions
# -----------------
class UsernameExceedLimit(Exception):
    "Raised when length of Username is more than 15."
    def __init__(self, message="invalid username. must not be more than 15 characters", *args):
        super().__init__(message, *args)
        self.message = message

class InvalidEmail(Exception):
    "Raised when email supplied is of invalid format."
    def __init__(self, message='invalid email', *args):
        super().__init__(message, *args)
        self.message = message

if __name__ == '__main__':
    app.run()