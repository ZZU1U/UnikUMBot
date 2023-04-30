import asyncio
import logging
from init import *
from handlers import *

async def main() -> None:
    """
    This is main function it launches bot
    """
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

# Lets start it!

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())