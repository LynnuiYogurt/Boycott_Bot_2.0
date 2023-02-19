


from aiogram.types import ReplyKeyboardMarkup, KeyboardButton,InlineKeyboardMarkup,InlineKeyboardButton,ReplyKeyboardRemove



check_name = KeyboardButton('Перевірка за назвою',)
lists = KeyboardButton('Списки компаній')
check_photo = KeyboardButton('Перевірка за фото')

kb_client_global = ReplyKeyboardMarkup(resize_keyboard=True)

ua = InlineKeyboardButton(text = '🇺🇦Українські компанії',callback_data='ua')
left = InlineKeyboardButton(text = '🟢Компанії, що покинули ринок',callback_data='left')
stay = InlineKeyboardButton(text = '🔴Компанії, що залишилися на ринку',callback_data='stay')
root = InlineKeyboardButton(text = '🔴🔴Компанії з ришистським корінням',callback_data='root')



kb_client_list = InlineKeyboardMarkup(row_width=1)

kb_client_global.add(check_name).add(lists).add(check_photo)

kb_client_list.add(ua).add(left).add(stay).add(root)
