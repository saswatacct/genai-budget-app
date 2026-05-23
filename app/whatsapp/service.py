import os
from twilio.rest import Client
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()


client = Client(
    os.getenv(
        "TWILIO_ACCOUNT_SID"
    ),
    os.getenv(
        "TWILIO_AUTH_TOKEN"
    )
)


def send_whatsapp(
    to,
    body
):

    try:

        message = client.messages.create(

            from_=os.getenv(
                "TWILIO_WHATSAPP_NO"
            ),

            body=body,

            to=f"whatsapp:+91{to}"
        )

        print(
            "TWILIO STATUS:",
            message.status
        )

        print(
            "TWILIO SID:",
            message.sid
        )

        return message.sid

    except Exception as e:

        print(
            "WHATSAPP ERROR:",
            str(e)
        )

        raise