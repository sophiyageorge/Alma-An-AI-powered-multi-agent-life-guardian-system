from twilio.rest import Client
import os
from app.core.logging_config import setup_logger
from dotenv import load_dotenv


logger = setup_logger(__name__)

def send_whatsapp_message(to_number: str, message: str) -> str:
        """
        Sends a WhatsApp message via Twilio sandbox.

        Args:
            to_number (str): Recipient phone number with country code (e.g., +91xxxxxxxxxx)
            message (str): Message content

        Returns:
            str: Twilio message SID
        """
        try:

            load_dotenv()

            
            account_sid = os.getenv("TWILIO_ACCOUNT_SID")
            auth_token = os.getenv("TWILIO_AUTH_TOKEN")
            phone_number = os.getenv("TWILIO_PHONE_NUMBER")
            print(account_sid, auth_token, phone_number)

            # from_whatsapp = f"whatsapp:{to_number}"  # Twilio sandbox number
            # to_whatsapp = f"whatsapp:{to_number}"

            if not account_sid or not auth_token or not phone_number:
                    raise ValueError("Twilio credentials missing. Check environment variables.")

            client = Client(account_sid, auth_token)

            from_whatsapp = f"whatsapp:{phone_number}"
            to_whatsapp = f"whatsapp:{to_number}"
            message = message.strip()

            sent_msg = client.messages.create(
                body=message,
                from_=from_whatsapp,
                to=to_whatsapp
            )

            logger.info("WhatsApp message sent successfully | SID=%s | to=%s", sent_msg.sid, to_number)
            
            return sent_msg.sid

        except Exception as e:
            logger.exception("Failed to send WhatsApp message to %s", to_number)
            raise  
