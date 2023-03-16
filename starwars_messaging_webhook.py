import os
from pyngrok import ngrok
from flask import Flask, request
from signalwire.messaging_response import MessagingResponse
from signalwire.rest import Client as signalwire_client


# Initialize the Flask object
app = Flask(__name__)


# Define what we would like our application to do
@app.route("/sms_app", methods=['GET', 'POST'])
def sms_app():

    # Find the body of the incoming message and send out a response based based on that string
    body = request.values.get('Body', None)

    # Start our message response
    resp = MessagingResponse()

    # Determine the proper body to reply back to the sender
    # If anything besides 'y' or 'n' comes in as the body, the application will send out the standard prompt (listed underneath the else statement)
    if body == 'y':
        resp.message("Great! You will report to the Death Star for training tomorrow")
    elif body == 'n':
        resp.message("No problem, may the sith be with you")
    else:
        resp.message('Would you like the First Order to contact you about career opportunities around the galaxy?(y/n)')
    return str(resp)


# Set the ngrok URL as the webhook for our SW phone
def start_ngrok():
    # Set up a tunnel on port 5000 for our Flask object to interact locally
    url = ngrok.connect(5000).public_url
    print(' * Tunnel URL:', url)

# In the previous step, we declared where the tunnel will be opened, however we must start ngrok before a tunnel will be available to open
# This checks your os to see if ngrok is already running and if it isnt, will begin running
if __name__ == '__main__':
    if os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
        start_ngrok()
    app.run(debug=True)
