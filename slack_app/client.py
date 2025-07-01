import ssl
from slack_sdk.web.async_client import AsyncWebClient
from slack_bolt.async_app import AsyncApp
from config.secrets import get_slack_auth

token_app, token_bot = get_slack_auth()

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

client = AsyncWebClient(token=token_bot, ssl=ssl_context)
app = AsyncApp(client=client, process_before_response=False)
