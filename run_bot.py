
from aiogram.utils import executor

from create_bot import dp

from handlers.client import *


executor.start_polling(dp, skip_updates=True)
