
![ChatGPT Image Apr 4, 2025, 05_33_16 PM](https://github.com/user-attachments/assets/6f0b72ad-1c36-42f7-aac4-8b3b7a53f43e)

# Instagram Chatbot Integration with CSV-Based Conditions

This project is a Flask-based application that integrates with the Instagram Graph API to create a highly flexible chatbot. The chatbot uses a CSV file to define keyword-based conditions and returns one or more responses (plain text or button messages) depending on the incoming Instagram message. It mimics ManyChat’s behavior by evaluating multiple conditions and sending multiple messages if needed.

## Features

- **CSV-Based Rule Engine:**  
  Define conditions in a CSV file using:
  - `contains_all`: All listed keywords must be present in the incoming message.
  - `contains_any`: At least one of the listed keywords must be present.
  - `does_not_contain`: None of the listed keywords should be present.
  
- **Multiple Response Types:**  
  Send plain text responses or rich messages with buttons (using JSON format).

- **Multi-Response Capability:**  
  If an incoming message matches more than one rule, all corresponding responses are sent.

- **Instagram Integration:**  
  Uses the Instagram Graph API to both receive messages (via webhook) and send responses.

## Requirements

- Python 3.6+
- [Flask](https://flask.palletsprojects.com/)
- [Requests](https://docs.python-requests.org/)
- [python-dotenv](https://github.com/theskumar/python-dotenv) (for loading environment variables)

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/irmakerkol/Instagram-Chatbot
   cd instagram-chatbot
   
2. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt

3. **Set Environment Variables:**

   Create a .env file in the root directory of the project with the following content:

   ```dotenv
   # Instagram API Credentials
    PAGE_ACCESS_TOKEN=YOUR_PAGE_ACCESS_TOKEN
    VERIFY_TOKEN=YOUR_VERIFY_TOKEN
    
    # Optional: Specify a custom CSV file path if not using the default 'conditions.csv'
    CONDITIONS_CSV=conditions.csv
    
    # Optional: Specify the port on which the application will run (default is 5000)
    PORT=5000

   
4. **Create a CSV file:**
    (default: conditions.csv) with the following columns:

    `contains_all:` Semicolon-separated list of keywords that must all be present.

    `contains_any:` Semicolon-separated list of keywords where at least one must be present.

    `does_not_contain:` Semicolon-separated list of keywords that must not be present.

    `response_type:` The type of response (text for plain text, buttons for button messages).

    `response_content:` For text, this is the message string; for buttons, this is a JSON string defining the button structure.


## Running the Application

  1. **Start the Flask Application:**

     ```bash
     python ig_chatbot.py
     
  2. **Configure the Instagram Webhook:**
     In your Facebook Developer dashboard, set the webhook URL (e.g., https://yourdomain.com/webhook) for your Instagram Business Account.
     During verification, Instagram will send a GET request with hub.challenge and hub.verify_token.
     The app will return the challenge token if the VERIFY_TOKEN matches.

## How it Works
  Webhook Verification:
  Instagram sends a GET request for webhook verification. The app checks the provided verify token and returns the challenge if it matches.
  
  Message Processing:
  Incoming Instagram messages (found in the entry and messaging fields) are processed by comparing the message text against all rules defined in the CSV file.
  
  Response Sending:
  For every rule that matches, the app sends the corresponding response via the Instagram Graph API. If multiple rules match, multiple responses are sent.


## Contributing
Contributions are welcome! Please feel free to open issues or submit pull requests.


## License
This project is licensed under the MIT License.

---

Feel free to update any sections or add further instructions as needed for your project.

  
