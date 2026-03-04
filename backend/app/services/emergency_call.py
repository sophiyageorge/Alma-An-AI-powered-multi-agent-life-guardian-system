from twilio.rest import Client
import os


def make_emergency_call(to_phone: str) -> None:
    """
    Initiates an automated emergency voice call.
    """

    try:
        account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        from_phone = os.getenv("TWILIO_PHONE_NUMBER")

        client = Client(account_sid, auth_token)

        call = client.calls.create(
            twiml="""
                <Response>
                    <Say voice="alice">
                        Emergency alert. Critical health condition detected.
                        Please check immediately.
                    </Say>
                </Response>
            """,
            from_=from_phone,
            to=to_phone
        )

        print(f"Emergency Call initiated. SID: {call.sid}")

    except Exception as e:
        print(f"Failed to initiate call: {e}")