from flask import Blueprint, Flask, render_template, request, redirect, url_for, flash, jsonify, session
from db import get_db, close_db

user_page_bp = Blueprint('user_page', __name__)

@user_page_bp.route('/user_page')
def user_page():

    user_id = session["user_id"]
    print(user_id)

    cursor = get_db().cursor(dictionary=True)
    cursor.execute("""
        SELECT r.* FROM Restaurant r
        JOIN FavoriteRestaurant fr ON r.id = fr.restaurant_id
        WHERE fr.user_id = %s    """, (user_id,))
    restaurants = cursor.fetchall()

    cursor.execute("""
        SELECT c.* FROM Chef c
        JOIN FavoriteChef fc ON c.id = fc.chef_id
        WHERE fc.user_id = %s    """, (user_id,))
    chefs = cursor.fetchall()

    cursor.execute("""
        SELECT d.* FROM Dish d
        JOIN FavoriteDish fd ON d.id = fd.dish_id
        WHERE fd.user_id = %s    """, (user_id,))
    dishes = cursor.fetchall()


    return render_template("user_page.html", dishes=dishes, restaurants=restaurants, chefs=chefs)
