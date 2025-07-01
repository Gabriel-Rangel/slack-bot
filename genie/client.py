from databricks.sdk import WorkspaceClient
from config.secrets import get_genie_space_id

w = WorkspaceClient()
genie = w.genie
space_id = get_genie_space_id()
