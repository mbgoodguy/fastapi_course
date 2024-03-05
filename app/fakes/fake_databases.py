import random
from string import ascii_letters, digits

import faker
from faker import Faker

fake = Faker('ru_RU')
ALPHABET = ascii_letters + digits


# def generate_fake_db(count_of_records):
#     fake_db = {}
#
#     for i in range(1, count_of_records):
#         # fake_db[i] = fake.name()
#         fake_user = {i: fake.name()}
#         fake_db.update(fake_user)
#
#     return fake_db


def generate_fake_users_db(count_of_records) -> list:
    fake_db = []

    for i in range(1, count_of_records):
        # fake_db[i] = fake.name()
        fake_user = {i: fake.name()}
        fake_db.append(fake_user)

    return fake_db


def generate_fake_products(count_of_products) -> list:
    fake_db = []
    categories = ['Smartphones', 'Notebooks', 'Accessories', 'Smartwatches', 'Headphones']
    brand = ['Xiaomi', 'Apple', 'Samsung', 'Lenovo', 'Razor']
    names = ['smartphone', 'notebook', 'accessory', 'watches', 'headphone']

    for i in range(1, count_of_products + 1):
        fake_product = {
            'product_id': i,
            'name': f"{random.choice(names)} {random.choice(brand)} {''.join(random.choice(ALPHABET) for i in range(5))}",
            'category': random.choice(categories),
            'price': round(random.uniform(300, 700), 2)
        }

        fake_db.append(fake_product)

    return fake_db
