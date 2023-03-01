
from aiogram.utils import executor

from create_bot import dp

from handlers.client import *


a = executor.start_polling(dp, skip_updates=True)
bot_thread = threading.Thread(target=a)
bot_thread.start()