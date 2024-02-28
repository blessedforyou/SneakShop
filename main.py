from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import CallbackQuery
from database import database as db
from kboard import keyboard as kb
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from setting import TOKEN


bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


async def on_startup(_):
    await db.database_info()
    await db.information_user()


# Класс для добавления Товаров.
class ProductAdd(StatesGroup):
    name = State()
    description = State()
    price = State()
    size = State()
    color = State()
    photo = State()


# Класс для создания Заказов.
class Order(StatesGroup):
    name = State()
    city = State()
    color = State()
    size = State()
    delivery = State()


# Функция обратной кнопки
def back():
    # Обработка кнопки назад
    @dp.callback_query_handler(lambda call: call.data == 'back')
    async def button_back(call: types.CallbackQuery):
        await call.bot.edit_message_text(message_id=call.message.message_id,
                                         chat_id=call.message.chat.id,
                                         text="MeduzaShop - интернет-магазин для тебя и для всех тех, "
                                              "кто любит хорошо выглядеть.",
                                         reply_markup=kb.keyboard)


# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):

    if message.chat.type != 'private':
        await message.answer("Использование доступно только в личных сообщениях.")
    else:
        await message.answer("Добро пожаловать в Интернет-Магазин MeduzaShop. Для работы введите команду /shop.")


# Обработчик команды /shop
@dp.message_handler(commands=['shop'])
async def shop(message: types.Message):

    if message.chat.type == 'private':
        await message.answer("MeduzaShop - интернет-магазин для тебя и для всех тех, кто любит хорошо выглядеть.",
                             reply_markup=kb.keyboard)
    else:
        await message.answer("Использование доступно только в личных сообщениях.")


# Обработчик нажатия на кнопку Информация
@dp.callback_query_handler(lambda call: call.data == 'information')
async def button_info(call: types.CallbackQuery):
    await bot.edit_message_text(message_id=call.message.message_id,
                                chat_id=call.message.chat.id,
                                text="<b>Информация о нас</b>\n\n"
                                     "📍 Магазин расположен в г.Светлоград.\n"
                                     "👟 У нас большой ассортимент кроссовок, а также имеется "
                                     "возможность приобретения товаров под заказ.\n\n"
                                     "Если у вас остались вопросы, обращайтесь к нам в <b>WhatsApp</b>:\n"
                                     "+7 918 769 02 10; +7 918 872 18 36",
                                reply_markup=kb.back_keyboard,
                                parse_mode='html')
    # Вызов функции обратной клавиши
    back()


# Обработка клавиши Связь
@dp.callback_query_handler(lambda call: call.data == 'call')
async def call_button(call: types.CallbackQuery):
    await bot.edit_message_text(message_id=call.message.message_id,
                                chat_id=call.message.chat.id,
                                text="<b>WhatsApp</b>: +7 918 769 02 10; +7 918 872 18 36\n"
                                     "<b>Instagram</b>: meduza__.club\n"
                                     "<b>Telegram</b>: @Meduzaclub777",
                                reply_markup=kb.back_keyboard,
                                parse_mode='html')

    back()


# Обработка клавиши Доставка/Оплата
@dp.callback_query_handler(lambda call: call.data == 'order')
async def order_button(call: types.CallbackQuery):
    await bot.edit_message_text(message_id=call.message.message_id,
                                chat_id=call.message.chat.id,
                                text="<b>Бесплатная доставка</b> курьером осуществляется только в "
                                     "г.Светлоград и Ставрополь.\n\n"
                                     "В остальные города России осуществляется <b>Платная доставка</b> с помощью:\n\n"
                                     "-Почты России\n"
                                     "-СДЭК\n"
                                     "-Рейсовых автобусов\n\n"
                                     "<i>При доставке товара вам отправляется фото или видео обзор на товар</i>.",
                                reply_markup=kb.back_keyboard,
                                parse_mode='html')
    back()


@dp.message_handler(commands=['apanel'])
async def apanel(message: types.Message):
    username = message.from_user.username

    if message.chat.type == 'private' and (username == 'diditsa'):
        await bot.send_message(message.chat.id,
                               "Добро пожаловать в Админ-Панель.",
                               reply_markup=kb.setting_keyboard)
    else:
        await bot.send_message(message.chat.id,
                               "Вы не являетесь администратором.")


# Добавление товара в БД.
@dp.callback_query_handler(lambda call: call.data == 'add')
async def add_button(call: types.CallbackQuery):
    await ProductAdd.name.set()
    await call.bot.edit_message_text(message_id=call.message.message_id,
                                     chat_id=call.message.chat.id,
                                     text="Введите название товара.",
                                     reply_markup=None)


@dp.message_handler(state=ProductAdd.name)
async def add_product_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await message.answer("Введите описание товара.")
    await ProductAdd.next()


@dp.message_handler(state=ProductAdd.description)
async def add_product_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
    await message.answer("Введите цену товара.")
    await ProductAdd.next()


@dp.message_handler(state=ProductAdd.price)
async def add_product_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text
    await message.answer('Введите доступные размеры через /')
    await ProductAdd.next()


@dp.message_handler(state=ProductAdd.size)
async def add_product_size(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['size'] = message.text
    await message.answer('Введите цвет товара.')
    await ProductAdd.next()


@dp.message_handler(state=ProductAdd.color)
async def add_product_color(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['color'] = message.text
    await message.answer('Введите ссылку на конечную фотографию товара.')
    await ProductAdd.next()


@dp.message_handler(state=ProductAdd.photo)
async def add_product_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.text
    await db.insert_product(state)
    await message.answer('Товар успешно создан.')
    await state.finish()


# Удаление товара из БД
@dp.message_handler(commands=['delete_product'])
async def delete_product(message: types.Message):

    # ИД продукта
    id_product = db.cursor.execute("SELECT id FROM product").fetchall()

    # Список со всеми продуктами
    all_product_id = []

    # Перебор всех ID и добавление их в список.
    for product in id_product:
        return all_product_id.append(product[0])

    # Разделение сообщения на две части.
    message_split = message.text.split()

    # Проверка условия длины сообщения.
    if len(message_split) < 2:
        await message.answer("Ошибка ввода.\n\n"
                             "Корректный ввод - /delete_product <ID>")
        return

    try:
        send_id_product = int(message_split[1])

        # Если введённого ID товара нет в списке.
        if send_id_product not in all_product_id:
            await message.answer(f"Товара с ID {send_id_product} не существует.")
            return

        # Если введенный ID был найден в списке.
        if ((message.chat.type == 'private') and (send_id_product in all_product_id) and
                (message.from_user.username == 'diditsa')):

            db.cursor.execute("DELETE FROM product WHERE id = ?", (send_id_product,))
            db.conn.commit()
            await message.answer("Товар был удален.")

        else:
            await message.answer("У вас нет доступа к удалению товаров.")

    except ValueError or TypeError:

        if ValueError:
            await message.answer('Ошибка ввода.')
        elif TypeError:
            await message.answer(f'Товара с ID: {message_split[1]} не существует.')


# Информация обо всех товарах
@dp.callback_query_handler(lambda call: call.data == 'all_product')
async def all_product(call: CallbackQuery):

    # Выбор текущего товара из БД по ID
    current_product = db.cursor.execute("SELECT * FROM product WHERE id = ?", (db.current_product_id,)).fetchone()

    # Если товар есть.
    if current_product:
        await bot.edit_message_text(chat_id=call.message.chat.id,
                                    message_id=call.message.message_id,
                                    text=f"ID товара: {current_product[0]}\nНазвание: {current_product[1]}\n"
                                         f"Описание: {current_product[2]}", reply_markup=kb.next_keyboard)
    else:
        await bot.edit_message_text(chat_id=call.message.chat.id,
                                    message_id=call.message.message_id,
                                    text="В базе данных нет товаров, добавьте их.",
                                    )


# Обработка нажатия на кнопку Далее.
@dp.callback_query_handler(lambda call: call.data == 'next_product')
async def next_product(call: types.CallbackQuery):
    db.current_product_id += 1
    current_product = db.cursor.execute("SELECT * FROM product WHERE id = ?", (db.current_product_id,)).fetchone()

    if current_product:
        await bot.edit_message_text(chat_id=call.message.chat.id,
                                    message_id=call.message.message_id,
                                    text=f"ID товара: {current_product[0]}\n"
                                         f"Название: {current_product[1]}\n"
                                         f"Описание: {current_product[2]}", reply_markup=kb.next_keyboard)
    else:
        await bot.answer_callback_query(callback_query_id=call.id, text="Товары закончились!")
        db.current_product_id -= 1


@dp.callback_query_handler(lambda call: call.data == 'back_button')
async def back_button(call: types.CallbackQuery):
    db.current_product_id -= 1
    current_product = db.cursor.execute("SELECT * FROM product WHERE id = ?", (db.current_product_id,)).fetchone()

    if current_product:
        await bot.edit_message_text(chat_id=call.message.chat.id,
                                    message_id=call.message.message_id,
                                    text=f"ID товара: {current_product[0]}\n"
                                         f"Название: {current_product[1]}\n"
                                         f"Описание: {current_product[2]}", reply_markup=kb.next_keyboard)
    else:
        await bot.edit_message_text(chat_id=call.message.chat.id,
                                    message_id=call.message.message_id,
                                    text="Добро пожаловать в Админ-Панель",
                                    reply_markup=kb.setting_keyboard)
        db.current_product_id = 1


# Обработка кнопки Каталог.
@dp.callback_query_handler(lambda call: call.data == 'catalog')
async def catalog_button(call: types.CallbackQuery):
    current_product = db.cursor.execute("SELECT * FROM product WHERE id = ?", (db.current_product_id,)).fetchone()

    if current_product:
        await bot.send_photo(call.message.chat.id,
                             f"{current_product[4]}",
                             f"<b>{current_product[1]}</b>\n\n"
                             f"<i>{current_product[2]}</i>\n\n"
                             f"<b>Стоимость</b>: {current_product[3]} рублей.\n"
                             f"<b>Доступные размеры</b>: {current_product[5]}\n"
                             f"<b>Цвет</b>: {current_product[6]}\n\n"
                             f"<i>Если у вас остались вопросы, обращайтесь в WhatsApp</i>:\n"
                             f"+7 918 769 02 10; +7 918 872 18 36\n\n"
                             f"<i>ID товара</i>: {current_product[0]}",
                             parse_mode='html', reply_markup=kb.order_keyboard)
    else:
        await call.bot.answer_callback_query(callback_query_id=call.id, text='Список товаров пуст.')


@dp.callback_query_handler(lambda call: call.data == 'next_order_keyboard')
async def next_order_keyboard(call: types.CallbackQuery):
    db.current_product_id += 1
    current_product = db.cursor.execute("SELECT * FROM product WHERE id = ?", (db.current_product_id,)).fetchone()

    if current_product:
        await bot.edit_message_media(chat_id=call.message.chat.id,
                                     message_id=call.message.message_id,
                                     media=types.InputMediaPhoto(media=current_product[4]))

        await bot.edit_message_caption(chat_id=call.message.chat.id,
                                       message_id=call.message.message_id,
                                       caption=f"<b>{current_product[1]}</b>\n\n"
                                               f"<i>{current_product[2]}</i>\n\n"
                                               f"<b>Стоимость</b>: {current_product[3]} рублей.\n"
                                               f"<b>Доступные размеры</b>: {current_product[5]}\n"
                                               f"<b>Цвет</b>: {current_product[6]}\n\n"
                                               f"<i>Если у вас есть вопросы по товару, обращайтесь в WhatsApp</i>:\n"
                                               f"+7 918 769 02 10; +7 918 872 18 36\n"
                                               f"<i>ID товара</i>: {current_product[0]}",
                                       parse_mode='html',
                                       reply_markup=kb.order_keyboard)
    else:
        await bot.answer_callback_query(callback_query_id=call.id, text="Вы посмотрели все товары.")
        db.current_product_id -= 1


@dp.callback_query_handler(lambda call: call.data == "back_order_keyboard")
async def back_order_keyboard(call: types.CallbackQuery):
    db.current_product_id -= 1
    current_product = db.cursor.execute("SELECT * FROM product WHERE id = ?", (db.current_product_id,)).fetchone()

    if current_product:
        await bot.edit_message_media(chat_id=call.message.chat.id,
                                     message_id=call.message.message_id,
                                     media=types.InputMediaPhoto(media=current_product[4]))

        await bot.edit_message_caption(chat_id=call.message.chat.id,
                                       message_id=call.message.message_id,
                                       caption=f"<b>{current_product[1]}</b>\n\n"
                                               f"<i>{current_product[2]}</i>\n\n"
                                               f"<b>Стоимость</b>: {current_product[3]} рублей.\n"
                                               f"<b>Доступные размеры</b>: {current_product[5]}\n"
                                               f"<b>Цвет</b>: {current_product[6]}\n\n"
                                               f"<i>Если у вас есть вопросы по товару, обращайтесь в WhatsApp</i>:\n"
                                               f"+7 918 769 02 10; +7 918 872 18 36\n\n"
                                               f"<i>ID товара</i>: {current_product[0]}",
                                       parse_mode='html',
                                       reply_markup=kb.order_keyboard)
    else:
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        db.current_product_id = 1


# Покупка товара.
@dp.callback_query_handler(lambda call: call.data == "buy_order_keyboard")
async def buy_order_keyboard(call: types.CallbackQuery):
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)

    # Информация об ID товара
    product_id = db.current_product_id

    # Информация из БД
    product = db.cursor.execute("SELECT * FROM product WHERE id = ?", (product_id,)).fetchone()

    await bot.send_message(call.message.chat.id,
                           "<b>Проверьте информацию о  выбранном товаре, "
                           "после чего переходите к оформлению.</b>\n\n"
                           f"<b>ID товара</b>: <i>{product_id}</i>\n"
                           f"<b>Название</b>: <i>{product[1]}</i>\n"
                           f"<b>Стоимость</b>: <i>{product[3]}</i>\n"
                           f"<b>Цвет</b>: <i>{product[6]}</i>\n"
                           f"<b>Размеры</b>: <i>{product[5]}</i>",
                           parse_mode='html',
                           reply_markup=kb.next_order_keyboard)


@dp.callback_query_handler(lambda call: call.data == 'next_buy_product')
async def next_buy_product(call: CallbackQuery):
    await Order.name.set()
    await bot.send_message(chat_id=call.message.chat.id,
                           text="Укажите ваше имя.")


@dp.message_handler(state=Order.name)
async def user_add_name(message: types.Message, state: FSMContext):
    async with state.proxy() as info:
        info['name'] = message.text
        info['id'] = message.from_user.id
        info['tg_name'] = message.from_user.username
    await bot.send_message(chat_id=message.chat.id,
                           text="Укажите ваш город.")
    await Order.next()


@dp.message_handler(state=Order.city)
async def user_add_city(message: types.Message, state: FSMContext):
    async with state.proxy() as info:
        info['city'] = message.text
    await bot.send_message(chat_id=message.chat.id,
                           text="Укажите цвет кроссовок.")
    await Order.next()


@dp.message_handler(state=Order.color)
async def user_add_color(message: types.Message, state: FSMContext):
    async with state.proxy() as info:
        info['color'] = message.text
    await bot.send_message(chat_id=message.chat.id,
                           text="Укажите размер кроссовок.")
    await Order.next()


@dp.message_handler(state=Order.size)
async def user_add_size(message: types.Message, state: FSMContext):
    async with state.proxy() as info:
        info['size'] = message.text
    await bot.send_message(chat_id=message.chat.id,
                           text="Укажите тип доставки - Курьер/Почта/СДЭК/Автобусы")
    await Order.next()


@dp.message_handler(state=Order.delivery)
async def user_add_delivery(message: types.Message, state: FSMContext):
    async with state.proxy() as info:
        info['delivery'] = message.text
    await bot.send_message(chat_id=message.chat.id,
                           text="Заказ успешно оформлен, в скором времени с вами свяжется продавец для уточнения "
                                "деталей доставки.",
                           reply_markup=kb.back_keyboard)
    await db.user_order(state)
    await state.finish()
    back()


# Удаление информации о заказе.
@dp.message_handler(commands=['delete_order'])
async def user_delete_order(message: types.Message):
    user_id_in_database = []
    user_id_in_information = db.cursor.execute("SELECT USER_ID FROM information").fetchall()

    for user_id in user_id_in_information:
        user_id_in_database.append(user_id[0])

    print(user_id_in_database)

    message_split = message.text.split()

    if len(message_split) < 2:
        await message.answer("Ошибка использования команды.")
        return

    try:
        user_information = int(message_split[1])
        if user_information not in user_id_in_database:
            await message.answer(f"Заказа с ID {user_information} нет в БД.")
        else:
            await message.answer(f"Заказ с ID {user_information} был удалён из БД")
            db.cursor.execute("DELETE FROM information WHERE USER_ID = ?", (user_information,))
            db.conn.commit()

    except ValueError:
        await message.answer(f"ID должен состоять из цифр.")


# Информация о заказах
@dp.callback_query_handler(lambda call: call.data == 'all_order')
async def all_order(call: CallbackQuery):
    order = db.cursor.execute("SELECT * FROM information WHERE USER = ?", (db.current_user,)).fetchone()

    if order:
        await bot.send_message(call.message.chat.id,
                               f"<b>Информация о заказах</b>\n\n"
                               f"<b>ID заказа</b> - {order[7]}\n"
                               f"<b>Имя</b> - {order[1]}\n"
                               f"<b>Город</b> - {order[2]}\n"
                               f"<b>ID товара</b> - {order[3]}\n"
                               f"<b>Тип доставки</b> - {order[4]}\n"
                               f"<b>Размер</b> - {order[5]}\n"
                               f"<b>Цвет</b> - {order[6]}\n"
                               f"<b>Телеграм</b> - @{order[8]}\n\n"
                               f"<i>Если пользователь существует в БД - значит вы должны написать ему "
                               f"и уточнить детали заказа, подробный адрес и т.п. Когда сделка успешно завершена - "
                               f"удаляете пользователя из базы данных</i>.",
                               parse_mode='html', reply_markup=kb.back_order_keyboard)
    else:
        await call.bot.answer_callback_query(callback_query_id=call.id, text="На данный момент заказов нет.")


@dp.callback_query_handler(lambda call: call.data == 'user_info_order_next')
async def user_info_order_next(call: CallbackQuery):
    db.current_user += 1

    order = db.cursor.execute("SELECT * FROM information WHERE USER = ?", (db.current_user,)).fetchone()

    if order:
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=f"<b>Информация о заказах</b>\n\n"
                                         f"<b>ID заказа</b> - {order[7]}\n"
                                         f"<b>Имя</b> - {order[1]}\n"
                                         f"<b>Город</b> - {order[2]}\n"
                                         f"<b>ID товара</b> - {order[3]}\n"
                                         f"<b>Тип доставки</b> - {order[4]}\n"
                                         f"<b>Размер</b> - {order[5]}\n"
                                         f"<b>Цвет</b> - {order[6]}\n"
                                         f"<b>Телеграм</b> - @{order[8]}\n\n"
                                         f"<i>Если пользователь существует в БД - значит вы должны написать ему "
                                         f"и уточнить детали заказа, подробный адрес и т.п. Когда сделка успешно "
                                         f"завершена - "
                                         f"удаляете пользователя из базы данных</i>.",
                                    parse_mode='html', reply_markup=kb.back_order_keyboard)
    else:
        db.current_user = 1
        await call.bot.answer_callback_query(callback_query_id=call.id, text="Больше заказов нет.")


@dp.callback_query_handler(lambda call: call.data == 'user_info_order_back')
async def user_info_order_back(call: CallbackQuery):
    db.current_user -= 1
    order = db.cursor.execute("SELECT * FROM information WHERE USER = ?", (db.current_user,)).fetchone()

    if order:
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=f"<b>Информация о заказах</b>\n\n"
                                         f"<b>ID заказа</b> - {order[7]}\n"
                                         f"<b>Имя</b> - {order[1]}\n"
                                         f"<b>Город</b> - {order[2]}\n"
                                         f"<b>ID товара</b> - {order[3]}\n"
                                         f"<b>Тип доставки</b> - {order[4]}\n"
                                         f"<b>Размер</b> - {order[5]}\n"
                                         f"<b>Цвет</b> - {order[6]}\n"
                                         f"<b>Телеграм</b> - @{order[8]}\n\n"
                                         f"<i>Если пользователь существует в БД - значит вы должны написать ему "
                                         f"и уточнить детали заказа, подробный адрес и т.п. Когда сделка успешно "
                                         f"завершена - "
                                         f"удаляете пользователя из базы данных</i>.",
                                    parse_mode='html', reply_markup=kb.back_order_keyboard)
    else:
        db.current_user = 1
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
