from genie.client import genie, space_id
from genie.polling import async_genie_start_conv, async_genie_create_message
from genie.formatting import format_genie_response
from slack_app.utils import extract_text, send_thinking_message, delete_message

conv_tracker = {}

def register_events(app):
    """
    Registers event handlers for the Slack app.

    This function attaches an asynchronous event handler for the "message" event. When a message is received, it processes the message by:
    - Sending a temporary "thinking" message.
    - Extracting the thread timestamp and tracking conversation state.
    - Starting a new conversation or continuing an existing one with an external service (genie).
    - Formatting and sending the response back to the Slack thread.
    - Handling exceptions and cleaning up temporary messages.

    Args:
        app: The Slack Bolt app instance to register events on.

    Returns:
        None
    """
    @app.event("message")
    async def message_hello(message, say, client):
        thinking_ts = await send_thinking_message(say)
        thread_ts = message.get("thread_ts")
        conv_id = conv_tracker.get(thread_ts)
        query = extract_text(message)
        try:
            if not conv_id:
                genie_message = await async_genie_start_conv(space_id, query)
                conv_tracker[thread_ts] = genie_message.conversation_id
            else:
                genie_message = await async_genie_create_message(space_id, conv_id, query)
            text = format_genie_response(genie_message)
        except Exception as e:
            text = str(e)
        await delete_message(message.get("channel"), thinking_ts)
        await say(text=text, thread_ts=thread_ts)
