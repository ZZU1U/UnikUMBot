import json
from base import Database
from aiogram import Dispatcher, Bot

database = Database('database.db')

dp = Dispatcher()

ORGANIZATIONS = ['УникУм', 'КузГТУ']

TOKEN = json.load(open('secrets.json'))['TOKEN']

bot = Bot(TOKEN, parse_mode="HTML")