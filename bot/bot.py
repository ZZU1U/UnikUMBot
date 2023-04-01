import asyncio
import logging
import sqlite3
import requests
import rutimeparser as rt
import datetime as dt
from aiogram import Bot, Dispatcher, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.client.telegram import TelegramAPIServer
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command
from aiogram.types import Message
from bs4 import BeautifulSoup as bs

class Database:
    def __init__(self, path):
        self.connection = sqlite3.connect(path)

        self.cursor = self.connection.cursor()
        
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
        user_id TEXT NOT NULL,
        party TEXT NOT NULL
        );
        """)

        self.connection.commit()
    
    def about_user(self, user_id):
        self.cursor.execute(f"SELECT user_id, party FROM users WHERE user_id = '{user_id}'")
        return self.cursor.fetchall()
    
    def new_user(self, user_id, group=""):
        self.cursor.execute(f"INSERT INTO users (user_id, party) VALUES ('{user_id}', '{group}')")
        self.connection.commit()
    
    def update_info(self, user_id, **args):
        for name, value in args:
            self.cursor.execute(f"UPDATE users SET {name} = '{value}' WHERE user_id = '{user_id}'")
        
        self.connection.commit()


def get_pari(group, datewen):
    PARI_BUDNI = {
        1: ('8:30', '10:00'),
        2: ('10:20', '11:50'),
        4: ('15:20', '16:50'),
        5: ('17:00', '18:30'),
        6: ('18:40', '20:10')
    }

    PARI_WEEKEND = {
        1: ('9:00', '10:30'),
        2: ('10:40', '12:10'),
        3: ('12:30', '14:00'),
        4: ('14:10', '15:40'),
        5: ('16:00', '17:30'),
        6: ('17:40', '19:10')
    }

    date = dt.datetime.now().date()

    URL = f'https://genius-school.kuzstu.ru/wp-content/uploads/{date.year}/{"0"*int(date.month < 10) + str(date.month)}/{group}-1.html'

    r = requests.get(URL)

    r.encoding = 'utf-8'

    soup = bs(r.text, "html.parser")

    vacancies_names = soup.find_all('tr')

    pari = []

    for name in vacancies_names:
        souptemp = bs(str(name), "html.parser")
        spans = souptemp.find_all('span', class_='s1')
        if rt.parse(spans[0].text) != None:
            dat = str(rt.parse(spans[0].text))[-5:]
            if dat == str(datewen)[-5:]:
                pari = [span.text for span in spans]
                break
    
    pari = [(i, j.replace('\n', '')) for i, j in enumerate(pari) if j.replace('\n', '')]
    
    if len(pari) > 1:
        pari_set = {para for _, para in pari[1:]}
        pari_dict = {}

        for id, para in pari[1:]:
            pari_dict[para] = pari_dict.get(para, []) + [id]

        weekno = datewen.weekday()

        if weekno < 5:
            prai = '\n'.join([f" - {pra}: {PARI_BUDNI[times[0]][0]}-{PARI_BUDNI[times[-1]][1]}" for pra, times in pari_dict.items()])
        else:  # 5 Sat, 6 Sun
            prai = '\n'.join([f"{pra}: {PARI_WEEKEND[times[0]][0]}-{PARI_WEEKEND[times[-1]][1]}" for pra, times in pari_dict.items()])
        
        message = f"{datewen.strftime('%m.%d.%Y')} 📚\n{prai}"

    else:
        message = ""
    
    return message


database = Database('database.db')

TOKEN = "6051725809:AAGVinByBrRgEo37-6J1EHx5sm7ZlNbdh-g"

router = Router()

sesi = AiohttpSession(
    api=TelegramAPIServer.from_base('http://localhost:8080')
)


@router.message(Command(commands=["help"]))
async def command_help_handler(message: Message) -> None:
    await message.answer("Вот команды: 'скоро будет'")


@router.message(Command(commands=["start"]))
async def command_start_handler(message: Message) -> None:
    """
    This handler receive messages with `/start` command
    """
    your_name = message.from_user.full_name
    if not database.about_user(message.chat.id):
        database.new_user(message.chat.id)
        await message.answer(f"Привет, это 'официальный' бот от уникума, что-бы ты легко отслеживал свое распианием!\n\
                            Что-бы выбрать группу (изначально это ИП-51) напиши /settings, если захотите поменять, то просто напишите /settings опять.")
    else:
        await message.answer(f"Мы вроде знакомы, ты же {your_name}?\nНо я если что бот, что-бы расписание из уникума смотреть")


@router.message(Command(commands=['settings']))
async def command_settings_handler(message: Message, state: FSMContext) -> None:
    if not database.about_user(message.chat.id)[0][1]:
        await message.answer("Хорошо, напиши свою группу так, как указано на сайте уникума")
    else:
        await message.answer(f"У тебя уже указана группа ({database.about_user(message.chat.id)[0][1]}), но если хочешь - меняй,")
    



@router.message(Command(commands=['tooday']))
async def command_tooday_handler(message: Message) -> None:
    your_name = message.from_user.full_name
    if not database.about_user(message.chat.id)[0][1]:
        await message.answer(f"{your_name}, у тебя не выбран группа, выбери ее с помощью /settings!")
    else:
        pari_info = get_pari(database.about_user(message.chat.id)[0][1], dt.datetime.now().date())
        if pari_info:
            await message.answer(f'Пары на {pari_info}')
        else:
            await message.answer("У тебя на сегодня нет пар!")


@router.message(Command(commands=['lessons']))
async def command_settings_handler(message: Message) -> None:
    your_name = message.from_user.full_name
    for i in range(30):
        pari_info = get_pari(database.about_user(message.chat.id)[0][1], (dt.datetime.now()+dt.timedelta(days=i)).date())
        if pari_info:
            await message.answer(f'Ближайшая пара будет {pari_info}')
            break
    else:
        await message.answer(f'Мне очень жаль, {your_name}, но ближайший месяц у тебя нет пар по расписанию...')


@router.message()
async def echo_handler(message: types.Message) -> None:
    """
    Handler will forward received message back to the sender

    By default, message handler will handle all message types (like text, photo, sticker and etc.)
    """
    await message.answer(f'Прости, я тебя не понимаю(\nИспользуй команды!\nДля справки используй /help')


async def main() -> None:
    # Dispatcher is a root router
    dp = Dispatcher()
    # ... and all other routers should be attached to Dispatcher
    dp.include_router(router)

    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TOKEN, parse_mode="HTML")
    # , session=sesi
    
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())