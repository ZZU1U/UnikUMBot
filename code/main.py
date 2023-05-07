import logging
from aiohttp import web
from aiogram.webhook.aiohttp_server import setup_application
from initialize import *
from handlers import *


def main() -> None:
    app = web.Application()

    setup_application(app, dp, bot=bot)

    web.run_app(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)


# Lets start it!

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
