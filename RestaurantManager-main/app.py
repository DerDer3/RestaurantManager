from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from db import get_db, close_db

import bcrypt

app = Flask(__name__)
app.secret_key = "password"
app.teardown_appcontext(close_db)

@app.route("/")
def index():
    query = request.args.get("q", "")
    search = request.args.get("search_by", "")
    min_rating = request.args.get("min_rating")
    price = request.args.get("price")
    course = request.args.get("course")
    region = request.args.get("region")
    open_now = request.args.get("open_now") == "true"
    res_michelin = request.args.get("res_michelin") == "true"
    chef_michelin = request.args.get("chef_michelin") == "true"
    seasonal = request.args.get("seasonal") == "true"
    has_delivery = request.args.get("has_delivery") == "true"
    opened_after = request.args.get("opened_after")
    active_since = request.args.get("active_since")
    established_after = request.args.get("established_after")
    radius = request.args.get("radius")
    min_experience = request.args.get("min_experience")
    max_price = request.args.get("max_price")

    # Multi-select (checkboxes) — use getlist
    cuisine = request.args.getlist("cuisine")
    dietary = request.args.getlist("dietary")
    specialty = request.args.getlist("specialty")
    results = []

    sql = ""
    conditions = []
    params = []

    print(search)
    print(query)

    if search:
        match search:
            case "location":
                print(f"Location query {query}")
                sql = """
                    SELECT DISTINCT r.name, r.id, r.address, r.city, r.state, r.price_range, r.rating, r.michelin_stars
                    FROM Restaurant r
                    """
                
                if query:
                    conditions.append("CONCAT(r.address, ', ', r.city, ' ', r.state) LIKE %s")
                    params.append(f"%{query}%")

            case "restaurants":
                print(f"Restaurant query {query}")
                sql = """
                    SELECT DISTINCT r.name, r.id, r.address, r.city, r.state, r.price_range, r.rating, r.michelin_stars
                    FROM Restaurant r
                    """

                if query:
                    conditions.append("r.name LIKE %s ") 
                    params.append(f"%{query}%",)


            case "chefs":
                print(f"Chef query {query}")
                sql = """
                    SELECT DISTINCT c.first_name, c.last_name, c.id, c.title, c.specialty
                    FROM Chef c
                    """
                    
                if query:
                    conditions.append("""CONCAT(c.first_name, ' ', c.last_name) 
                    LIKE %s """) 
                    params.append(f"%{query}%")

            case "dishes":
                print(f"Dish query {query}")
                sql = """
                    SELECT DISTINCT d.id, d.name, d.price, d.description
                    FROM Dish d
                    """

                if query:
                    conditions.append("d.name LIKE %s")
                    params.append(f"%{query}%")
            case _:
                pass

        if min_rating:
            conditions.append("r.rating >= %s")
            params.append(min_rating)
        if cuisine:
            placeholders = ", ".join(["%s"] * len(cuisine))
            conditions.append(f"r.cuisine_type IN ({placeholders})")
            params.extend(cuisine)
        if price:
            conditions.append("r.price_range = %s")
            params.append(price)
        if res_michelin:
            conditions.append("r.michelin_stars > 0")
        if specialty:
            placeholders = ", ".join(["%s"] * len(specialty))
            conditions.append(f"c.specialty IN ({placeholders})")
            params.extend(specialty)
        if min_experience:
            conditions.append("c.exp >= %s")
            params.append(min_experience)
        if chef_michelin:
            sql += """
            JOIN WorksAt wa ON c.id = wa.chef_id
            JOIN Restaurant r ON wa.restaurant_id = r.id
            """
            conditions.append("r.michelin_stars > 0")
        if dietary:
            placeholders = ", ".join(["%s"] * len(dietary))
            conditions.append(f"d.dietary_info IN ({placeholders})")
            params.extend(dietary)
        if course:
            conditions.append("d.course_type = %s")
            params.append(course)
        if max_price and max_price != '0':
            conditions.append("d.price <= %s")
            params.append(max_price)
        if seasonal:
            conditions.append("d.is_seasonal = 1")


        if conditions:
            sql += " WHERE " + " AND ".join(conditions)

        if sql:
            cursor = get_db().cursor(dictionary=True)
            print(sql)
            cursor.execute(sql, tuple(params))
            results = cursor.fetchall()

    return render_template("index.html", results=results, query=query, search_type=search)



@app.route("/api/entity/<string:entity_type>/<int:entity_id>")
def get_selection(entity_type, entity_id):
    print(entity_type)
    print(entity_id)

    info = None
    
    if entity_type:
        match entity_type:
            case "location":
                cursor = get_db().cursor(dictionary=True)
                cursor.execute("""
                    SELECT DISTINCT *
                    FROM Restaurant r
                    WHERE r.id = %s 
                """, (entity_id,))
                info = cursor.fetchall()
                entity_type = "restaurants"

            case "restaurants":
                cursor = get_db().cursor(dictionary=True)
                cursor.execute("""
                    SELECT DISTINCT *
                    FROM Restaurant r
                    WHERE r.id = %s 
                """, (entity_id,))
                info = cursor.fetchall()

            case "chefs":
                cursor = get_db().cursor(dictionary=True)
                cursor.execute("""
                    SELECT DISTINCT *
                    FROM Chef c
                    WHERE c.id = %s 
                """, (entity_id,))
                info = cursor.fetchall()

            case "dishes":
                cursor = get_db().cursor(dictionary=True)
                cursor.execute("""
                    SELECT DISTINCT *
                    FROM Dish d
                    WHERE d.id = %s 
                """, (entity_id,))
                info = cursor.fetchall()

    print(info)
    print(entity_type)
    return render_template("entity_detail.html", info=info, selection_type=entity_type)

@app.route("/api/entity_title/<string:entity_type>/<int:entity_id>")
def get_selection_title(entity_type, entity_id):
    print(entity_type)
    print(entity_id)

    info = None
    
    if entity_type:
        match entity_type:
            case "location":
                cursor = get_db().cursor(dictionary=True)
                cursor.execute("""
                    SELECT DISTINCT *
                    FROM Restaurant r
                    WHERE r.id = %s 
                """, (entity_id,))
                info = cursor.fetchall()
                entity_type = "restaurants"

            case "restaurants":
                cursor = get_db().cursor(dictionary=True)
                cursor.execute("""
                    SELECT DISTINCT *
                    FROM Restaurant r
                    WHERE r.id = %s 
                """, (entity_id,))
                info = cursor.fetchall()

            case "chefs":
                cursor = get_db().cursor(dictionary=True)
                cursor.execute("""
                    SELECT DISTINCT *
                    FROM Chef c
                    WHERE c.id = %s 
                """, (entity_id,))
                info = cursor.fetchall()

            case "dishes":
                cursor = get_db().cursor(dictionary=True)
                cursor.execute("""
                    SELECT DISTINCT *
                    FROM Dish d
                    WHERE d.id = %s 
                """, (entity_id,))
                info = cursor.fetchall()

    print(info)
    print(entity_type)
    return render_template("entity_title.html", info=info, selection_type=entity_type)

@app.route("/api/graph/<type>/<int:id>/<relationship>")
def get_graph(type, id, relationship):
    cursor = get_db().cursor(dictionary=True)
    elements = []

    if type == "chefs" and relationship == "restaurants":
        # get center node first
        cursor.execute("SELECT first_name, last_name FROM Chef WHERE id = %s", (id,))
        center = cursor.fetchone()
        elements.append({"data": {"id": f"c{id}", "label": f"{center['first_name']} {center['last_name']}", "type": "center"}})

        # then get related nodes
        cursor.execute("""
            SELECT r.id, r.name FROM Restaurant r
            JOIN WorksAt wa ON r.id = wa.restaurant_id
            WHERE wa.chef_id = %s
        """, (id,))
        for row in cursor.fetchall():
            elements.append({"data": {"id": f"r{row['id']}", "label": row["name"]}})
            elements.append({"data": {"source": f"c{id}", "target": f"r{row['id']}", "label": "works at"}})

    if type == "restaurants" and relationship == "chefs":
        # get center node first
        cursor.execute("SELECT name FROM Restaurant WHERE id = %s", (id,))
        center = cursor.fetchone()
        elements.append({"data": {"id": f"c{id}", "label": f"{center['name']}", "type": "center"}})

        # then get related nodes
        cursor.execute("""
            SELECT c.id, c.first_name, c.last_name FROM Chef c
            JOIN WorksAt wa ON c.id = wa.chef_id
            WHERE wa.restaurant_id = %s
        """, (id,))
        for row in cursor.fetchall():
            elements.append({"data": {"id": f"r{row['id']}", "label": f"{row['first_name']} {row['last_name']}"}})
            elements.append({"data": {"source": f"c{id}", "target": f"r{row['id']}", "label": "works at"}})
        # add other type/relationship combos here

    return jsonify({"elements": elements})

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
