# Databricks notebook source
dbutils.widgets.text("token_app", "Token for Slack App")
dbutils.widgets.text("token_bot", "Token for Slack Bot")
dbutils.widgets.text("space_id", "Genie Space ID")

# COMMAND ----------

token_app = dbutils.widgets.get("token_app")
token_bot = dbutils.widgets.get("token_bot")
space_id = dbutils.widgets.get("space_id")

# COMMAND ----------

from databricks.sdk import WorkspaceClient

w = WorkspaceClient()

scope_name = f'slack-bot'

w.secrets.create_scope(scope=scope_name)
w.secrets.put_secret(scope=scope_name, key='slack_token_app', string_value=token_app)
w.secrets.put_secret(scope=scope_name, key='slack_token_bot', string_value=token_bot)
w.secrets.put_secret(scope=scope_name, key='genie_space_id', string_value=space_id)
