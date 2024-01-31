from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram import F
import sqlite3
import aiogram
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import StateFilter

token=("6778733951:AAFroTGR9xZkD_U2vbkMHqAUaNBE1AjLkd0")
bot=Bot(token=token)
dp=Dispatcher()

logging.basicConfig(level=logging.INFO)

@dp.message(Command("start"))
async def Start(message:types.Message):
    await message.answer(text="Приветствую! Вы подписались на бот уведомлений по Гугл Каледндарю!")

async def Main():
    await dp.start_polling(bot)

if __name__=="__main__":
    asyncio.run(Main())