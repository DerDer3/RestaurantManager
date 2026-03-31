import mysql.connector

# Connect without specifying a database first
conn = mysql.connector.connect(
    host="localhost",
    user="derek",
    password="password",
)
cursor = conn.cursor()

# Create and select the database
cursor.execute("CREATE DATABASE IF NOT EXISTS fooddb")
cursor.execute("USE fooddb")

tables = [
    """
    CREATE TABLE IF NOT EXISTS Chef (
        id        INT AUTO_INCREMENT PRIMARY KEY,
        name      VARCHAR(100)
        bio       TEXT,
        exp       INT,
        specialty VARCHAR(100)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS Restaurant (
        id             INT AUTO_INCREMENT PRIMARY KEY,
        name           VARCHAR(100)
        location       VARCHAR(255),
        michelin_stars INT     DEFAULT 0,
        is_q1          BOOLEAN DEFAULT FALSE
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS Dish (
        id            INT AUTO_INCREMENT PRIMARY KEY,
        name          VARCHAR(100)
        price         DECIMAL(6,2),
        avg_rating    DECIMAL(3,2),
        calorie_count INT
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
]

for table in tables:
    cursor.execute(table)
    
conn.commit()
conn.close()
print("Done.")
