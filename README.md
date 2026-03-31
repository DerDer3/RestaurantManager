# RestaurantManager

## Setup

- Create a user within mySql with a password
- Within the RestaurantManager directory create a file called .env, this is ignored by the git push but should contain the following:
  DB_HOST=(likely "localhost")
  DB_USER=
  DB_PASSWORD=
  DB_NAME=

- You can then run setup_db.py and seed.py to create the database and populate it with fake entries
- The app can then be run with python app.py
- This references the templates directory for creating the webpage
