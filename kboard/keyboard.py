from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Главная информация после команды /start
keyboard = InlineKeyboardMarkup(row_width=2)
keyboard.add(
    InlineKeyboardButton(text="Каталог", callback_data="catalog"),
    InlineKeyboardButton(text="Информация", callback_data="information"),
    InlineKeyboardButton(text="Доставка/Оплата", callback_data="order"),
    InlineKeyboardButton(text="Контакты", callback_data="call")
)

# Кнопка возврата назад
back_keyboard = InlineKeyboardMarkup(row=1)
back_keyboard.add(InlineKeyboardButton(text="Назад", callback_data='back'))

# Управление товарами
setting_keyboard = InlineKeyboardMarkup(row_width=2)
setting_keyboard.add(InlineKeyboardButton(text="Добавить товар", callback_data='add'),
                     InlineKeyboardButton(text="Все товары", callback_data='all_product'),
                     InlineKeyboardButton(text="Список заказов", callback_data='all_order'))

# Кнопки Далее/Назад
next_keyboard = InlineKeyboardMarkup(row_width=1)
next_keyboard.add(InlineKeyboardButton("Далее", callback_data='next_product'),
                  InlineKeyboardButton("Назад", callback_data='back_button'))

# Покупка товара
order_keyboard = InlineKeyboardMarkup(row_width=3)
order_keyboard.add(InlineKeyboardButton(text="Назад", callback_data='back_order_keyboard'),
                   InlineKeyboardButton(text="Купить", callback_data='buy_order_keyboard'),
                   InlineKeyboardButton(text="Далее", callback_data='next_order_keyboard'))

# Продолжить
next_order_keyboard = InlineKeyboardMarkup(row_width=1)
next_order_keyboard.add(InlineKeyboardButton("Перейти к оформлению", callback_data='next_buy_product'))

# Новые Кнопки Далее/Назад
back_order_keyboard = InlineKeyboardMarkup(row_width=2)
back_order_keyboard.add(InlineKeyboardButton(text="Назад", callback_data='user_info_order_back'),
                        InlineKeyboardButton(text="Далее", callback_data='user_info_order_next'),
                        )
