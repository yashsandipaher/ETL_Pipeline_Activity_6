import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

cred = credentials.Certificate('config\projectKey.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

ingredients = [
    {"Name": "Chicken", "Quantity": 500, "Unit": "grams", "Optional": False},
    {"Name": "Turmeric Powder", "Quantity": 1, "Unit": "tsp", "Optional": False},
    {"Name": "Chicken Masala", "Quantity": 1, "Unit": "tbsp", "Optional": False},
    {"Name": "Ginger-Garlic Paste", "Quantity": 2, "Unit": "tsp", "Optional": False},
    {"Name": "Garam Masala", "Quantity": 1, "Unit": "tsp", "Optional": False},
    {"Name": "Jeera", "Quantity": 2, "Unit": "tsp", "Optional": False},
    {"Name": "Oil", "Quantity": 2, "Unit": "tbsp", "Optional": False},
    {"Name": "Salt", "Quantity": 2, "Unit": "tsp", "Optional": False},
    {"Name": "Water", "Quantity": 500, "Unit": "ml", "Optional": False},
    {"Name": "Coriander Leaves", "Quantity": 1, "Unit": "small handful", "Optional": True},
]

steps = [
    {"StepNumber": 1, "Instruction": "Turn on gas, put cooker on burner, heat for 20–30 sec", "Duration": "30 sec"},
    {"StepNumber": 2, "Instruction": "Wash chicken and put into bowl", "Duration": "5 min"},
    {"StepNumber": 3, "Instruction": "Add oil, turmeric, garam masala, jeera in cooker and stir", "Duration": "3 min"},
    {"StepNumber": 4, "Instruction": "Add 2 cups (≈200 ml) water and stir", "Duration": "1 min"},
    {"StepNumber": 5, "Instruction": "Add chicken, close lid of cooker", "Duration": "1 min"},
    {"StepNumber": 6, "Instruction": "Boil chicken for 10–15 min (2–3 whistles)", "Duration": "15 min"},
    {"StepNumber": 7, "Instruction": "Check if cooked, remove chicken and keep broth aside", "Duration": "5 min"},
    {"StepNumber": 8, "Instruction": "If not cooked, repeat boiling step", "Duration": "variable"},
    {"StepNumber": 9, "Instruction": "Heat pan with 2 tbsp oil", "Duration": "1 min"},
    {"StepNumber": 10, "Instruction": "Add ginger-garlic paste & chicken masala, stir", "Duration": "3 min"},
    {"StepNumber": 11, "Instruction": "Add boiled chicken into pan, stir", "Duration": "10 min"},
    {"StepNumber": 12, "Instruction": "Add broth and cook", "Duration": "7 min"},
    {"StepNumber": 13, "Instruction": "Add salt & chicken masala", "Duration": "1 min"},
    {"StepNumber": 14, "Instruction": "Cook for 20–30 min until gravy thickens", "Duration": "30 min"},
    {"StepNumber": 15, "Instruction": "Add coriander leaves for garnish", "Duration": "1 min"},
    {"StepNumber": 16, "Instruction": "Turn off gas. Chicken curry is ready", "Duration": "1 min"},
]


recipe_ref = db.collection("Recipe").document()

recipe_ref.set({
    "Title": "Chicken Curry",
    "Description": "Traditional homemade Indian chicken curry.",
    "AuthorID": "user_12345",
    "AuthorName": "yashaher",
    "Ingredients": ingredients,
    "Steps": steps,
    "TimeRequired": {
        "PrepTime": 15,
        "CookTime": 45,
        "TotalTime": 60
    },
    "Difficulty": "Medium",
    "Statistics": {
        "ViewCount": 0,
        "LikeCount": 0,
        "RatingCount": 0
    },
    "CreatedAt": datetime.now()
})

print("Chicken Curry Recipe Added. ID:", recipe_ref.id)

interaction_ref = db.collection("Interaction").document()

interaction_ref.set({
    "RecipeId": recipe_ref.id,
    "UserId": "user_12345",
    "Type": "rating",
    "Rating": "5",
    "Cooknote": "This recipe turned out amazing!",
    "Username": "yashaher",
    "RecipeTitle": "Chicken Curry",
    "CreatedAt": datetime.now()
})

print("Interaction added. Interaction ID:", interaction_ref.id)

user_ref = db.collection("Users").document()

user_data = {
    "UserID": user_ref.id,
    "UserName": "Sample User",
    "Email": "sampleUser@gmail.com",
    "MobileNumber": "1234567890",
    "JoinedAt": datetime.now(),
    "SkillLevel": "Expert"
}

user_ref.set(user_data)
print("User created with ID:", user_ref.id)

activity_ref = user_ref.collection("Activities").document()

activity_ref.set({
    "InteractionID": interaction_ref.id, 
    "RecipeName": "Chicken Curry",
    "Type": "rating",
    "CreatedAt": datetime.now()
})

print("Activity added for user:", user_ref.id)
