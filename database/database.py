import sqlite3 as sq

conn = sq.connect('product.db')
cursor = conn.cursor()


async def database_info():
    cursor.execute("CREATE TABLE IF NOT EXISTS product("
                   "id INTEGER PRIMARY KEY, "
                   "title TEXT, "
                   "description TEXT,  "
                   "price TEXT,"
                   "photo TEXT,"
                   "shoe_size TEXT,"
                   "color TEXT )")
    conn.commit()


async def information_user():
    cursor.execute("CREATE TABLE IF NOT EXISTS information("
                   "USER_ID INTEGER PRIMARY KEY,"
                   "USERNAME TEXT,"
                   "CITY TEXT,"
                   "ID_ORDER INTEGER,"
                   "DELIVERY TEXT,"
                   "SIZE INTEGER,"
                   "COLOR TEXT  )")
    conn.commit()


async def insert_product(state):
    async with state.proxy() as data:
        conn.execute("INSERT INTO product (title, description, price, photo, shoe_size, color) "
                     "VALUES (?, ?, ?, ?, ?, ?)",
                     (data['name'], data['description'], data['price'], data['photo'], data['size'],
                      data['color']))
        conn.commit()


async def user_order(state):
    async with state.proxy() as info:
        conn.execute("INSERT INTO information (USERNAME, CITY, DELIVERY, SIZE, COLOR, USER_ID, TGNAME) "
                     "VALUES (?, ?, ?, ?, ?, ?, ?)",
                     (info['name'], info['city'], info['delivery'],
                      info['size'], info['color'], info['id'], info['tg_name']))
        conn.commit()

current_product_id = 1
current_user = 1
