from databricks.sdk import WorkspaceClient

w = WorkspaceClient()

def get_genie_space_id():
    """
    Retrieves the Genie space ID from the Databricks secrets store.

    Returns:
        str: The Genie space ID retrieved from the specified secret scope and key.

    Raises:
        Exception: If the secret cannot be retrieved or does not exist.
    """
    return w.dbutils.secrets.get(scope='slack-bot', key='genie_space_id')

def get_slack_auth():
    """
    Retrieves Slack authentication tokens from the specified secret scope.

    Returns:
        tuple: A tuple containing two strings:
            - token_app (str): The Slack app-level token.
            - token_bot (str): The Slack bot-level token.

    Raises:
        Exception: If the secrets cannot be retrieved from the specified scope or keys.
    """
    token_app = w.dbutils.secrets.get(scope='slack-bot', key='slack_token_app')
    token_bot = w.dbutils.secrets.get(scope='slack-bot', key='slack_token_bot')
    return token_app, token_bot
