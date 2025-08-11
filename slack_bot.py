import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

client = WebClient(token=os.getenv("SLACK_TOKEN"))

def slack_send_message(message:str):
    """
    Send a message to a Slack channel.

    Args:
        message (str): The message to send.

    Returns:
        None
    """
    try:
        resp = client.chat_postMessage(
            channel=os.getenv("CHANNEL_ID"),   # z.B. "C0123456789"
            text=message,
            blocks=[
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": message}
                }
            ],
        )
        print("Gesendet, ts=", resp["ts"])
    except SlackApiError as e:
        print(f"Fehler: {e.response['error']}")