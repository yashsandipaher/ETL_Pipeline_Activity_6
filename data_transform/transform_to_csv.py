import json
import csv
import uuid
import re
import os
from datetime import datetime


def parse_duration_to_seconds(d):
    if not d:
        return None
    d = str(d).strip().lower()

    if d.isdigit():
        return int(d)

    m = re.match(r'(?P<num>\d+)\s*(?P<unit>hr|hrs|hour|hours|min|minutes|sec|second|seconds)?', d)  # regex expression for duration
    if not m:
        return None

    num = int(m.group("num"))
    unit = m.group("unit") or "min"

    if unit.startswith("hr"):
        return num * 3600
    if unit.startswith("min"):
        return num * 60
    if unit.startswith("sec"):
        return num
    return None



# transform the recipe, interaction json file
def transform(
    recipes_json="data_extract/recipes.json",
    interactions_json="data_extract/interactions.json"
):

    os.makedirs("data_transform", exist_ok=True)

    # Load recipes
    with open(recipes_json, "r", encoding="utf-8") as f:
        recipes = json.load(f)

    # Load interactions
    with open(interactions_json, "r", encoding="utf-8") as f:
        interactions = json.load(f)

    # Open CSV writers
    r_fp = open("data_transform/recipe.csv", "w", newline="", encoding="utf-8")
    i_fp = open("data_transform/ingredients.csv", "w", newline="", encoding="utf-8")
    s_fp = open("data_transform/steps.csv", "w", newline="", encoding="utf-8")
    inter_fp = open("data_transform/interactions.csv", "w", newline="", encoding="utf-8")

    r_writer = csv.writer(r_fp)
    i_writer = csv.writer(i_fp)
    s_writer = csv.writer(s_fp)
    inter_writer = csv.writer(inter_fp)

    # CSV headers
    r_writer.writerow([
        "recipe_id", "title", "description", "prep_time",
        "cook_time", "total_time", "difficulty",
        "author_id", "author_name", "view_count",
        "like_count", "rating_count", "created_at"
    ])

    i_writer.writerow([
        "ingredient_id", "recipe_id", "name", "quantity", "unit", "optional"
    ])

    s_writer.writerow([
        "step_id", "recipe_id", "step_number", "instruction",
        "duration_seconds", "duration_raw"
    ])

    inter_writer.writerow([
        "interaction_id", "recipe_id", "user_id",
        "username", "type", "rating", "cooknote",
        "recipe_title", "created_at"
    ])

    # process the recipe json
    for r in recipes:
        rid = r.get("id") or str(uuid.uuid4())

        title = r.get("Title")
        desc = r.get("Description")
        tr = r.get("TimeRequired", {})
        stats = r.get("Statistics", {})

        prep = tr.get("PrepTime")
        cook = tr.get("CookTime")
        total = tr.get("TotalTime")

        difficulty = r.get("Difficulty")
        author_id = r.get("AuthorID")
        author_name = r.get("AuthorName")

        view_count = stats.get("ViewCount", 0)
        like_count = stats.get("LikeCount", 0)
        rating_count = stats.get("RatingCount", 0)

        created_at = r.get("CreatedAt")

        # write data into recipe csv
        r_writer.writerow([
            rid, title, desc, prep, cook, total, difficulty,
            author_id, author_name, view_count, like_count,
            rating_count, created_at
        ])

        # process the ingredient json
        for ing in r.get("Ingredients", []):
            iid = str(uuid.uuid4())
            i_writer.writerow([
                iid, rid,
                ing.get("Name"),
                ing.get("Quantity"),
                ing.get("Unit"),
                ing.get("Optional", False)
            ])

        
        # process steps json
        for st in r.get("Steps", []):
            sid = str(uuid.uuid4())
            step_no = st.get("StepNumber")
            instr = st.get("Instruction")
            dur_raw = st.get("Duration")
            dur_sec = parse_duration_to_seconds(dur_raw)

            s_writer.writerow([
                sid, rid, step_no, instr, dur_sec, dur_raw
            ])

    # process interaction json
    for inter in interactions:
        inter_writer.writerow([
            inter.get("id") or str(uuid.uuid4()),
            inter.get("RecipeId"),
            inter.get("UserId"),
            inter.get("Username"),
            inter.get("Type"),
            inter.get("Rating"),
            inter.get("Cooknote"),
            inter.get("RecipeTitle"),
            inter.get("CreatedAt")
        ])

    r_fp.close()
    i_fp.close()
    s_fp.close()
    inter_fp.close()

    print("Transform complete! CSVs created inside data_transform/")


if __name__ == "__main__":
    transform()
