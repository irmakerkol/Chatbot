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

2. **Set Environment Variables:**

   Create a .env file in the root directory of the project with the following content:

   ```dotenv
   # Instagram API Credentials
    PAGE_ACCESS_TOKEN=YOUR_PAGE_ACCESS_TOKEN
    VERIFY_TOKEN=YOUR_VERIFY_TOKEN
    
    # Optional: Specify a custom CSV file path if not using the default 'conditions.csv'
    CONDITIONS_CSV=conditions.csv
    
    # Optional: Specify the port on which the application will run (default is 5000)
    PORT=5000



