"""
Test WhatsApp Message Sender using Twilio Sandbox
-------------------------------------------------

This script sends a test WhatsApp message using Twilio.
Make sure you have:

1. Created a Twilio account
2. Joined the Twilio WhatsApp sandbox
3. Set environment variables:
   TWILIO_ACCOUNT_SID
   TWILIO_AUTH_TOKEN
"""

import os
from twilio.rest import Client
from app.services.send_whatsapp_message import send_whatsapp_message
from app.core.logging_config import setup_logger


logger = setup_logger(__name__)


def test_send_whatsapp_message():
    """
    Send a test WhatsApp message using Twilio sandbox.
    """

    try:
       
        

        # Replace with your test number
        to_whatsapp = "+919539749441"

        send_whatsapp_message(to_whatsapp, "Hello from Alma! This is a test message.")

       

        print("✅ Message sent successfully!")
        
    except Exception as e:
        print("❌ Failed to send message")
        print(str(e))


if __name__ == "__main__":
    test_send_whatsapp_message()
