from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Create Flask app
app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def whatsapp_webhook():
    incoming_msg = request.form.get('Body')
    sender = request.form.get('From')

    print(f"📩 Message from {sender}: {incoming_msg}")

    # Generate OpenAI response
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are WeldBot, a helpful welding diagnostics assistant."},
            {"role": "user", "content": incoming_msg}
        ]
    )

    reply = response['choices'][0]['message']['content']
    twilio_response = MessagingResponse()
    twilio_response.message(reply)
    return str(twilio_response)

import os

if __name__ == "__main__" or __name__ == "weldbot_main":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
