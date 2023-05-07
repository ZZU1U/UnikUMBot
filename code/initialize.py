import json
from base import Database
from aiogram import Dispatcher, Bot

database = Database('database.db')

dp = Dispatcher()

ORGANIZATIONS = ['УникУм', 'КузГТУ']

TOKEN = json.load(open('secrets.json'))['TOKEN']

WEB_SERVER_HOST = json.load(open('secrets.json'))['WEB_SERVER_HOST']

WEB_SERVER_PORT = json.load(open('secrets.json'))['WEB_SERVER_PORT']

bot = Bot(TOKEN, parse_mode="HTML")
