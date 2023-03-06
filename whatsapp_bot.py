from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from class_chatgpt import Gpt_API
from class_replicate import Replicate_API
from water_mark import Water_Mark
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

from dotenv import load_dotenv
load_dotenv()

account_sid = os.getenv('ACCOUNT_SID')
auth_token = os.getenv('AUTH_TOKEN')
client = Client(account_sid, auth_token)

app = Flask(__name__)
 
@app.route("/", methods=['POST'])
def wa_sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Fetch the message
    
    msg = request.form.get('Body') # Reading the message from the WhatsApp
    sender = request.form.get('From') # Retrieving the sender's phone number or username
    print("Message from", sender, ":", msg)
    resp = MessagingResponse()
    if msg.startswith('/tai'):
        send_photo_message(sender,"https://m.media-amazon.com/images/I/710ut7y5jYL._AC_UF894,1000_QL80_.jpg","Here is your image")
        return str(resp)
    else:
        
        reply = resp.message()
        
        # Create reply
        response = generate_response(msg)
        reply.body(response)
    
        return str(resp)

def generate_response(msg):
    #prompt = f"{sender}: {msg}\nBot:"
    try:
        obj = Gpt_API(msg)
        result = obj.get_result()
    except Exception as e:
        print("Error: ", e)
        return "Sorry, there was an error generating a response."
    return result

def send_photo_message(to_number, media_url, caption):
    """Send a photo message with a caption to the specified phone number."""
    try:
        message = client.messages.create(
            to=to_number,
            media_url=media_url,
            from_='whatsapp:+14155238886',
            body=caption,
            
        )
        print(f"Photo message sent to {to_number}")
    except TwilioRestException as e:
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(e)

if __name__ == "__main__":
    app.run(port=5000)
