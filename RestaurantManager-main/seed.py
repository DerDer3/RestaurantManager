import mysql.connector

import Los
from dotenv import load_dotenv

conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)
cursor = conn.cursor()

restaurants = [
    ("The Gilded Fork", "New York, NY", 3, True),
    ("Maison Lumière", "Paris, France", 2, True),
    ("Sakura Zenith", "Tokyo, Japan", 3, False),
    ("Prairie Table", "Chicago, IL", 1, True),
    ("Coastal Ember", "Los Angeles, CA", 2, False),
]
cursor.executemany(
    "INSERT INTO Restaurant (name, location, michelin_stars, is_q1) VALUES (%s, %s, %s, %s)",
    restaurants
)

chefs = [
    ("Jean-Pierre Moreau", "Classically trained in Lyon, France.", 20, "French cuisine"),
    ("Hiro Tanaka", "Specializes in modern Japanese techniques.", 12, "Japanese cuisine"),
    ("Sara Collins", "Known for farm-to-table philosophy.", 8, "American cuisine"),
    ("Claire Dubois", "Pastry expert with a focus on desserts.", 10, "Pastry"),
    ("Marcus Yee", "Bold flavors inspired by Southeast Asia.", 15, "Fusion"),
]
cursor.executemany(
    "INSERT INTO Chef (name, bio, exp, specialty) VALUES (%s, %s, %s, %s)",
    chefs
)

dishes = [
    ("Duck Confit", 42.00, 4.8, 620),
    ("Truffle Risotto", 18.50, 4.5, 430),
    ("Wagyu Omakase", 95.00, 4.9, 810),
    ("Smoked Brisket", 12.00, 4.2, 310),
    ("Mango Tuna Tartare", 67.00, 4.7, 540),
    ("Lavender Crème Brûlée", 24.00, 4.3, 390),
    ("Black Truffle Ramen", 55.00, 4.6, 720),
]
cursor.executemany(
    "INSERT INTO Dish (name, price, avg_rating, calorie_count) VALUES (%s, %s, %s, %s)",
    dishes
)

conn.commit()
conn.close()
print("Seeded.")
