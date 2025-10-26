from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
ACCOUNT_SID = "ACb77633a111cb8311cbe26d540ffc9c14"
AUTH_TOKEN = "c3f3720a9d1370ba084c52d431d440bf"
FROM_WHATSAPP = "whatsapp:+14155238886"

client = Client(ACCOUNT_SID, AUTH_TOKEN)
app = Flask(__name__)

messages_received = []  # store received messages temporarily

@app.route("/send", methods=["POST"])
def send_message():
    data = request.json
    to = data.get("to")
    text = data.get("text")

    try:
        message = client.messages.create(
            from_=FROM_WHATSAPP,
            body=text,
            to=f"whatsapp:{to}"
        )
        return jsonify({"status": "success", "sid": message.sid})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route("/whatsapp", methods=["POST"])
def receive_message():
    incoming_msg = request.values.get("Body", "")
    sender = request.values.get("From", "")
    messages_received.append({"from": sender, "text": incoming_msg})

    resp = MessagingResponse()
    resp.message(f"🤖 I received your message: {incoming_msg}")
    return str(resp)

@app.route("/receive", methods=["GET"])
def get_messages():
    return jsonify(messages_received)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
