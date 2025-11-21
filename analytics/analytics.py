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

    # Convert numeric field
    recipes["prep_time"] = pd.to_numeric(recipes["prep_time"], errors="coerce")
    recipes["cook_time"] = pd.to_numeric(recipes["cook_time"], errors="coerce")
    recipes["total_time"] = pd.to_numeric(recipes["total_time"], errors="coerce")

    interactions["rating"] = pd.to_numeric(interactions["rating"], errors="coerce")

    return recipes, ingredients, steps, interactions


def insights(recipes, ingredients, steps, interactions):
    out = {}

    # most common ingredients
    out["most_common_ingredients"] = (
        ingredients["name"].value_counts().head(20).to_dict()
    )

    # average preparation time
    out["avg_prep_time"] = recipes["prep_time"].mean()

    out["avg_cook_time"] = recipes["cook_time"].mean()

    out["difficulty_distribution"] = recipes["difficulty"].value_counts().to_dict()

    # most interacted recipes
    out["most_interacted"] = (
        interactions["recipe_id"].value_counts().head(20).to_dict()
    )

    avg_ratings = interactions.groupby("recipe_id")["rating"].mean().reset_index()
    merged = recipes.merge(avg_ratings, on="recipe_id", how="left")
    out["prep_vs_rating_corr"] = merged["prep_time"].corr(merged["rating"])

 
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

    # top rated recipes
    top_rated = (
        merged.sort_values("rating", ascending=False)
        .head(10)[["recipe_id", "title", "rating"]]
        .to_dict(orient="records")
    )
    out["top_rated_recipes"] = top_rated

    steps_count = steps.groupby("recipe_id").size().rename("steps_count")
    out["steps_count_distribution"] = steps_count.describe().to_dict()

    # most comments recipe
    comments = interactions[
        interactions["cooknote"].notnull()
        & (interactions["cooknote"].str.strip() != "")
    ]
    out["recipes_most_comments"] = (
        comments["recipe_id"].value_counts().head(10).to_dict()
    )

    # longest time recipe
    out["longest_total_time"] = (
        recipes[["recipe_id", "title", "total_time"]]
        .sort_values("total_time", ascending=False)
        .head(10)
        .to_dict(orient="records")
    )

    # save into csv
    os.makedirs("analytics", exist_ok=True)
    pd.Series(out["most_common_ingredients"]).to_csv(
        "analytics/most_common_ingredients.csv"
    )
    pd.DataFrame(out["top_rated_recipes"]).to_csv(
        "analytics/top_rated_recipes.csv", index=False
    )

    # save into json
    with open("analytics/analytics_summary.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, default=str)

    return out


# chart generation using scatter plot
def generate_charts(recipes, ingredients, interactions, out):
    os.makedirs("analytics/charts", exist_ok=True)

    recipes["difficulty"].value_counts().plot(
        kind="bar", title="Difficulty Distribution"
    )
    plt.tight_layout()
    plt.savefig("analytics/charts/difficulty_distribution.png")
    plt.clf()

    top_ing = pd.Series(out["most_common_ingredients"])
    top_ing.head(15).plot(kind="bar", title="Top Ingredients")
    plt.tight_layout()
    plt.savefig("analytics/charts/top_ingredients.png")
    plt.clf()

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
