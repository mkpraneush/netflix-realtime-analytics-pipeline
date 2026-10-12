import pandas as pd
import numpy as np


def standardize_missing_values(df):
    df = df.copy()

    missing_values = [
        "",
        " ",
        "NA",
        "N/A",
        "na",
        "n/a",
        "NULL",
        "null",
        "None",
        "none",
        "NaN",
        "nan",
        "-"
    ]

    df = df.replace(missing_values, np.nan)

    return df


def clean_column_names(df):
    df = df.copy()

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )

    return df


def remove_duplicate_rows(df):
    df = df.copy()

    before = len(df)

    df = df.drop_duplicates()

    removed = before - len(df)

    return df, removed


def clean_text_columns(df):
    df = df.copy()

    text_columns = df.select_dtypes(include=["object"]).columns

    for column in text_columns:
        df[column] = df[column].apply(
            lambda x: x.strip() if isinstance(x, str) else x
        )

    return df


def detect_numeric_outliers(df, columns):
    report = {}

    for column in columns:

        if column not in df.columns:
            continue

        series = pd.to_numeric(df[column], errors="coerce").dropna()

        if len(series) == 0:
            continue

        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)

        iqr = q3 - q1

        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        outliers = series[
            (series < lower) | (series > upper)
        ]

        report[column] = {
            "Q1": q1,
            "Q3": q3,
            "IQR": iqr,
            "lower_bound": lower,
            "upper_bound": upper,
            "outlier_count": len(outliers)
        }

    return report


def fill_categorical_missing(df, columns):
    df = df.copy()

    for column in columns:

        if column not in df.columns:
            continue

        df[column] = df[column].fillna("Unknown")

    return df


def fill_numeric_missing_with_median(df, columns):
    df = df.copy()

    for column in columns:

        if column not in df.columns:
            continue

        median_value = df[column].median()

        if pd.notna(median_value):
            df[column] = df[column].fillna(median_value)

    return df


def validate_numeric_range(df, column, minimum=None, maximum=None):

    if column not in df.columns:
        return df

    if minimum is not None:
        df.loc[df[column] < minimum, column] = np.nan

    if maximum is not None:
        df.loc[df[column] > maximum, column] = np.nan

    return df


def clean_titles(df):

    df = clean_column_names(df)

    df = standardize_missing_values(df)

    df = clean_text_columns(df)

    df, duplicate_count = remove_duplicate_rows(df)

    if "id" in df.columns:
        df = df.drop_duplicates(subset="id")

    categorical_columns = [
        "age_certification"
    ]

    df = fill_categorical_missing(
        df,
        categorical_columns
    )

    if "description" in df.columns:
        df["description"] = df["description"].fillna(
            "No description available"
        )

    if "imdb_score" in df.columns:
        df = validate_numeric_range(
            df,
            "imdb_score",
            minimum=0,
            maximum=10
        )

    if "tmdb_score" in df.columns:
        df = validate_numeric_range(
            df,
            "tmdb_score",
            minimum=0,
            maximum=10
        )

    if "runtime" in df.columns:
        df = validate_numeric_range(
            df,
            "runtime",
            minimum=0
        )

    if "release_year" in df.columns:
        df = validate_numeric_range(
            df,
            "release_year",
            minimum=1888
        )

    return df


def clean_credits(df, valid_title_ids=None):

    df = clean_column_names(df)

    df = standardize_missing_values(df)

    df = clean_text_columns(df)

    if "character" in df.columns:
        df["character"] = df["character"].fillna("N/A")

    if valid_title_ids is not None and "id" in df.columns:
        df = df[
            df["id"].isin(valid_title_ids)
        ]

    if all(
        column in df.columns
        for column in ["person_id", "id", "role"]
    ):
        df = df.drop_duplicates(
            subset=[
                "person_id",
                "id",
                "role"
            ]
        )

    return df


def generate_quality_report(df):

    report = pd.DataFrame({
        "column": df.columns,
        "data_type": [
            str(dtype)
            for dtype in df.dtypes
        ],
        "total_rows": len(df),
        "missing_count": [
            df[column].isna().sum()
            for column in df.columns
        ],
        "missing_percentage": [
            round(
                df[column].isna().mean() * 100,
                2
            )
            for column in df.columns
        ],
        "unique_values": [
            df[column].nunique(dropna=True)
            for column in df.columns
        ]
    })

    return report


def validate_clean_data(df):

    problems = {}

    problems["duplicate_rows"] = df.duplicated().sum()

    problems["total_missing_values"] = df.isna().sum().sum()

    problems["empty_strings"] = (
        df.astype(str)
        .apply(
            lambda column:
            column.str.strip().eq("").sum()
        )
        .sum()
    )

    return problems