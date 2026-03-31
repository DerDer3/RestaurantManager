from flask import Flask, render_template, request, redirect
from db import get_db, close_db

app = Flask(__name__)
app.secret_key = "password"
app.teardown_appcontext(close_db)

@app.route("/")
def index():
    query = request.args.get("q", "")
    results = []

    if query:
        cursor = get_db().cursor(dictionary=True)
        cursor.execute("""
            SELECT DISTINCT r.id, r.name, r.location, r.michelin_stars, r.is_q1
            FROM Restaurant r
            WHERE r.location LIKE %s
        """, (f"%{query}%",))
        restaurants = cursor.fetchall()

        for restaurant in restaurants:
            # Get chefs at this restaurant
            cursor.execute("""
                SELECT c.specialty, c.exp
                FROM Chef c
                JOIN WorksAt w ON c.id = w.chef_id
                WHERE w.restaurant_id = %s
            """, (restaurant["id"],))
            restaurant["chefs"] = cursor.fetchall()

            # Get dishes served at this restaurant
            cursor.execute("""
                SELECT d.price, d.avg_rating, d.calorie_count
                FROM Dish d
                JOIN Serves s ON d.id = s.dish_id
                WHERE s.restaurant_id = %s
            """, (restaurant["id"],))
            restaurant["dishes"] = cursor.fetchall()

            results.append(restaurant)

    return render_template("index.html", results=results, query=query)

if __name__ == "__main__":
    app.run(debug=True)
