import asyncio
from slack_app.client import app, token_app
from slack_app.events import register_events

async def main():
    register_events(app)
    from slack_bolt.adapter.socket_mode.aiohttp import AsyncSocketModeHandler
    handler = AsyncSocketModeHandler(app, token_app)
    await handler.start_async()

if __name__ == "__main__":
    asyncio.run(main())

