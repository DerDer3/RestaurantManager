from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from db import get_db, close_db

import bcrypt

app = Flask(__name__)
app.secret_key = "password"
app.teardown_appcontext(close_db)

@app.route("/")
def index():
    query = request.args.get("q", "")
    min_rating = request.args.get("min_rating", 0, type=float)
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
            cursor.execute("""
                SELECT c.name, c.specialty, c.exp
                FROM Chef c
                JOIN WorksAt w ON c.id = w.chef_id
                WHERE w.restaurant_id = %s
            """, (restaurant["id"],))
            restaurant["chefs"] = cursor.fetchall()

            cursor.execute("""
                SELECT d.name, d.price, d.avg_rating, d.calorie_count
                FROM Dish d
                JOIN Serves s ON d.id = s.dish_id
                WHERE s.restaurant_id = %s
            """, (restaurant["id"],))
            restaurant["dishes"] = cursor.fetchall()

            results.append(restaurant)

    return render_template("index.html", results=results, query=query, min_rating=min_rating)

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        try:
            db= get_db()
            cursor = db.cursor()
            cursor.execute("INSERT INTO User (username, email, password) VALUES (%s, %s, %s)", 
                (username, email, hashed)
            )
            db.commit()
            flash("Account created! You can now login")
            return redirect(url_for("index"))
        except Exception as e:
            flash("Email already in use")
            return redirect(url_for("signup"))

    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email    = request.form["email"]
        password = request.form["password"]

        cursor = get_db().cursor(dictionary=True)
        cursor.execute("SELECT * FROM User WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user and bcrypt.checkpw(password.encode("utf-8"), user["password"].encode("utf-8")):
            session["user_id"]   = user["id"]
            session["user_name"] = user["username"]
            flash("Welcome back, " + user["username"] + "!")
            return redirect(url_for("index"))
        else:
            flash("Invalid email or password.")
            return redirect(url_for("login"))

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
