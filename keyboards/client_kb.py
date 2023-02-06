

from aiogram.utils.callback_data import CallbackData
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton,InlineKeyboardMarkup,InlineKeyboardButton,ReplyKeyboardRemove


cb_inline = CallbackData("post", 'action', "data")

chek_name = KeyboardButton('Перевірка за назвою')
lists = KeyboardButton('Списки компаній')
chek_photo = KeyboardButton('Перевірка за фото')

kb_client_global = ReplyKeyboardMarkup(resize_keyboard=True)

ua = InlineKeyboardButton(text = '🇺🇦Українські компанії',callback_data=cb_inline.new(action='ua', data='MyText'))
left = InlineKeyboardButton(text = '🟢Компанії, що покинули ринок',callback_data=cb_inline.new(action='left', data='MyText1'))
stay = InlineKeyboardButton(text = '🔴Компанії, що залишилися на ринку',callback_data=cb_inline.new(action='stay', data='MyText2'))
root = InlineKeyboardButton(text = '🔴🔴Компанії з ришистським корінням',callback_data=cb_inline.new(action='root', data='MyText3'))



kb_client_list = InlineKeyboardMarkup(row_width=1)

kb_client_global.add(chek_name).add(lists).add(chek_photo)

kb_client_list.add(ua).add(left).add(stay).add(root)
