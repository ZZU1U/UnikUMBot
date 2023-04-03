import asyncio
import logging
from aiogram import Bot
from base import dp, database, TOKEN
from aiogram import types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.filters import CommandObject
from parse import getLessons, isGroup
import datetime as dt


@dp.message(Command(commands=["help"]))
async def command_help_handler(message: Message) -> None:
    await message.answer("Привет, я телеграм-бот, который подскажет тебе твое распиание в уникуме!\nСписок команд:\n/start - поздороваться со мной\n/settings - рассказать мне из какой ты группы\n/help - справка\n/tooday - расписание на сегодня\n/lessons - ближиайшие пары")


@dp.message(Command(commands=["start"]))
async def command_start_handler(message: Message) -> None:
    """
    This handler receive messages with `/start` command
    """
    your_name = message.from_user.full_name
    if not database.about_user(message.chat.id):
        database.new_user(message.chat.id)
        await message.answer(f"Привет, это 'официальный' бот от уникума, что-бы ты легко отслеживал свое распианием, давай с тобой познакомимся!\nЧто-бы выбрать группу напиши /settings, если захотчешь поменять, то просто напиши /settings опять!")
    else:
        await message.answer(f"Мы вроде знакомы, ты же {your_name}? Я тебя помню, а вот ты помнишь свое расписание из уникума?\nЕсли не помнишь, то напиши /tooday или /lessons.")


@dp.message(Command(commands=['set']))
async def command_settings_handler(message: Message, command: CommandObject) -> None:
    if not command.args:
        await message.answer("При вызове команды укажи свою группу!\nНа пример так - /settigns ИИ-82.")
    elif isGroup(command.args):
        if not database.about_user(message.chat.id)[0][1]:
            await message.answer(f"Хорошо, теперь твоя группа - {command.args}.")
            database.update_info(message.chat.id, party=command.args)
        else:
            await message.answer(f"У тебя уже была указана группа - {database.about_user(message.chat.id)[0][1]}, но теперь ты перешел в {command.args}.")
            database.update_info(message.chat.id, party=command.args)
    else:
        await message.answer(f"Группы {command.args} нет в уникуме, может ты ошибся...")



@dp.message(Command(commands=['tooday']))
async def command_tooday_handler(message: Message) -> None:
    your_name = message.from_user.full_name
    if not database.about_user(message.chat.id)[0][1]:
        await message.answer(f"{your_name}, у тебя не выбран группа, выбери ее с помощью /settings!")
    else:
        pari_info = getLessons(database.about_user(message.chat.id)[0][1])
        if pari_info:
            await message.answer(f'Пары на {pari_info}')
        else:
            await message.answer("У тебя на сегодня нет пар!")


@dp.message(Command(commands=['lessons']))
async def command_settings_handler(message: Message) -> None:
    your_name = message.from_user.full_name
    if not database.about_user(message.chat.id)[0][1]:
        await message.answer(f"{your_name}, у тебя не выбран группа, выбери ее с помощью /settings!")
    else:
        pari_info = getLessons(database.about_user(message.chat.id)[0][1], date='anywhen')
        if pari_info:
            await message.answer(f'Ближайшая пара будет {pari_info}')
        else:
            await message.answer(f'Мне очень жаль, {your_name}, но ближайший месяц у тебя нет пар по расписанию...')


@dp.message()
async def default_handler(message: types.Message) -> None:
    await message.answer(f'Прости, я тебя не понимаю(\nИспользуй команды!\nДля справки используй /help')


async def main() -> None:
    bot = Bot(TOKEN, parse_mode="HTML")

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
