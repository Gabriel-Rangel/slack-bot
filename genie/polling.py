import asyncio
from functools import wraps
from genie.client import genie

def message_poll(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        result_waiter = func(*args, **kwargs)
        poll_count = 0
        wait = 5
        while poll_count < 20:
            message = genie.get_message(
                result_waiter.space_id,
                result_waiter.conversation_id,
                result_waiter.message_id
            )
            if message.status.value == "COMPLETED":
                return result_waiter.result()
            elif message.status.value == "FAILED":
                raise LookupError("Genie failed to return a response")
            poll_count += 1
            await asyncio.sleep(wait)
        raise TimeoutError("Genie did not return a response")
    return wrapper

@message_poll
def async_genie_start_conv(*args, **kwargs):
    return genie.start_conversation(*args, **kwargs)

@message_poll
def async_genie_create_message(*args, **kwargs):
    return genie.create_message(*args, **kwargs)
