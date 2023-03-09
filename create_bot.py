from aiogram import Bot
from aiogram.dispatcher import Dispatcher
import os
from dotenv import load_dotenv
from aiogram.contrib.fsm_storage.memory import MemoryStorage


load_dotenv()
storage = MemoryStorage()
bot = Bot(token=os.environ.get('TOKEN'))
dp = Dispatcher(bot,storage=storage)