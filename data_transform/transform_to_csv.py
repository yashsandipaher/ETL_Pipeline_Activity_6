import json
import csv
import uuid
import re
from datetime import datetime

def parse_duration_to_seconds(d):
    if not d: return None
    d = str(d).strip().lower()
    if d.isdigit():
        return int(d)
    m = re.match(r'(?P<num>\d+)\s*(?P<unit>hr|hrs|hour|hours|min|minute|minutes|sec|second|seconds)?', d)
    if not m:
        return None
    num = int(m.group('num'))
    unit = m.group('unit') or "min"

# used to convert duration
    if unit.startswith("hr"):
        return num * 3600
    if unit.startswith("min"):
        return num * 60
    if unit.startswith("sec"):
        return num
    return None

def safe_get(d, key, default=None):
    return d.get(key, default) if isinstance(d, dict) else default

def transform(recipes_json="data_export/recipes.json"):    

# used to load the json
    with open(recipes_json, 'r', encoding='utf-8') as f:
        recipes = json.load(f)

    r_fp = open("data_transform/recipe.csv", "w", newline="", encoding="utf-8")
    i_fp = open("data_transform/ingredients.csv", "w", newline="", encoding="utf-8")
    s_fp = open("data_transform/steps.csv", "w", newline="", encoding="utf-8")
    inter_fp = open("data_transform/interactions.csv", "w", newline="", encoding="utf-8")

# used to write the csv files
    r_writer = csv.writer(r_fp); i_writer = csv.writer(i_fp)
    s_writer = csv.writer(s_fp); inter_writer = csv.writer(inter_fp)

    r_writer.writerow(["recipe_id","title","description","prep_time","cook_time","total_time","difficulty","author_id","author_name","created_at"])
    i_writer.writerow(["ingredient_id","recipe_id","name","quantity","unit","optional"])
    s_writer.writerow(["step_id","recipe_id","step_number","instruction","duration_seconds","duration_raw"])
    inter_writer.writerow(["interaction_id","recipe_id","user_id","username","type","rating","cooknote","created_at"])

# used to extract recipe.csv 
    for r in recipes:
        rid = r.get("id") or str(uuid.uuid4())
        title = r.get("Title")
        desc = r.get("Description")
        tr = r.get("TimeRequired") or {}
        prep = tr.get("PrepTime")
        cook = tr.get("CookTime")
        total = tr.get("TotalTime")
        difficulty = r.get("Difficulty")
        author_id = r.get("AuthorID") or None
        author_name = r.get("AuthorName") or None
        created_at = r.get("CreatedAt")

        r_writer.writerow([rid, title, desc, prep, cook, total, difficulty, author_id, author_name, created_at])

        for ing in r.get("Ingredients", []) or []:
            iid = ing.get("id") or str(uuid.uuid4())
            name = ing.get("name")
            qty = ing.get("Quantity")
            unit = ing.get("Unit")
            optional = ing.get("Optional", False)
            i_writer.writerow([iid, rid, name, qty, unit, optional])

        for s in r.get("Steps", []) or []:
            sid = s.get("id") or str(uuid.uuid4())
            step_no = s.get("StepNumber")
            instr = s.get("Instruction")
            dur_raw = s.get("Duration")
            dur_secs = parse_duration_to_seconds(dur_raw)
            s_writer.writerow([sid, rid, step_no, instr, dur_secs, dur_raw])

        for inter in r.get("Interaction", []) or []:
            iid = inter.get("id") or str(uuid.uuid4())
            user_id = inter.get("userID")
            username = inter.get("username")
            itype = inter.get("type")
            rating = None
            try:
                rating = float(inter.get("rating")) if inter.get("rating") not in (None,"") else None
            except:
                rating = None
            cooknote = inter.get("cooknote")
            created = inter.get("createdAt")
            inter_writer.writerow([iid, rid, user_id, username, itype, rating, cooknote, created])

    r_fp.close(); i_fp.close(); s_fp.close(); inter_fp.close()
    print("Transform complete. CSVs in data_transform/")
    
if __name__ == "__main__":
    transform()
