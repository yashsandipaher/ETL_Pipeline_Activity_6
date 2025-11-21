import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import json


def load_csvs():
    recipes = pd.read_csv("data_transform/recipe.csv")
    ingredients = pd.read_csv("data_transform/ingredients.csv")
    steps = pd.read_csv("data_transform/steps.csv")
    interactions = pd.read_csv("data_transform/interactions.csv")

    # Convert numeric fields properly
    recipes["prep_time"] = pd.to_numeric(recipes["prep_time"], errors="coerce")
    recipes["cook_time"] = pd.to_numeric(recipes["cook_time"], errors="coerce")
    recipes["total_time"] = pd.to_numeric(recipes["total_time"], errors="coerce")

    interactions["rating"] = pd.to_numeric(interactions["rating"], errors="coerce")

    return recipes, ingredients, steps, interactions


def insights(recipes, ingredients, steps, interactions):
    out = {}

    # 1. Most common ingredients
    out["most_common_ingredients"] = (
        ingredients["name"].value_counts().head(20).to_dict()
    )

    # 2. Average preparation time
    out["avg_prep_time"] = recipes["prep_time"].mean()

    # 3. Average cooking time
    out["avg_cook_time"] = recipes["cook_time"].mean()

    # 4. Difficulty distribution
    out["difficulty_distribution"] = recipes["difficulty"].value_counts().to_dict()

    # 5. Most interacted recipes
    out["most_interacted"] = (
        interactions["recipe_id"].value_counts().head(20).to_dict()
    )

    # 6. Correlation between prep time and average rating
    avg_ratings = interactions.groupby("recipe_id")["rating"].mean().reset_index()
    merged = recipes.merge(avg_ratings, on="recipe_id", how="left")
    out["prep_vs_rating_corr"] = merged["prep_time"].corr(merged["rating"])

    # 7. Ingredients linked to higher ratings
    ing_ratings = ingredients.merge(
        interactions[["recipe_id", "rating"]], on="recipe_id", how="left"
    )
    ing_ratings["rating"] = pd.to_numeric(
        ing_ratings["rating"], errors="coerce"
    )

    ing_score = (
        ing_ratings.groupby("name")["rating"]
        .mean()
        .dropna()
        .sort_values(ascending=False)
        .head(20)
    )
    out["ingredients_high_rating"] = ing_score.to_dict()

    # 8. Top rated recipes
    top_rated = (
        merged.sort_values("rating", ascending=False)
        .head(10)[["recipe_id", "title", "rating"]]
        .to_dict(orient="records")
    )
    out["top_rated_recipes"] = top_rated

    # 9. Steps count distribution
    steps_count = steps.groupby("recipe_id").size().rename("steps_count")
    out["steps_count_distribution"] = steps_count.describe().to_dict()

    # 10. Recipes with most comments
    comments = interactions[
        interactions["cooknote"].notnull()
        & (interactions["cooknote"].str.strip() != "")
    ]
    out["recipes_most_comments"] = (
        comments["recipe_id"].value_counts().head(10).to_dict()
    )

    # 11. Longest total time recipes
    out["longest_total_time"] = (
        recipes[["recipe_id", "title", "total_time"]]
        .sort_values("total_time", ascending=False)
        .head(10)
        .to_dict(orient="records")
    )

    # Save useful CSVs
    os.makedirs("analytics", exist_ok=True)
    pd.Series(out["most_common_ingredients"]).to_csv(
        "analytics/most_common_ingredients.csv"
    )
    pd.DataFrame(out["top_rated_recipes"]).to_csv(
        "analytics/top_rated_recipes.csv", index=False
    )

    # Save summary JSON
    with open("analytics/analytics_summary.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, default=str)

    return out


def generate_charts(recipes, ingredients, interactions, out):
    os.makedirs("analytics/charts", exist_ok=True)

    # Difficulty distribution
    recipes["difficulty"].value_counts().plot(
        kind="bar", title="Difficulty Distribution"
    )
    plt.tight_layout()
    plt.savefig("analytics/charts/difficulty_distribution.png")
    plt.clf()

    # Top ingredients
    top_ing = pd.Series(out["most_common_ingredients"])
    top_ing.head(15).plot(kind="bar", title="Top Ingredients")
    plt.tight_layout()
    plt.savefig("analytics/charts/top_ingredients.png")
    plt.clf()

    # Prep time vs rating scatter plot
    avg_ratings = interactions.groupby("recipe_id")["rating"].mean().reset_index()
    merged = recipes.merge(avg_ratings, on="recipe_id", how="left")

    merged.plot.scatter(x="prep_time", y="rating", title="Prep Time vs Rating")
    plt.tight_layout()
    plt.savefig("analytics/charts/prep_vs_rating.png")
    plt.clf()


if __name__ == "__main__":
    recipes, ingredients, steps, interactions = load_csvs()
    out = insights(recipes, ingredients, steps, interactions)
    generate_charts(recipes, ingredients, interactions, out)
    print("Analytics complete. Summary saved to analytics/analytics_summary.json")
