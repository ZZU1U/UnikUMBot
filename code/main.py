import logging
import asyncio
from initialize import *
from handlers import *


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
    logging.basicConfig(level=logging.INFO)
