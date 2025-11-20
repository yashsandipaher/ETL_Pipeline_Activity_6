import json, csv, re
from collections import defaultdict

VALID_DIFFICULTY = {"Easy","Medium","Hard"}

def is_positive_number(v):
    try:
        return float(v) > 0
    except:
        return False

def validate_recipes(csv_path="data_transform/recipe.csv", ingredients_path="data_transform/ingredients.csv", steps_path="data_transform/steps.csv", interactions_path="data_transform/interactions.csv"):
    recipes = {}
    
# used to load the data
    with open(csv_path, encoding='utf-8') as f:  
        r = csv.DictReader(f)
        for row in r:
            recipes[row['recipe_id']] = row

    ingredients = defaultdict(list)
    with open(ingredients_path, encoding='utf-8') as f:
        r = csv.DictReader(f)
        for row in r:
            ingredients[row['recipe_id']].append(row)

    steps = defaultdict(list)
    with open(steps_path, encoding='utf-8') as f:
        r = csv.DictReader(f)
        for row in r:
            steps[row['recipe_id']].append(row)

    interactions = defaultdict(list)
    with open(interactions_path, encoding='utf-8') as f:
        r = csv.DictReader(f)
        for row in r:
            interactions[row['recipe_id']].append(row)

    report = {"summary": {"total_recipes": len(recipes), "valid_recipes":0, "invalid_recipes":0},
              "invalid_records": [], "valid_records": []}

    for rid, rec in recipes.items():
        errors = []
        if not rec.get("title"):
            errors.append("Missing Title")
        try:
            prep = float(rec.get("prep_time")) if rec.get("prep_time") not in (None,"") else None
            cook = float(rec.get("cook_time")) if rec.get("cook_time") not in (None,"") else None
            total = float(rec.get("total_time")) if rec.get("total_time") not in (None,"") else None
        except:
            prep = prep if 'prep' in locals() else None
            cook = cook if 'cook' in locals() else None
            total = total if 'total' in locals() else None


# used to check the positive values of prep time,cook time and total time
        if prep is None or not (prep > 0):
            errors.append("PrepTime must be > 0")
        if cook is None or not (cook >= 0):
            errors.append("CookTime must be >= 0")
        if total is None:
            errors.append("TotalTime missing")
        else:
            if prep is not None and cook is not None:
                if total < (prep + cook) - 1e-6: 
                    errors.append("TotalTime less than PrepTime + CookTime")

# used to check the difficulty value of recipe
        if (rec.get("difficulty") or "").strip() not in VALID_DIFFICULTY:
            errors.append(f"Invalid difficulty: {rec.get('difficulty')}")

# used to chekc non empty array
        if len(ingredients.get(rid, [])) == 0:
            errors.append("No ingredients")
        else:
            for ing in ingredients[rid]:
                qty = ing.get("quantity")
                if qty and re.match(r'^\d+(\.\d+)?$', str(qty).strip()):
                    if float(qty) <= 0:
                        errors.append(f"Ingredient {ing.get('name')} has non-positive quantity")

        if len(steps.get(rid, [])) == 0:
            errors.append("No steps")

# used to check interaction ratings
        for inter in interactions.get(rid, []):
            rstr = inter.get("rating")
            if rstr:
                try:
                    rv = float(rstr)
                    if rv < 0 or rv > 5:
                        errors.append(f"Interaction rating {rstr} out of range (0-5)")
                except:
                    errors.append(f"Interaction rating {rstr} not numeric")

        if errors:
            report["invalid_records"].append({"recipe_id": rid, "errors": errors})
        else:
            report["valid_records"].append(rid)

    report["summary"]["valid_recipes"] = len(report["valid_records"])
    report["summary"]["invalid_recipes"] = len(report["invalid_records"])

    with open("data_validation/validation_report.json", "w", encoding='utf-8') as f:
        json.dump(report, f, indent=2)
    print("Validation done. Summary:", report["summary"])

if __name__ == "__main__":
    validate_recipes()
