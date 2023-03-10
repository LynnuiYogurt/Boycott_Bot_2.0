
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton,InlineKeyboardMarkup,InlineKeyboardButton,ReplyKeyboardRemove



check_name = KeyboardButton('Перевірка за назвою',)
lists = KeyboardButton('Списки компаній')
check_photo = KeyboardButton('Перевірка за фото')

kb_client_global = ReplyKeyboardMarkup(resize_keyboard=True)

ua = InlineKeyboardButton(text = '🇺🇦Українські компанії',callback_data='ua')
left = InlineKeyboardButton(text = '🟢Компанії, що покинули ринок',callback_data='left')
stay = InlineKeyboardButton(text = '🔴Компанії, що залишилися на ринку',callback_data='stay')
root = InlineKeyboardButton(text = '🔴🔴Компанії з рашистським корінням',callback_data='root')



kb_client_list = InlineKeyboardMarkup(row_width=1)

kb_client_global.add(check_name).add(lists).add(check_photo)

kb_client_list.add(ua).add(left).add(stay).add(root)

class CompanySearchOptions:
    def __init__(self, matching_companies):
        self.matching_companies = matching_companies
        self.options = [f"{i + 1}. {company.name}" for i, company in enumerate(matching_companies)]

    def get_inline_keyboard(self):
        keyboard = InlineKeyboardMarkup(row_width=1)
        for i, option in enumerate(self.options):
            keyboard.add(InlineKeyboardButton(option, callback_data=f"company_search_{i}"))
        return keyboard
