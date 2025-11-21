import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import random

cred = credentials.Certificate('config/projectKey.json')
firebase_admin.initialize_app(cred)

db = firestore.client()


recipe_titles = [
    "Paneer Butter Masala", "Mutton Gravy", "Vegetable Biryani", "Egg Curry",
    "Fish Fry", "Dal Tadka", "Aloo Paratha", "Prawn Masala", "Veg Pulao",
    "Chicken Biryani", "Masala Dosa", "Chole Bhature", "Rajma Chawal",
    "Kadai Paneer", "Tandoori Chicken", "Bhindi Masala", "Egg Fried Rice",
    "Sambar", "Chicken Korma", "Lemon Rice"
]

ingredient_pool = [
    "Onion", "Tomato", "Ginger", "Garlic", "Green Chili", "Oil",
    "Cumin Seeds", "Garam Masala", "Turmeric", "Salt", "Red Chili Powder",
    "Coriander Powder", "Water", "Butter", "Coriander Leaves",
    "Chicken", "Paneer", "Mutton", "Rice", "Eggs", "Curd"
]

units = ["grams", "tsp", "tbsp", "cups", "ml", "pieces"]

difficulty_levels = ["Easy", "Medium", "Hard"]

interaction_types = ["view", "rating", "like", "cooknote"]

sample_users = [
    {"userID": "user_001", "username": "chefA"},
    {"userID": "user_002", "username": "chefB"},
    {"userID": "user_003", "username": "foodlover"},
    {"userID": "user_004", "username": "kitchenKing"},
    {"userID": "user_005", "username": "masterChef"}
]


def generate_ingredients():
    ingredients = []
    for _ in range(random.randint(5, 10)):
        item = random.choice(ingredient_pool)
        ingredients.append({
            "Name": item,
            "Quantity": random.randint(1, 500),
            "Unit": random.choice(units),
            "Optional": random.choice([True, False])
        })
    return ingredients

def generate_steps():
    steps = []
    for i in range(1, random.randint(6, 15)):
        steps.append({
            "StepNumber": i,
            "Instruction": f"Follow step {i} carefully.",
            "Duration": f"{random.randint(1, 15)} min"
        })
    return steps

def generate_interaction(recipe_id, recipe_title):
    user = random.choice(sample_users)

    interaction_ref = db.collection("Interaction").document()

    interaction_ref.set({
        "RecipeId": recipe_id,
        "UserId": user["userID"],
        "Type": random.choice(interaction_types),
        "Rating": str(random.randint(1, 5)),
        "Cooknote": "Amazing taste!" if random.random() > 0.4 else "",
        "Username": user["username"],
        "RecipeTitle": recipe_title,
        "CreatedAt": datetime.now()
    })

    print("   → Interaction added:", interaction_ref.id)


for i in range(20):

    title = random.choice(recipe_titles)
    author = random.choice(sample_users)

    recipe_ref = db.collection("Recipe").document()

    recipe_ref.set({
        "Title": title,
        "Description": f"A delicious recipe for {title}.",
        "Ingredients": generate_ingredients(),
        "Steps": generate_steps(),
        "TimeRequired": {
            "PrepTime": random.randint(10, 25),
            "CookTime": random.randint(20, 50),
            "TotalTime": random.randint(40, 80)
        },
        "Difficulty": random.choice(difficulty_levels),
        "Statistics": {
            "ViewCount": random.randint(5, 200),
            "LikeCount": random.randint(0, 80),
            "RatingCount": random.randint(0, 50)
        },
        "CreatedAt": datetime.now(),
        "AuthorID": author["userID"],
        "AuthorName": author["username"]
    })

    print(f"✔ Recipe {i+1} created: {title}")

    for _ in range(random.randint(1, 3)):
        generate_interaction(recipe_ref.id, title)
