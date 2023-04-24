import asyncio
import logging
from aiogram import Bot
from base import dp, database, TOKEN
from aiogram import types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.filters import CommandObject
from parse import getLessons, isGroup


@dp.message(Command(commands=["help"]))
async def command_help_handler(message: Message) -> None:
    """
    This handler receive messages with `/help` command and helps you to navigate
    """
    await message.answer("Привет, я телеграм-бот, который подскажет тебе твое распиание в уникуме!\
    \nСписок команд:\
    \n/start - Поздароваться\
    \n/set - Указать группу\
    \n/help - Вызов справки\
    \n/today - Расписание на сегодня\
    \n/coming - Ближайшие занятия")


@dp.message(Command(commands=["start"]))
async def command_start_handler(message: Message) -> None:
    """
    This handler receive messages with `/start` command and start talk with you
    """
    your_name = message.from_user.full_name
    if not database.about_user(message.chat.id):
        database.new_user(message.chat.id)
        await message.answer(f"Привет, это 'официальный' бот от уникума, что-бы ты легко отслеживал свое распианием, давай с тобой познакомимся!\
        \nЧто-бы выбрать группу напиши /set, если захотчешь поменять, то просто напиши /set опять!")
    else:
        await message.answer(f"Мы вроде знакомы, ты же {your_name}? Я тебя помню, а вот ты помнишь свое расписание из уникума?\
        \nЕсли не помнишь, то напиши /today или /coming.")


@dp.message(Command(commands=['set']))
async def command_settings_handler(message: Message, command: CommandObject) -> None:
    """
    This handler receive messages with `/set` command and let you choose your group
    """
    if not command.args:
        await message.answer("При вызове команды укажи свою группу!\nНа пример так - /set ИИ-82.")
    elif isGroup(command.args):
        if not database.about_user(message.chat.id)[0][1]:
            await message.answer(f"Хорошо, теперь твоя группа - {command.args}. 🥳")
            database.update_info(message.chat.id, party=command.args)
        else:
            cur_grp = database.about_user(message.chat.id)[0][1]
            if cur_grp == command.args:
                await message.answer(f"Я знаю, что ты из этой группу, ты мне уже говорил. 😉")
            else:
                await message.answer(f"У тебя уже была указана группа - {cur_grp}, но теперь ты перешел в {command.args}. 🥳")
                database.update_info(message.chat.id, party=command.args)
    else:
        await message.answer(f"Группы {command.args} нет в уникуме, может ты ошибся? 😕")


@dp.message(Command(commands=['today']))
async def command_today_handler(message: Message) -> None:
    """
    This handler receive messages with `/today` command and tell you your lessons for today or says you are free now
    """
    your_name = message.from_user.full_name
    if not database.about_user(message.chat.id)[0][1]:
        await message.answer(f"{your_name}, у тебя не выбран группа. 🧐\
        \nВыбери ее с помощью /set!")
    else:
        pari_info = getLessons(database.about_user(message.chat.id)[0][1])
        if pari_info:
            await message.answer(f'Пары на {pari_info}')
        else:
            await message.answer("У тебя на сегодня нет пар! 😴")


@dp.message(Command(commands=['coming']))
async def command_settings_handler(message: Message) -> None:
    """
    This handler receive messages with `/coming` command and tell you about your closest lessons
    """
    your_name = message.from_user.full_name
    if not database.about_user(message.chat.id)[0][1]:
        await message.answer(f"{your_name}, у тебя не выбран группа. 🧐\
                \nВыбери ее с помощью /set!")
    else:
        pari_info = getLessons(database.about_user(message.chat.id)[0][1], date='anywhen')
        if pari_info:
            await message.answer(f'Ближайшая пара будет в {pari_info}')
        else:
            await message.answer(f'Мне очень жаль, {your_name}, но ближайший месяц у тебя нет пар по расписанию. 😴')


@dp.message()
async def default_handler(message: types.Message) -> None:
    """
    This handler receive all over messages
    """
    await message.answer(f'Прости, я тебя не понимаю. 😰\
    \nИспользуй команды, что-бы общаться со мной!\
    \nЧто-бы узнать больше о командах напиши /help.')


async def main() -> None:
    """
    This is main function it launches bot
    """
    bot = Bot(TOKEN, parse_mode="HTML")

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

# Lets start endless cycle!
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
