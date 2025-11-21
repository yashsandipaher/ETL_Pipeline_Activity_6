import json
from datetime import datetime
from google.cloud.firestore_v1 import DocumentSnapshot
import firebase_admin
from firebase_admin import credentials, firestore
import os


# used to get firestore database
def get_db():
    if not firebase_admin._apps:
        cred_path = os.path.join("config", "ProjectKey.json")
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
    return firestore.client()

# used to convert Firestore DocumentSnapshot to dictionary
def doc_to_json(doc: DocumentSnapshot):
    data = doc.to_dict() or {}
    data["id"] = doc.id 
    for k, v in list(data.items()):
        if hasattr(v, "isoformat"):
            data[k] = v.isoformat()
    return data


# used to convert both recipe and subcollection interaction
def export_recipes(output_path="data_export/recipes.json"):
    db = get_db()
    recipes = []
    for doc in db.collection("Recipe").stream():
        r = doc_to_json(doc)
        interactions = []
        for inter in doc.reference.collection("Interaction").stream():
            inter_data = doc_to_json(inter)
            interactions.append(inter_data)
        r["Interaction"] = interactions
        recipes.append(r)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(recipes, f, indent=2, ensure_ascii=False)
    print("Exported recipes:", len(recipes))


# used to export users collection
def export_users(output_path="data_export/users.json"):
    db = get_db()
    users = []
    for doc in db.collection("Users").stream():
        users.append(doc_to_json(doc))
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2, ensure_ascii=False)
    print("Exported users:", len(users))

if __name__ == "__main__":
    export_recipes()
    export_users()
