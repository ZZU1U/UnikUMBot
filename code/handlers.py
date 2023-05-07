from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandObject, Text
from keyboards import *
from initialize import *
from parsenew import *
from decorate import *


# A lot handlers


@dp.message(Command(commands=["help"]))
async def command_help_handler(message: Message) -> None:
    """
    This handler receive messages with `/help` command and helps you to navigate
    """
    await message.answer("Привет, я телеграм-бот, который подскажет тебе твое распиание в уникуме!\
    \nСписок команд:\
    \n/start - Поздароваться\
    \n/help - Вызов справки\
    \n/set - Указать группу\
    \n/groups - Список всех доступных групп\
    \n/today - Расписание на сегодня\
    \n/coming - Ближайшие занятия\
    \n/week - Рассписание на текущюю неделю")


@dp.message(Command(commands=['start']))
async def command_start_handler(message: Message) -> None:
    """
    This handler receive messages with `/start` command and start talk with you
    """
    your_name = message.from_user.first_name
    if not database.about_user(message.chat.id):
        database.new_user(message.chat.id)
        await message.answer(f"👋 Привет, это 'официальный' бот от уникума, что-бы ты легко отслеживал свое распианием, давай с тобой познакомимся!\
        \nЧто-бы выбрать группу напиши /set, если захотчешь поменять, то просто напиши /set опять!")
    else:
        await message.answer(f"Мы вроде знакомы, ты же {your_name}? Я тебя помню, а вот ты помнишь свое расписание из уникума?\
        \nЕсли не помнишь, то напиши /today или /coming.")


@dp.message(Command(commands=['set']))
async def command_settings_handler(message: Message, command: CommandObject) -> None:
    """
    This handler receive messages with `/set` command and let you choose your group
    """
    your_name = message.from_user.first_name
    if not command.args:
        await message.answer(f"{your_name}, если хочешь указать группу, то напиши мне так: /set название_твоей_группы.\nКстати, список групп можешь узнать, написа /groups.")
    else:
        group = command.args
        org = ''
        if group in await get_groups('КузГТУ'):
            org = 'КузГТУ'
        elif group in await get_groups('УникУм'):
            org = 'УникУм'
        else:
            await message.answer("Такой группы нет ни в УникУме, ни в КузГТУ, проверь еще раз.\n\
                                 Если хочешь посмотреть список всех доступных групп, то напиши /groups.")
        if org:
            if not database.about_user(message.chat.id)[0][1]:
                if group in await get_groups(org):
                    await message.answer(f"Хорошо, {your_name}, теперь я знаю, где смотреть твоё расписание.")
                    database.update_info(message.chat.id, party=group, organization=org)
            else:
                cur_args = database.about_user(message.chat.id)[0]
                # cur_args[0] is id...
                cur_grp = cur_args[1]
                cur_org = cur_args[2]
                if cur_grp == group:
                    await message.answer(f"Я знаю, что ты из {cur_grp}, ты мне уже говорил.")
                else:
                    if org == cur_org:
                        await message.answer(f"Раньше ты учился в {cur_grp}, но теперь ты перешел в {group}.")
                        database.update_info(message.chat.id, party=group)
                    else:
                        await message.answer(f"Ого, я думал ты просто группу поменять хотел, а ты еще дальше пошел...\nВот скажи, разве {org} лучше, чем {cur_org}?")
                        database.update_info(message.chat.id, party=group, organization=org)


@dp.message(Command(commands=['groups']))
async def command_groups_handler(message: Message, command: CommandObject) -> None:
    """
    This handler receive messages with `/groups` command and gives you a list of groups for your organization
    """

    await message.answer("Окей, выбери название своей организации.", reply_markup=organizations_keyboard)


@dp.message(Command(commands=['today']))
async def command_today_schedule_handler(message: Message) -> None:
    """
    This handler receive messages with `/today` command and tell you your lessons for today or says you are free now
    """
    your_name = message.from_user.first_name
    if not (info := database.about_user(message.chat.id)[0])[1]:
        await message.answer(f"{your_name}, у тебя не выбран группа. 🧐\
        \nВыбери ее с помощью /set!")
    else:
        pari_info = await get_lessons(info[2], info[1], 'today')
        print(pari_info)
        if len(pari_info) > 1:
            await message.answer(create_beautiful_table(pari_info, 'tooday', org=info[2]), parse_mode='Markdown')
        else:
            await message.answer("У тебя на сегодня нет пар! 😴")


@dp.message(Command(commands=['coming']))
async def command_coming_lessons_handler(message: Message) -> None:
    """
    This handler receive messages with `/coming` command and tell you about your closest lessons
    """
    your_name = message.from_user.first_name
    if not (info := database.about_user(message.chat.id)[0])[1]:
        await message.answer(f"{your_name}, у тебя не выбран группа. 🧐\
                \nВыбери ее с помощью /set!")
    else:
        pari_info = await get_lessons(info[2], info[1], 'coming')
        if len(pari_info) > 1:
            await message.answer(create_beautiful_table(pari_info, 'coming', org=info[2]), parse_mode='Markdown')
        else:
            await message.answer(f'Мне очень жаль, {your_name}, но ближайший месяц у тебя нет пар по расписанию. 😴')


@dp.message(Command(commands=['week']))
async def command_week_schedule_handler(message: Message) -> None:
    """
    This handler receive messages with `/week` command and tell you your week schedule
    """
    your_name = message.from_user.first_name
    if not (info := database.about_user(message.chat.id)[0])[1]:
        await message.answer(f"{your_name}, у тебя не выбран группа. 🧐\
                \nВыбери ее с помощью /set!")
    else:
        pari_info = await get_lessons(info[2], info[1], 'week')
        if pari_info:
            await message.answer(create_beautiful_table(pari_info, 'week', org=info[2]), parse_mode='Markdown')
        else:
            await message.answer(f'Мне очень жаль, {your_name}, но ближайшую неделю у тебя нет пар по расписанию. 😴')


@dp.message()
async def default_handler(message: Message) -> None:
    """
    This handler receive all over messages
    """
    await message.answer(f'Прости, я тебя не понимаю. 😰\
    \nИспользуй команды, что-бы общаться со мной!\
    \nЧто-бы узнать больше о командах напиши /help.')

# A little callbacks

@dp.callback_query(Text("kuzgtu"))
async def send_list_of_kuzgtu_groups(callback: CallbackQuery) -> None:
    """
    This callback function activates when you need list of kuzgtu groups
    """
    await callback.message.answer(create_beautiful_list(await get_groups('КузГТУ'), 'КузГТУ'), parse_mode='Markdown')
    await callback.answer()

@dp.callback_query(Text("unikum"))
async def send_list_of_unikum_groups(callback: CallbackQuery) -> None:
    """
    This callback function activates when you need list of unikum groups
    """
    await callback.message.answer(create_beautiful_list(await get_groups('УникУм'), 'УникУм'), parse_mode='Markdown')
    await callback.answer()