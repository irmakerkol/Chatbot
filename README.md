# Instagram Chatbot Integration with CSV-Based Conditions

This project is a Flask-based application that integrates with the Instagram Graph API to create a highly flexible chatbot. The chatbot uses a CSV file to define keyword-based conditions and returns one or more responses (text messages or button messages) depending on the incoming Instagram message. It mimics ManyChat’s behavior by evaluating multiple conditions and sending multiple messages if needed.

## Features

- **CSV-Based Rule Engine:**  
  Define conditions with fields for:
  - `contains_all` – All listed keywords must be present.
  - `contains_any` – At least one listed keyword must be present.
  - `does_not_contain` – None of the listed keywords should be present.
  
- **Multiple Response Types:**  
  Send plain text responses or rich messages with buttons (in JSON format).

- **Multi-Response Capability:**  
  If an incoming message matches more than one rule, all corresponding responses are sent.

- **Instagram Integration:**  
  The application uses Instagram Graph API for both receiving messages (via webhook) and sending responses.

## Requirements

- Python 3.6+
- Flask
- Requests
- A valid Instagram Business Account with access to the Instagram Graph API

## Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/irmakerkol/Instagram-Chatbot
   cd instagram-chatbot
