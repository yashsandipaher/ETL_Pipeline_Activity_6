import json
from datetime import datetime
from google.cloud.firestore_v1 import DocumentSnapshot
import firebase_admin
from firebase_admin import credentials, firestore
import os


def get_db():
    if not firebase_admin._apps:
        cred_path = os.path.join("config", "projectKey.json")
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
    return firestore.client()


# convert documentsnapshot into json
def doc_to_json(doc: DocumentSnapshot):
    data = doc.to_dict() or {}
    data["id"] = doc.id
    for k, v in list(data.items()):
        if hasattr(v, "isoformat"):
            data[k] = v.isoformat()

    return data


# export the recipe schema
def export_recipes(output_path="data_extract/recipes.json"):
    db = get_db()
    recipes = []

    for doc in db.collection("Recipe").stream():
        recipe = doc_to_json(doc)
        recipes.append(recipe)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:     # write data into json file
        json.dump(recipes, f, indent=2, ensure_ascii=False)

    print("Exported recipes:", len(recipes))


# export interaction schema
def export_interactions(output_path="data_extract/interactions.json"):
    db = get_db()
    interactions = []

    for doc in db.collection("Interaction").stream():
        interactions.append(doc_to_json(doc))

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(interactions, f, indent=2, ensure_ascii=False)

    print("Exported interactions:", len(interactions))


# export users schema
def export_users(output_path="data_extract/users.json"):
    db = get_db()
    users = []

    for user_doc in db.collection("Users").stream():
        u = doc_to_json(user_doc)
        activities = []
        for act in user_doc.reference.collection("Activities").stream():
            activities.append(doc_to_json(act))

        u["Activities"] = activities
        users.append(u)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2, ensure_ascii=False)

    print("Exported users:", len(users))

if __name__ == "__main__":
    export_recipes()
    export_interactions()
    export_users()
