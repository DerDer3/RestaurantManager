import mysql.connector

import os
from dotenv import load_dotenv

load_dotenv()

conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
)
cursor = conn.cursor()

# Create and select the database
cursor.execute(f"CREATE DATABASE IF NOT EXISTS {os.getenv("DB_NAME")}")
cursor.execute(f"USE {os.getenv("DB_NAME")}")

tables = [
    """
    CREATE TABLE IF NOT EXISTS Chef (
        id          INT AUTO_INCREMENT PRIMARY KEY,
        first_name  VARCHAR(100),
        last_name   VARCHAR(100),
        specialty   VARCHAR(100),
        title       VARCHAR(100),
        bio         TEXT,
        exp         INT
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS Restaurant (
        id              INT AUTO_INCREMENT PRIMARY KEY,
        `name`          VARCHAR(100),
        cuisine_type    VARCHAR(100),
        address         VARCHAR(255),
        city            VARCHAR(100),
        state           VARCHAR(2),
        zip_code        VARCHAR(10),
        phone           VARCHAR(30),
        website         VARCHAR(100),
        price_range     VARCHAR(4),
        rating          DECIMAL(3,2),
        michelin_stars  INT     DEFAULT 0
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS Dish (
        id              INT AUTO_INCREMENT PRIMARY KEY,
        `name`          VARCHAR(100),
        description     TEXT,
        price           DECIMAL(6,2),
        course_type     VARCHAR(100),
        dietary_info    VARCHAR(100),
        calorie_count   INT,
        is_seasonal     BOOLEAN
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS WorksAt (
        chef_id       INT NOT NULL,
        restaurant_id INT NOT NULL,
        PRIMARY KEY (chef_id, restaurant_id),
        FOREIGN KEY (chef_id)       REFERENCES Chef(id),
        FOREIGN KEY (restaurant_id) REFERENCES Restaurant(id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS Creates (
        chef_id INT NOT NULL,
        dish_id INT NOT NULL,
        PRIMARY KEY (chef_id, dish_id),
        FOREIGN KEY (chef_id) REFERENCES Chef(id),
        FOREIGN KEY (dish_id) REFERENCES Dish(id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS Serves (
        restaurant_id INT NOT NULL,
        dish_id       INT NOT NULL,
        PRIMARY KEY (restaurant_id, dish_id),
        FOREIGN KEY (restaurant_id) REFERENCES Restaurant(id),
        FOREIGN KEY (dish_id)       REFERENCES Dish(id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS User (
        id          INT AUTO_INCREMENT PRIMARY KEY,
        username    VARCHAR(100) NOT NULL,
        email       VARCHAR(100) NOT NULL UNIQUE,
        password    VARCHAR(255) NOT NULL
    )
    """,
]

for table in tables:
    cursor.execute(table)
    
conn.commit()
conn.close()
print("Done.")
