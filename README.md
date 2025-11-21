# ETL_Pipeline_Activity_6
This project is a complete data engineering pipeline built on Firebase Firestore. It collects recipe data, exports it, transforms it into clean CSV files, validates the quality of the data, and generates analytics insights.

The pipeline does:
1. Export Firestore collections into JSON
2. Transform the JSON into clean CSV files
3. Validate the transformed data
4. Run analytics to generate insights + charts
5. Store results as CSV, JSON, charts

# **Data Model -**

<img width="6096" height="2117" alt="ERD_Diagram" src="https://github.com/user-attachments/assets/2050160c-5930-49b8-9e00-cce3d8a6197f" />

### 1. Recipe (Root Collection)
  This is the main collection where all recipes are stored.\
  Each recipe document contains basic recipe information such as the title, description, ingredients, steps, time required, difficulty, etc.

### 2. Interaction (Subcollection inside each Recipe)
  Inside each recipe, there is an Interaction subcollection.\
  This subcollection stores actions performed by users on that specific recipe, such as:\
  views,likes,ratings,comments (cook notes)

-------- Why is it a subcollection? -------------\
  Because each recipe can have many interactions, and storing them under the recipe:\
  keeps recipe-related activity grouped together\
  makes queries like “get interactions for one recipe” very fast\
  avoids scanning thousands of interactions across all recipes

### 3. Users (Root Collection)
  This collection stores information about all users.\
  Each user is a document containing basic profile details.

### 4. Activities (Subcollection inside each User)
  Each user has an Activities subcollection.\
  This stores actions that the user performs across any recipe, such as:\
  viewed a recipe,liked a recipe,added a note,rated a recipe

# **How to Run the Pipeline -**
### Step 1 - Install Dependencies
> pip install firebase-admin pandas matplotlib numpy google-cloud-firestore

### Step 2 — Export Firestore Data
> python firestore_export.py\
> Output → data_export/recipes.json & users.json

### Step 3 — Transform JSON → CSV
> python transform_to_csv.py\
> Output → recipe.csv, ingredients.csv, steps.csv, interactions.csv

### Step 4 — Validate CSV Data
> python validator.py\
> Output → validation_report.json (lists valid + invalid recipes)

### Step 5 — Run Analytics
> python analytics.py

# **Outputs -**
> Charts → analytics/charts/\
> Summary → analytics/analytics_summary.json\
> CSV → top ingredients, top rated recipes

<img width="200" height="200" alt="difficulty_distribution" src="https://github.com/user-attachments/assets/310bc248-858d-4936-bac5-2a56015c04a1" /> <img width="200" height="200" alt="prep_vs_rating" src="https://github.com/user-attachments/assets/92cde96d-e47e-491d-9026-60c1ca729931" /> <img width="200" height="200" alt="top_ingredients" src="https://github.com/user-attachments/assets/e70d5a86-1d5d-4aff-98ff-02e401b336bc" />





# **ETL Process**

## E → Extract
**firestore_export.py\** \
  Reads all Recipes & Interactions\
  Reads all Users\
  Saves as JSON

## T → Transform
**transform_to_csv.py\** \
  Converts JSON to clean CSV tables\
  Converts durations to seconds\
  Fixes missing fields\
  Creates IDs when missing

## L → Load
  Not storing back into Firestore → loading means\
  “prepare for analytics in CSV format”.

## Validate
**validator.py checks:\** \
  Missing fields\
  Invalid difficulty\
  Prep/Cook/Total time logic\
  Non-positive ingredient quantity\
  Rating range (0–5)

## Analyze
**analytics.py creates:\** \
  Most common ingredients\
  Difficulty distribution\
  Correlation between prep time and rating\
  Top rated recipes\
  Recipe step distribution\
  Charts

# **Insights Summary (Example Output)**

### The analytics generates:

- Top 20 most common ingredients
- Average prep time & cook time
- Most interacted recipes
- Top-rated recipes
- Ingredients associated with high ratings
- Correlation between prep time & rating
- Recipes with most comments
- Longest total time recipes

### You can find all results in:
> analytics/analytics_summary.json

# **Known Constraints / Limitations**

### Firestore limitations
  Firestore does not support joins → therefore, interactions are grouped under recipes.\
  Querying huge subcollections may cost more reads.
### Local CSV files must exist
  If export step fails, analytics won’t run.
