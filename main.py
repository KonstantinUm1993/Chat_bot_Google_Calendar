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
from aiogram.filters import Command,StateFilter
from aiogram.fsm.context import FSMContext
import datetime
from datetime import date, time, datetime
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]



"""Shows basic usage of the Google Calendar API.
Prints the start and name of the next 10 events on the user's calendar.
"""
creds = None
# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json", SCOPES
        )
        creds = flow.run_local_server(port=0)
# Save the credentials for the next run
with open("token.json", "w") as token:
    token.write(creds.to_json())


service=build("calendar", "v3",  credentials=creds, static_discovery=False)
token=("6778733951:AAFroTGR9xZkD_U2vbkMHqAUaNBE1AjLkd0")
bot=Bot(token=token)
dp=Dispatcher()

logging.basicConfig(level=logging.INFO)

class States(StatesGroup):
    choosing_calendar_name = State()

def create_buttons():
    button_list=[[types.KeyboardButton(text="Выслать расписание на день")], 
                 [types.KeyboardButton(text="Поставить встречу в календаре")], 
                 [types.KeyboardButton(text="Посмотреть расписание встреч коллеги")
                 ]]
    builder=ReplyKeyboardMarkup(keyboard=button_list, resize_keyboard=True)
    return builder


@dp.message(Command("start"))
async def Start(message:types.Message):
    button_list_2=[
        [types.InlineKeyboardButton(text="Расписание на сегодня", callback_data="Today_events")],
        [types.InlineKeyboardButton(text="Поставить встречу в календаре", callback_data="Meeting_create")], 
        [types.InlineKeyboardButton(text="Посмотреть расписание встреч коллеги", callback_data="Show_schedule_of_collegue")]
    ]
    builder=InlineKeyboardMarkup(inline_keyboard=button_list_2)

    await message.answer(text="Приветствую! Вы подписались на бот уведомлений по Гугл Календарю!", reply_markup=builder)


@dp.callback_query(F.data=="Today_events")
async def Text_for_user(callback:types.CallbackQuery):
        
        button_list_2=[
        [types.InlineKeyboardButton(text="Расписание на сегодня", callback_data="Today_events")],
        [types.InlineKeyboardButton(text="Поставить встречу в календаре", callback_data="Meeting_create")], 
        [types.InlineKeyboardButton(text="Посмотреть расписание встреч коллеги", callback_data="Show_schedule_of_collegue")]
    ]
        builder=InlineKeyboardMarkup(inline_keyboard=button_list_2)

        Text = ""
        now=datetime.utcnow().isoformat()+"Z"
        events_results=(service.events().list(calendarId="primary",timeMin=now, timeMax=datetime.combine(date.today(),time.max).isoformat()+"Z", maxResults=5, singleEvents=True, orderBy="startTime").execute())
        Events=events_results.get("items",[])
        for event in Events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            Text += f"{start} {event["summary"]}\n"
        await callback.message.edit_text(text=Text, reply_markup=builder)        
        await callback.answer()
 
@dp.message(F.text, States.choosing_calendar_name)
async def Choosing_calendar_name(message:types.Message, state: FSMContext):

    if message.text == "Сегодня":
        await  message.answer(text="Расписание на сегодня показано", reply_markup=create_buttons())
        await state.clear()
    elif message.text == "Завтра":
        await  message.answer(text="Расписание на завтра показано", reply_markup=create_buttons())
        await state.clear()
    elif message.text == "Другой день": 
        await  message.answer(text="Расписание на другой день показано", reply_markup=create_buttons())
        await state.clear()


    
async def Main():
    await dp.start_polling(bot)

if __name__=="__main__":
    asyncio.run(Main())








   # elif message.text == "Поставить встречу в календаре":
    #     button_list=[[types.KeyboardButton(text="Сегодня")], 
    #              [types.KeyboardButton(text="Завтра")], 
    #              [types.KeyboardButton(text="Другой день")
    #              ],[types.KeyboardButton(text="Назад")
    #              ]]
    #     builder=ReplyKeyboardMarkup(keyboard=button_list, resize_keyboard=True)
    #     await  message.answer(text="Выберите день встречи", reply_markup=builder)
    #     await state.set_state(States.choosing_calendar_name)
    # elif message.text == "Посмотреть расписание встреч коллеги":
    #   await  message.answer(text="Расписание коллег показано")
    # else:
    #   await  message.answer(text="Команда не распознана! Уточните команду!")


