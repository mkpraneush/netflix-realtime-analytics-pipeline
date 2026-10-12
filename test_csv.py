import pandas as pd

from data_cleaning import clean_titles, clean_credits


# ==========================================
# 1. LOAD RAW DATA
# ==========================================

titles = pd.read_csv("data/titles.csv")
credits = pd.read_csv("data/credits.csv")


# ==========================================
# 2. CLEAN DATA
# ==========================================

cleaned_titles = clean_titles(titles)
cleaned_credits = clean_credits(credits)


# ==========================================
# 3. APPLY FINAL CLEANING RULES
# ==========================================

cleaned_titles["title"] = cleaned_titles["title"].fillna("Unknown Title")

cleaned_titles["description"] = (
    cleaned_titles["description"]
    .fillna("No description available")
)

cleaned_titles["age_certification"] = (
    cleaned_titles["age_certification"]
    .fillna("Unknown")
)

# Movies do not have seasons
cleaned_titles.loc[
    cleaned_titles["type"] == "MOVIE",
    "seasons"
] = pd.NA

# Keep observed numeric metrics as NULL
numeric_columns = [
    "imdb_score",
    "imdb_votes",
    "tmdb_popularity",
    "tmdb_score"
]

for column in numeric_columns:
    cleaned_titles[column] = pd.to_numeric(
        cleaned_titles[column],
        errors="coerce"
    )

# Credits
cleaned_credits["character"] = (
    cleaned_credits["character"].fillna("N/A")
)

# Remove duplicates
cleaned_titles = cleaned_titles.drop_duplicates()
cleaned_credits = cleaned_credits.drop_duplicates()

# Remove credits without ID
cleaned_credits = cleaned_credits.dropna(subset=["id"])


# ==========================================
# 4. DATABASE COMPATIBILITY CHECK
# ==========================================

print("\n==========================================")
print("DATABASE COMPATIBILITY CHECK")
print("==========================================")


# ------------------------------------------
# CHECK 1: TITLES ID UNIQUE
# ------------------------------------------

duplicate_ids = cleaned_titles["id"].duplicated().sum()

print("\n1. Duplicate title IDs:", duplicate_ids)

if duplicate_ids == 0:
    print("PASS - Every title ID is unique.")
else:
    print("FAIL - Duplicate title IDs found.")


# ------------------------------------------
# CHECK 2: CREDITS ID REFERENCES TITLES
# ------------------------------------------

valid_title_ids = set(cleaned_titles["id"])

invalid_credit_ids = (
    ~cleaned_credits["id"].isin(valid_title_ids)
).sum()

print("\n2. Credits with invalid title IDs:", invalid_credit_ids)

if invalid_credit_ids == 0:
    print("PASS - All credit IDs exist in titles.")
else:
    print("FAIL - Some credit IDs do not exist in titles.")


# ------------------------------------------
# CHECK 3: NULL PRIMARY KEY VALUES
# ------------------------------------------

null_title_ids = cleaned_titles["id"].isna().sum()

null_credit_person_ids = (
    cleaned_credits["person_id"].isna().sum()
)

null_credit_ids = cleaned_credits["id"].isna().sum()

print("\n3. NULL primary/key values:")
print("Title ID NULL:", null_title_ids)
print("Credit person_id NULL:", null_credit_person_ids)
print("Credit ID NULL:", null_credit_ids)


# ------------------------------------------
# CHECK 4: NUMERIC DATA TYPES
# ------------------------------------------

print("\n4. Numeric data types:")

print(
    cleaned_titles[
        [
            "release_year",
            "runtime",
            "seasons",
            "imdb_score",
            "imdb_votes",
            "tmdb_popularity",
            "tmdb_score"
        ]
    ].dtypes
)


# ------------------------------------------
# CHECK 5: INVALID RATINGS
# ------------------------------------------

invalid_imdb_scores = (
    (
        cleaned_titles["imdb_score"] < 0
    ) |
    (
        cleaned_titles["imdb_score"] > 10
    )
).sum()

invalid_tmdb_scores = (
    (
        cleaned_titles["tmdb_score"] < 0
    ) |
    (
        cleaned_titles["tmdb_score"] > 10
    )
).sum()

print("\n5. Invalid ratings:")
print("Invalid IMDb scores:", invalid_imdb_scores)
print("Invalid TMDB scores:", invalid_tmdb_scores)


# ------------------------------------------
# CHECK 6: NEGATIVE VOTES / POPULARITY
# ------------------------------------------

negative_votes = (
    cleaned_titles["imdb_votes"] < 0
).sum()

negative_popularity = (
    cleaned_titles["tmdb_popularity"] < 0
).sum()

print("\n6. Negative values:")
print("Negative IMDb votes:", negative_votes)
print("Negative TMDB popularity:", negative_popularity)


# ------------------------------------------
# CHECK 7: COLUMN STRUCTURE
# ------------------------------------------

expected_titles_columns = [
    "id",
    "title",
    "type",
    "description",
    "release_year",
    "age_certification",
    "runtime",
    "genres",
    "production_countries",
    "seasons",
    "imdb_id",
    "imdb_score",
    "imdb_votes",
    "tmdb_popularity",
    "tmdb_score"
]

expected_credits_columns = [
    "person_id",
    "id",
    "name",
    "character",
    "role"
]

print("\n7. Column structure:")

if list(cleaned_titles.columns) == expected_titles_columns:
    print("PASS - Titles columns match MySQL structure.")
else:
    print("FAIL - Titles columns do not match.")

if list(cleaned_credits.columns) == expected_credits_columns:
    print("PASS - Credits columns match MySQL structure.")
else:
    print("FAIL - Credits columns do not match.")


# ==========================================
# FINAL RESULT
# ==========================================

print("\n==========================================")
print("FINAL VERIFICATION COMPLETE")
print("==========================================")

if (
    duplicate_ids == 0
    and invalid_credit_ids == 0
    and null_title_ids == 0
    and null_credit_person_ids == 0
    and null_credit_ids == 0
    and invalid_imdb_scores == 0
    and invalid_tmdb_scores == 0
    and negative_votes == 0
    and negative_popularity == 0
):
    print("SUCCESS - Dataset is ready for MySQL.")
else:
    print("WARNING - Some issues need to be reviewed.")