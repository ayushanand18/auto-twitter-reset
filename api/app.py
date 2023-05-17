"""
API to send password reset emails
"""
import re
import asyncio
from flask import Flask, request, jsonify
from pyppeteer import launch
from flask_socketio import SocketIO
from time import sleep

app = Flask(__name__)
socketio = SocketIO(app)
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
async def send():
    """
    endpoint: send password reset emails
    """
    try:
        email = request.args.get('email')
        username = request.args.get('username')
        phone_number = request.args.get('phone')

        # check email regex, if it is valid or not
        regex_email = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

        if not re.fullmatch(regex_email, email):
            raise InvalidEmail

        # catch if the length of username is more than 15
        # characters (specified in the bounty requirements)
        if len(username)>15:
            raise UsernameExceedLimit

        status = await send_password_reset_email(email, username, phone_number)
        res = {
            "status": "success" if len(status)==4 else "failed",
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
async def send_password_reset_email(email: str, username: str, phone_number: int) -> bool:
    """
    Send Password Reset Email Logic
    """
    browser = await launch(
        handleSIGINT=False,
        handleSIGTERM=False,
        handleSIGHUP=False,
        options={'args': ['--no-sandbox']}
    )
    page = await browser.newPage()
    
    await page.goto("https://twitter.com/i/flow/password_reset?input_flow_data=%7B%22requested_variant%22%3A%22eyJwbGF0Zm9ybSI6IlJ3ZWIifQ%3D%3D%22%7D")
    response = []
    
    sleep(3)

    await page.evaluate(
        f"""
        document.querySelector("input").value = '{username}';
        document.querySelectorAll("[role='button']")[1].click();
        """)
    response.append("username")

    sleep(2)

    await page.evaluate(
        f"""
        document.querySelectorAll("input").value = "{email}";
        document.querySelectorAll("[role='button']")[1].click();
        """
    )
    response.append("email")
    alerts = await page.evaluate(
        """ 
        () => {
            return document.querySelectorAll("[role='alert']").length;
        }
        """
    )
    if(alerts): raise IncorrectDetails

    sleep(2)
    
    await page.evaluate(
        f"""
        document.querySelector("input").value = {phone_number};
        document.querySelectorAll("[role='button']")[1].click();
        """
    )
    response.append("phone number")

    alerts = await page.evaluate(
        """ 
        () => {
            return document.querySelectorAll("[role='alert']").length;
        }
        """
    )
    if(alerts): raise IncorrectDetails

    sleep(2) # so that there's a buffer time to load the page

    await page.evaluate(
        """
        document.querySelectorAll("[role='button']")[1].click();
        """
    )
    response.append("submitted")
    await browser.close()

    return response

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

class IncorrectDetails(Exception):
    "Raised when wrong account info is provided."
    def __init__(self, message="Incorrect Account Details. Failed to verify.", *args):
        super().__init__(message, *args)
        self.message = message

if __name__ == '__main__':
    socketio.run(app)
