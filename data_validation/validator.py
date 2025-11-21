import json, csv, re, os
from collections import defaultdict

VALID_DIFFICULTY = {"Easy", "Medium", "Hard"}

def is_positive_number(v):
    try:
        return float(v) > 0
    except:
        return False


def validate_recipes(
    csv_path="data_transform/recipe.csv",
    ingredients_path="data_transform/ingredients.csv",
    steps_path="data_transform/steps.csv",
    interactions_path="data_transform/interactions.csv"
):

    # Load recipes
    recipes = {}
    with open(csv_path, encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            recipes[row["recipe_id"]] = row

    # Load ingredients
    ingredients = defaultdict(list)
    with open(ingredients_path, encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            ingredients[row["recipe_id"]].append(row)

    # Load steps
    steps = defaultdict(list)
    with open(steps_path, encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            steps[row["recipe_id"]].append(row)

    # Load interactions
    interactions = defaultdict(list)
    with open(interactions_path, encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            interactions[row["recipe_id"]].append(row)

    # Final report structure
    report = {
        "summary": {
            "total_recipes": len(recipes),
            "valid_recipes": 0,
            "invalid_recipes": 0
        },
        "invalid_records": [],
        "valid_records": []
    }

    # Validate each recipe
    for rid, rec in recipes.items():
        errors = []

        # Required Title
        if not rec.get("title"):
            errors.append("Missing Title")

        # Time Validations
        try:
            prep = float(rec.get("prep_time")) if rec.get("prep_time") else None
            cook = float(rec.get("cook_time")) if rec.get("cook_time") else None
            total = float(rec.get("total_time")) if rec.get("total_time") else None
        except:
            prep, cook, total = None, None, None

        if prep is None or prep <= 0:
            errors.append("PrepTime must be > 0")

        if cook is None or cook < 0:
            errors.append("CookTime must be >= 0")

        if total is None:
            errors.append("TotalTime missing")
        else:
            if prep and cook:
                if total < prep + cook:
                    errors.append("TotalTime < PrepTime + CookTime")

        # Difficulty validation
        diff = (rec.get("difficulty") or "").strip()
        if diff not in VALID_DIFFICULTY:
            errors.append(f"Invalid Difficulty: {diff}")

        # Ingredients validation
        if len(ingredients[rid]) == 0:
            errors.append("No ingredients found")
        else:
            for ing in ingredients[rid]:
                qty = ing.get("quantity")
                if qty:
                    if not re.match(r"^\d+(\.\d+)?$", str(qty)):
                        errors.append(f"Ingredient quantity invalid: {qty}")
                    else:
                        if float(qty) <= 0:
                            errors.append(f"Ingredient quantity must be positive: {qty}")

        # Steps validation
        if len(steps[rid]) == 0:
            errors.append("No steps found")

        # Interactions validation
        for inter in interactions.get(rid, []):
            rstr = inter.get("rating")
            if rstr:
                try:
                    rv = float(rstr)
                    if rv < 0 or rv > 5:
                        errors.append(f"Interaction rating out of range (0–5): {rv}")
                except:
                    errors.append(f"Invalid interaction rating: {rstr}")

        # Append to report
        if errors:
            report["invalid_records"].append({"recipe_id": rid, "errors": errors})
        else:
            report["valid_records"].append(rid)

    # Summary update
    report["summary"]["valid_recipes"] = len(report["valid_records"])
    report["summary"]["invalid_recipes"] = len(report["invalid_records"])

    # Output directory
    os.makedirs("data_validation", exist_ok=True)

    # Write JSON report
    with open("data_validation/validation_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print("Validation Complete.")
    print("Summary:", report["summary"])


if __name__ == "__main__":
    validate_recipes()
