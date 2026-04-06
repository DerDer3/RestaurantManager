import random
from faker import Faker
from faker.providers import BaseProvider

fake = Faker()


class RestaurantProvider(BaseProvider):
    """
    Custom Faker provider for ChefGraph / RestaurantManager data.
    Covers: Chef, Restaurant, Dish, WorksAt, Creates, Serves, User tables.
    """

    # ------------------------------------------------------------------ #
    #  Chef
    # ------------------------------------------------------------------ #

    _SPECIALTIES = [
        "French Cuisine", "Italian Cuisine", "Japanese Cuisine",
        "Mexican Cuisine", "Indian Cuisine", "Mediterranean",
        "Pastry & Desserts", "BBQ & Grilling", "Seafood",
        "Vegan & Plant-Based", "Molecular Gastronomy", "Korean Fusion",
        "Middle Eastern", "American Comfort Food", "Thai Cuisine",
    ]

    _TITLES = ["Chef", "Executive Chef", "Head Chef", "Sous Chef", "Pastry Chef"]

    def chef_specialty(self) -> str:
        return self.random_element(self._SPECIALTIES)

    def chef_title(self) -> str:
        return self.random_element(self._TITLES)

    def chef_bio(self, name: str, specialty: str) -> str:
        years = random.randint(5, 30)
        school = self.random_element([
            "the Culinary Institute of America",
            "Le Cordon Bleu",
            "the Institute of Culinary Education",
            "Johnson & Wales University",
            "a family kitchen in rural Tuscany",
        ])
        return (
            f"{name} has spent {years} years mastering {specialty}, "
            f"having trained at {school}. Known for bold flavors and "
            f"meticulous technique."
        )

    def chef(self) -> dict:
        """Return a dict ready to INSERT into the Chef table."""
        first = fake.first_name()
        last = fake.last_name()
        specialty = self.chef_specialty()
        return {
            "first_name": first,
            "last_name": last,
            "specialty": specialty,
            "title": self.chef_title(),
            "bio": self.chef_bio(f"{first} {last}", specialty),
            "exp": random.randint(1, 35),
        }

    # ------------------------------------------------------------------ #
    #  Restaurant
    # ------------------------------------------------------------------ #

    _CUISINE_TYPES = [
        "French", "Italian", "Japanese", "Mexican", "Indian",
        "American", "Mediterranean", "Thai", "Korean", "Spanish",
        "Chinese", "Greek", "Ethiopian", "Brazilian", "Vietnamese",
    ]

    _RESTAURANT_ADJECTIVES = [
        "The Golden", "Le Petit", "Casa", "Blue", "Red Door",
        "The Rustic", "Urban", "Garden", "Harbor", "Ember",
        "Salt & Stone", "The Gilded", "Copper", "Ivory", "Noir",
    ]

    _RESTAURANT_NOUNS = [
        "Table", "Kitchen", "Bistro", "Brasserie", "Grill",
        "House", "Eatery", "Cantina", "Tavern", "Trattoria",
        "Bouchon", "Cellar", "Quarter", "Hearth", "Spoon",
    ]

    def restaurant_name(self) -> str:
        return f"{self.random_element(self._RESTAURANT_ADJECTIVES)} {self.random_element(self._RESTAURANT_NOUNS)}"

    def cuisine_type(self) -> str:
        return self.random_element(self._CUISINE_TYPES)

    def price_range(self) -> str:
        """Returns $, $$, $$$, or $$$$."""
        return self.random_element(["$", "$$", "$$$", "$$$$"])

    def michelin_stars(self) -> int:
        """Weighted — most restaurants have 0 stars."""
        return random.choices([0, 1, 2, 3], weights=[70, 18, 8, 4])[0]

    def restaurant_rating(self) -> float:
        """Rating between 2.5 and 5.0, rounded to 1 decimal."""
        return round(random.uniform(2.5, 5.0), 1)

    def restaurant(self) -> dict:
        """Return a dict ready to INSERT into the Restaurant table."""
        return {
            "name": self.restaurant_name(),
            "cuisine_type": self.cuisine_type(),
            "address": fake.street_address(),
            "city": fake.city(),
            "state": fake.state_abbr(),
            "zip_code": fake.zipcode(),
            "phone": fake.phone_number(),
            "email": fake.company_email(),
            "website": fake.url(),
            "price_range": self.price_range(),
            "rating": self.restaurant_rating(),
            "michelin_stars": self.michelin_stars(),
        }

    # ------------------------------------------------------------------ #
    #  Dish
    # ------------------------------------------------------------------ #

    _DISH_PREFIXES = [
        "Pan-Seared", "Slow-Braised", "Wood-Fired", "Crispy", "Smoked",
        "Charred", "Poached", "Glazed", "Roasted", "Grilled",
        "Chilled", "Caramelized", "Cured", "Whipped", "Deconstructed",
    ]

    _DISH_PROTEINS = [
        "Duck Breast", "Salmon Fillet", "Lamb Chop", "Beef Tenderloin",
        "Scallops", "Sea Bass", "Pork Belly", "Chicken Thigh",
        "Lobster", "Tofu", "Mushroom", "Cauliflower Steak",
    ]

    _DISH_GARNISHES = [
        "with Truffle Foam", "over Saffron Risotto", "with Miso Glaze",
        "atop Pea Purée", "with Chimichurri", "finished with Brown Butter",
        "with Pickled Shallots", "on a Bed of Lentils", "with Yuzu Emulsion",
        "alongside Roasted Root Vegetables",
    ]

    _COURSES = ["Appetizer", "Soup", "Salad", "Main Course", "Dessert", "Side"]

    _DIETARY_FLAGS = [
        "None", "Vegetarian", "Vegan", "Gluten-Free",
        "Nut-Free", "Dairy-Free", "Kosher", "Halal",
    ]

    def dish_name(self) -> str:
        return (
            f"{self.random_element(self._DISH_PREFIXES)} "
            f"{self.random_element(self._DISH_PROTEINS)} "
            f"{self.random_element(self._DISH_GARNISHES)}"
        )

    def dish_price(self) -> float:
        return round(random.uniform(8.0, 95.0), 2)

    def course_type(self) -> str:
        return self.random_element(self._COURSES)

    def dietary_info(self) -> str:
        return self.random_element(self._DIETARY_FLAGS)

    def dish(self) -> dict:
        """Return a dict ready to INSERT into the Dish table."""
        return {
            "name": self.dish_name(),
            "description": fake.sentence(nb_words=12),
            "price": self.dish_price(),
            "course_type": self.course_type(),
            "dietary_info": self.dietary_info(),
            "calories": random.randint(150, 1200),
            "is_seasonal": random.choice([True, False]),
        }

    # ------------------------------------------------------------------ #
    #  Relationship helpers (WorksAt / Creates / Serves)
    # ------------------------------------------------------------------ #

    def works_at(self, chef_id: int, restaurant_id: int) -> dict:
        """Return a dict for a WorksAt join-table row."""
        start_year = random.randint(2000, 2023)
        still_works = random.random() > 0.2
        return {
            "chef_id": chef_id,
            "restaurant_id": restaurant_id,
            "role": self.chef_title(),
            "start_year": start_year,
            "end_year": None if still_works else random.randint(start_year + 1, 2024),
            "is_current": still_works,
        }

    def creates(self, chef_id: int, dish_id: int) -> dict:
        """Return a dict for a Creates join-table row."""
        return {
            "chef_id": chef_id,
            "dish_id": dish_id,
            "year_created": random.randint(2000, 2024),
            "is_signature": random.random() > 0.7,
        }

    def serves(self, restaurant_id: int, dish_id: int) -> dict:
        """Return a dict for a Serves join-table row."""
        return {
            "restaurant_id": restaurant_id,
            "dish_id": dish_id,
            "is_available": random.random() > 0.1,
            "menu_section": self.course_type(),
        }

    # ------------------------------------------------------------------ #
    #  User
    # ------------------------------------------------------------------ #

    def user(self, hashed_password: str = None) -> dict:
        """
        Return a dict for the User table.
        Pass in a bcrypt-hashed password, or leave None to get a
        placeholder (swap before inserting into a real DB).
        """
        return {
            "username": fake.user_name(),
            "email": fake.email(),
            "password_hash": hashed_password or "<HASH_ME>",
            "display_name": fake.name(),
            "joined_at": fake.date_time_between(start_date="-5y", end_date="now"),
            "is_admin": random.random() > 0.95,
        }


# ------------------------------------------------------------------ #
#  Quick demo / sanity check
# ------------------------------------------------------------------ #
if __name__ == "__main__":
    fake.add_provider(RestaurantProvider)

    print("=== Chef ===")
    print(fake.chef())

    print("\n=== Restaurant ===")
    print(fake.restaurant())

    print("\n=== Dish ===")
    print(fake.dish())

    print("\n=== WorksAt (chef 1 → restaurant 3) ===")
    print(fake.works_at(1, 3))

    print("\n=== User ===")
    print(fake.user())
