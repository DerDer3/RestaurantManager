import mysql.connector
import os
from dotenv import load_dotenv
from faker import Faker
from faker_provider import RestaurantProvider


load_dotenv()
fake = Faker()
fake.faker_provider(RestaurantProvider)

conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)
cursor = conn.cursor()

reset = [
    "SET FOREIGN_KEY_CHECKS = 0;",
    "TRUNCATE TABLE Creates;",
    "TRUNCATE TABLE Serves;",
    "TRUNCATE TABLE WorksAt;",
    "TRUNCATE TABLE Dish;",
    "TRUNCATE TABLE Chef;",
    "TRUNCATE TABLE Restaurant;",
    "SET FOREIGN_KEY_CHECKS = 1;",
]

for resets in reset:
    cursor.execute(resets)


CHEF_RANGE = 80
RESTAURANT_RANGE = 30
DISH_RANGE = 120

restaurants = [fake.restaurant() for _ in range(RESTAURANT_RANGE)]
cursor.executemany(
    "INSERT IGNORE INTO Restaurant (name, location, michelin_stars, is_q1) VALUES (%s, %s, %s, %s)",
    restaurants
)

chefs = [fake.chef for _ in range(CHEF_RANGE)]
cursor.executemany(
    "INSERT IGNORE INTO Chef (name, bio, exp, specialty) VALUES (%s, %s, %s, %s)",
    chefs
)

dishes = [fake.dish() for _ in range(DISH_RANGE)]
cursor.executemany(
    "INSERT IGNORE INTO Dish (name, price, avg_rating, calorie_count) VALUES (%s, %s, %s, %s)",
    dishes
)

serves = [fake.serves(random.randint(1,RESTAURANT_RANGE),  random.randint(1,DISH_RANGE))  for _ in range(300)]
cursor.executemany(
    "INSERT IGNORE INTO Serves (restaurant_id, dish_id) VALUES (%s, %s)",
    serves
)

works = [fake.works_at(random.randint(1,CHEF_RANGE), random.randint(1,RESTAURANT_RANGE)) for _ in range(200)]
cursor.executemany(
    "INSERT IGNORE INTO WorksAt (restaurant_id, chef_id) VALUES (%s, %s)",
    works
)

creates_rows  = [fake.creates(random.randint(1,CHEF_RANGE), random.randint(1,DISH_RANGE))  for _ in range(250)]

conn.commit()
conn.close()
print("Seeded.")
