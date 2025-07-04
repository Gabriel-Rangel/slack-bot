from genie.client import genie

def format_genie_response(genie_message):
    query_desc = query_code = table_text = None

    query = genie_message.attachments[0].query
    text = genie_message.attachments[0].text

    text_content = text.content if text else None
    if query:
        query_desc = query.description if query else None
        query_code = query.query if query else None


        query_result = genie.get_message_attachment_query_result(
            genie_message.space_id,
            genie_message.conversation_id,
            genie_message.message_id,
            genie_message.attachments[0].attachment_id
        )
        columns = [col.name for col in query_result.statement_response.manifest.schema.columns]
        data_array = query_result.statement_response.result.data_array
        # Determine maximum width for each column (consider header and row values)
        widths = [len(col) for col in columns]
        for row in data_array:
            for i, cell in enumerate(row):
                widths[i] = max(widths[i], len(str(cell)))

        # Create the header row
        header = " | ".join(col.ljust(widths[i]) for i, col in enumerate(columns))
        # Create a separator row
        separator = "-|-".join("-" * widths[i] for i in range(len(columns)))

        # Build the rows of the table
        rows = [header, separator]
        for row in data_array:
            row_str = " | ".join(str(cell).ljust(widths[i]) for i, cell in enumerate(row))
            rows.append(row_str)

        # Wrap the table in triple backticks to format as a code block

        table_text =  "```\n" + "\n".join(rows) + "\n```"
    text_result = "\n".join([s for s in [text_content, query_desc, table_text, query_code] if s])
    return text_result