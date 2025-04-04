import csv
import json
import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Configuration: Read from environment variables.
PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN", "YOUR_PAGE_ACCESS_TOKEN")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "YOUR_VERIFY_TOKEN")
INSTAGRAM_API_URL = "https://graph.facebook.com/v15.0/me/messages"  # Update API version if needed
CSV_FILE = os.getenv("CONDITIONS_CSV", "conditions.csv")  # Path to the CSV file

# Load conditions from the CSV file.
conditions = []
try:
    with open(CSV_FILE, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Convert the 'contains_all', 'contains_any', and 'does_not_contain' fields into lists.
            for field in ['contains_all', 'contains_any', 'does_not_contain']:
                if row.get(field, "").strip():
                    keywords = [kw.strip().lower() for kw in row[field].split(';') if kw.strip()]
                else:
                    keywords = []
                row[field] = keywords
            row['response_type'] = row.get('response_type', 'text').strip().lower()
            row['response_content'] = row.get('response_content', '').strip()
            conditions.append(row)
except Exception as e:
    print("Error loading CSV file:", e)
    conditions = []  # If error, leave conditions empty

def check_message(user_message):
    """
    Check the incoming user message against the conditions defined in the CSV.
    Returns a list of matching responses.
    """
    results = []
    msg = user_message.lower()
    for cond in conditions:
        # 'contains_all': All keywords must be present.
        if cond['contains_all']:
            if not all(kw in msg for kw in cond['contains_all']):
                continue
        # 'contains_any': At least one keyword must be present.
        if cond['contains_any']:
            if not any(kw in msg for kw in cond['contains_any']):
                continue
        # 'does_not_contain': None of the keywords must be present.
        if cond['does_not_contain']:
            if any(kw in msg for kw in cond['does_not_contain']):
                continue
        # If all conditions pass, add the response.
        result = {
            "type": cond['response_type'],
            "content": cond['response_content']
        }
        results.append(result)
    return results

def send_instagram_message(recipient_id, message_data):
    """
    Send a message to the user via Instagram Graph API.
    recipient_id: The Instagram user ID to send the message to.
    message_data: Dictionary containing the message type and content.
    """
    payload = {
        "recipient": {"id": recipient_id},
        "message": {}
    }
    # Prepare payload based on the response type.
    if message_data['type'] == 'text':
        payload["message"] = {"text": message_data["content"]}
    elif message_data['type'] == 'buttons':
        try:
            # If the button message content is a JSON string, parse it.
            button_content = json.loads(message_data["content"])
            payload["message"] = button_content
        except Exception as e:
            print("Error parsing button message:", e)
            payload["message"] = {"text": message_data["content"]}
    else:
        payload["message"] = {"text": message_data["content"]}

    params = {"access_token": PAGE_ACCESS_TOKEN}
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(INSTAGRAM_API_URL, params=params, headers=headers, json=payload)
        response.raise_for_status()
        print("Message sent:", response.json())
        return response.json()
    except requests.exceptions.RequestException as e:
        print("Error sending message:", e)
        return None

# Webhook verification (GET request)
@app.route('/webhook', methods=['GET'])
def verify_webhook():
    """
    Instagram verifies your webhook URL by sending a GET request.
    Return the 'hub.challenge' value if the verify token matches.
    """
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if mode and token:
        if mode == "subscribe" and token == VERIFY_TOKEN:
            print("WEBHOOK VERIFIED")
            return challenge, 200
        else:
            return "Invalid verification token", 403
    return "Missing parameters", 400

# Webhook to receive messages (POST request)
@app.route('/webhook', methods=['POST'])
def webhook():
    """
    Process incoming messages from Instagram.
    The incoming data is expected to have an 'entry' array with 'messaging' events.
    """
    data = request.get_json()
    print("Received data:", json.dumps(data, indent=2))
    if data.get("object") == "instagram":
        for entry in data.get("entry", []):
            for messaging_event in entry.get("messaging", []):
                sender_id = messaging_event.get("sender", {}).get("id")
                message_text = messaging_event.get("message", {}).get("text", "")
                if sender_id and message_text:
                    print(f"Received message - Sender ID: {sender_id}, Message: {message_text}")
                    responses = check_message(message_text)
                    if responses:
                        for response_data in responses:
                            send_instagram_message(sender_id, response_data)
                    else:
                        # Send a default response if no condition is matched.
                        default_response = {"type": "text", "content": "Sorry, no appropriate response was found."}
                        send_instagram_message(sender_id, default_response)
        return jsonify(status="ok"), 200
    else:
        return jsonify(status="invalid object"), 400

if __name__ == '__main__':
    # Run the app on 0.0.0.0 so it can be reached externally, on the specified PORT.
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
