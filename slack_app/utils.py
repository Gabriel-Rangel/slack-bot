from slack_app.client import app

def extract_text(message):
    """
    Extracts and concatenates text from the nested elements of a Slack message's blocks.

    Args:
        message (dict): A dictionary representing a Slack message, expected to contain a "blocks" key with a list of block objects.

    Returns:
        str: The concatenated text extracted from all nested elements within the message blocks.

    Note:
        This function assumes a specific structure for the Slack message, where each block contains "elements",
        and each element contains its own "elements" list with dictionaries having "type" and "text" keys.
    """
    query = ""
    for block in message["blocks"]:
        for element in block["elements"]:
            query = "".join([text["text"] if text["type"] else "" for text in element["elements"]])
    return query

async def send_thinking_message(say):
    """
    Sends a "Genie is thinking..." message using the provided 'say' function and returns the message timestamp.

    Args:
        say (Callable): An asynchronous function to send a message (typically from Slack Bolt).

    Returns:
        str or None: The timestamp ('ts') of the sent message if available, otherwise None.
    """
    response = await say(text="Genie is thinking...")
    return response.get("ts")

async def delete_message(channel, ts):
    """
    Asynchronously deletes a message from a specified Slack channel.

    Args:
        channel (str): The ID of the Slack channel from which to delete the message.
        ts (str): The timestamp identifier of the message to be deleted.

    Raises:
        Exception: If an error occurs while attempting to delete the message, it is caught and printed.
    """
    try:
        await app.client.chat_delete(channel=channel, ts=ts)
    except Exception as e:
        print(f"Error deleting message: {e}")
