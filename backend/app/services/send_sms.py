from twilio.rest import Client
import os


def send_emergency_sms(
    to_phone: str,
    message: str
) -> None:
    """
    Sends an emergency SMS alert.

    Args:
        to_phone (str): Recipient phone number (with country code)
        message (str): Emergency message
    """

    try:
        # Twilio credentials (store in environment variables)
        account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        from_phone = os.getenv("TWILIO_PHONE_NUMBER")

        client = Client(account_sid, auth_token)

        sms = client.messages.create(
            body=message,
            from_=from_phone,
            to=to_phone
        )

        print(f"Emergency SMS sent. SID: {sms.sid}")

    except Exception as e:
        print(f"Failed to send emergency SMS: {e}")