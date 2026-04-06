import mysql.connector
import os
import random
from dotenv import load_dotenv
from faker import Faker
from provider import RestaurantProvider


load_dotenv()
fake = Faker()
fake.add_provider(RestaurantProvider)

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
for r in restaurants:
    cursor.execute(
        """INSERT INTO Restaurant
        (name, cuisine_type, address, city, state, zip_code, phone, website, price_range, rating, michelin_stars)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
        (r["name"], r["cuisine_type"], r["address"], r["city"], r["state"],
         r["zip_code"], r["phone"], r["website"],
         r["price_range"], r["rating"], r["michelin_stars"])
    )

chefs = [fake.chef() for _ in range(CHEF_RANGE)]
for chef in chefs:
    cursor.execute(
    "INSERT IGNORE INTO Chef (first_name, last_name, specialty, title, bio, exp) VALUES (%s, %s, %s, %s, %s, %s)",
    (chef["first_name"], chef["last_name"], chef["specialty"], chef["title"], chef["bio"], chef["exp"])
    )

dishes = [fake.dish() for _ in range(DISH_RANGE)]
for d in dishes:
    cursor.execute(
        """INSERT INTO Dish
        (name, description, price, course_type, dietary_info, calorie_count, is_seasonal)
        VALUES (%s, %s, %s, %s, %s, %s, %s)""",
        (d["name"], d["description"], d["price"], d["course_type"],
         d["dietary_info"], d["calories"], d["is_seasonal"])
    )

serves = [(random.randint(1,RESTAURANT_RANGE), random.randint(1,DISH_RANGE)) for _ in range(300)]
cursor.executemany(
    "INSERT IGNORE INTO Serves (restaurant_id, dish_id) VALUES (%s, %s)",
    serves
)

works = [(random.randint(1,CHEF_RANGE), random.randint(1,RESTAURANT_RANGE)) for _ in range(200)]
cursor.executemany(
    "INSERT IGNORE INTO WorksAt (restaurant_id, chef_id) VALUES (%s, %s)",
    works
)

creates = [(random.randint(1,CHEF_RANGE), random.randint(1,DISH_RANGE)) for _ in range(250)]

conn.commit()
conn.close()
print("Seeded.")
