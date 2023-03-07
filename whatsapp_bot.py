from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from class_chatgpt import Gpt_API
from class_replicate import Replicate_API
from water_mark import Water_Mark
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
import os
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
        print("Prompt was {}",msg[5:])
        obj = Replicate_API(msg[5:])
        url = obj.get_result()[0]
        print("Got result")
        obj_watermark= Water_Mark(url)
        obj_watermark.get_result()
        print("Image saved")
        photo_path = '/result.png'
        print('file:///home/whatsapp_TaiBOT/result.png')
        send_photo_message(sender,'http://165.232.134.84:5000/image.jpg',"Here is your image")
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
