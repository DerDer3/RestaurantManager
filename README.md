# RestaurantManager
Full stack graph database system storing Chefs, Restaurants, and Databases along with all the relations between them displayed in graphs.

## Setup
1. Download and extract the zip
2. Create a new file in the root called **.env**, and put the following:
   ```
   DB_HOST=localhost
   DB_USER=guest
   DB_PASSWORD=password
   DB_NAME=RestaurantDB
   ```
4. Set up the database:
    ```
    python3 install -r requirements.txt
    python3 setup_db.py
    ```
5. Set up mysql:
    ```
    sudo install mysql
    sudo mysql
    GRANT ALL PRIVILEGES ON RestaurantDB. * TO 'guest'@'localhost';
    quit

    python3 seed.py
    ```
## Run
1. Start up the server:
    ```
    python3 app.py
    ```
2. Access the application
    Visit **http://127.0.0.1:5000** in your browser
