-- ============================================================
-- Netflix Data Analytics Pipeline
-- SQL Analytical Views
-- Database: netflix_analytics
-- MySQL 8+
-- ============================================================

USE netflix_analytics;


-- ============================================================
-- VIEW 1: vw_content_summary
-- Purpose: Overall Movie vs Show performance summary
-- ============================================================

CREATE OR REPLACE VIEW vw_content_summary AS
SELECT
    t.type AS type,
    COUNT(DISTINCT t.id) AS total_content,
    ROUND(AVG(t.imdb_score), 2) AS avg_imdb_score,
    ROUND(AVG(t.tmdb_score), 2) AS avg_tmdb_score,
    ROUND(AVG(t.runtime), 2) AS avg_runtime,
    COALESCE(SUM(t.imdb_votes), 0) AS total_imdb_votes,
    ROUND(AVG(t.tmdb_popularity), 2) AS avg_tmdb_popularity
FROM titles t
GROUP BY t.type;


-- ============================================================
-- VIEW 2: vw_yearly_content_trend
-- Purpose: Yearly content growth - Movies vs Shows
-- ============================================================

CREATE OR REPLACE VIEW vw_yearly_content_trend AS
SELECT
    t.release_year AS release_year,
    COUNT(DISTINCT CASE
        WHEN t.type = 'MOVIE' THEN t.id
    END) AS movie_count,
    COUNT(DISTINCT CASE
        WHEN t.type = 'SHOW' THEN t.id
    END) AS show_count,
    COUNT(DISTINCT t.id) AS total_content
FROM titles t
WHERE t.release_year IS NOT NULL
GROUP BY t.release_year;


-- ============================================================
-- VIEW 3: vw_genre_performance
-- Purpose: Performance analysis by individual genre
-- ============================================================

CREATE OR REPLACE VIEW vw_genre_performance AS
WITH RECURSIVE genre_split AS (

    SELECT
        t.id AS title_id,
        t.imdb_score AS imdb_score,
        t.tmdb_score AS tmdb_score,
        t.runtime AS runtime,
        TRIM(SUBSTRING_INDEX(t.genres, ',', 1)) AS genre,
        CASE
            WHEN LOCATE(',', t.genres) > 0
            THEN SUBSTRING(
                t.genres,
                LOCATE(',', t.genres) + 1
            )
            ELSE NULL
        END AS remaining_genres
    FROM titles t
    WHERE t.genres IS NOT NULL
      AND TRIM(t.genres) <> ''

    UNION ALL

    SELECT
        gs.title_id,
        gs.imdb_score,
        gs.tmdb_score,
        gs.runtime,
        TRIM(
            SUBSTRING_INDEX(gs.remaining_genres, ',', 1)
        ) AS genre,
        CASE
            WHEN LOCATE(',', gs.remaining_genres) > 0
            THEN SUBSTRING(
                gs.remaining_genres,
                LOCATE(',', gs.remaining_genres) + 1
            )
            ELSE NULL
        END AS remaining_genres
    FROM genre_split gs
    WHERE gs.remaining_genres IS NOT NULL
)

SELECT
    genre AS genre,
    COUNT(DISTINCT title_id) AS content_count,
    ROUND(AVG(imdb_score), 2) AS avg_imdb_score,
    ROUND(AVG(tmdb_score), 2) AS avg_tmdb_score,
    ROUND(AVG(runtime), 2) AS avg_runtime
FROM genre_split
WHERE genre IS NOT NULL
  AND genre <> ''
GROUP BY genre;


-- ============================================================
-- VIEW 4: vw_people_performance
-- Purpose: Performance analysis for Actors and Directors
-- ============================================================

CREATE OR REPLACE VIEW vw_people_performance AS
WITH person_titles AS (

    /*
       Create exactly one row for each:
       person + role + title
    */

    SELECT DISTINCT
        c.person_id AS person_id,
        c.name AS person_name,
        c.role AS role,
        t.id AS title_id,
        t.imdb_score AS imdb_score,
        t.tmdb_score AS tmdb_score,
        t.imdb_votes AS imdb_votes
    FROM credits c
    INNER JOIN titles t
        ON c.id = t.id
    WHERE c.role IN ('ACTOR', 'DIRECTOR')
)

SELECT
    person_name AS person_name,
    role AS role,
    COUNT(DISTINCT title_id) AS title_count,
    ROUND(AVG(imdb_score), 2) AS average_imdb_score,
    ROUND(AVG(tmdb_score), 2) AS average_tmdb_score,
    COALESCE(SUM(imdb_votes), 0) AS total_imdb_votes
FROM person_titles
GROUP BY
    person_name,
    role;


-- ============================================================
-- VIEW 5: vw_content_ranking
-- Purpose: Analytical ranking of Netflix content
--
-- Ranking weights:
-- IMDb Score       = 35%
-- TMDB Score       = 25%
-- IMDb Votes       = 25%
-- TMDB Popularity  = 15%
-- ============================================================

CREATE OR REPLACE VIEW vw_content_ranking AS

WITH log_metrics AS (

    /*
       Transform IMDb votes using logarithm.
       NULL votes remain NULL.
    */

    SELECT
        t.id AS title_id,
        t.title AS title,
        t.type AS type,
        t.release_year AS release_year,
        t.imdb_score AS imdb_score,
        t.imdb_votes AS imdb_votes,
        t.tmdb_score AS tmdb_score,
        t.tmdb_popularity AS tmdb_popularity,

        CASE
            WHEN t.imdb_votes IS NULL THEN NULL
            ELSE LOG10(t.imdb_votes + 1)
        END AS imdb_votes_log

    FROM titles t
),


bounds AS (

    /*
       Find minimum and maximum values
       for each metric.
    */

    SELECT
        MIN(imdb_score) AS min_imdb_score,
        MAX(imdb_score) AS max_imdb_score,

        MIN(tmdb_score) AS min_tmdb_score,
        MAX(tmdb_score) AS max_tmdb_score,

        MIN(imdb_votes_log) AS min_imdb_votes_log,
        MAX(imdb_votes_log) AS max_imdb_votes_log,

        MIN(tmdb_popularity) AS min_tmdb_popularity,
        MAX(tmdb_popularity) AS max_tmdb_popularity

    FROM log_metrics
),


normalized AS (

    /*
       Normalize all metrics to 0-100.
    */

    SELECT

        lm.title_id,
        lm.title,
        lm.type,
        lm.release_year,
        lm.imdb_score,
        lm.imdb_votes,
        lm.tmdb_score,
        lm.tmdb_popularity,

        -- IMDb Score normalization
        CASE
            WHEN lm.imdb_score IS NULL THEN 0
            WHEN b.max_imdb_score = b.min_imdb_score THEN 0
            ELSE
                (
                    (lm.imdb_score - b.min_imdb_score)
                    /
                    (b.max_imdb_score - b.min_imdb_score)
                ) * 100
        END AS imdb_score_norm,


        -- TMDB Score normalization
        CASE
            WHEN lm.tmdb_score IS NULL THEN 0
            WHEN b.max_tmdb_score = b.min_tmdb_score THEN 0
            ELSE
                (
                    (lm.tmdb_score - b.min_tmdb_score)
                    /
                    (b.max_tmdb_score - b.min_tmdb_score)
                ) * 100
        END AS tmdb_score_norm,


        -- Log IMDb Votes normalization
        CASE
            WHEN lm.imdb_votes_log IS NULL THEN 0
            WHEN b.max_imdb_votes_log = b.min_imdb_votes_log THEN 0
            ELSE
                (
                    (lm.imdb_votes_log - b.min_imdb_votes_log)
                    /
                    (b.max_imdb_votes_log - b.min_imdb_votes_log)
                ) * 100
        END AS imdb_votes_log_norm,


        -- TMDB Popularity normalization
        CASE
            WHEN lm.tmdb_popularity IS NULL THEN 0
            WHEN b.max_tmdb_popularity = b.min_tmdb_popularity THEN 0
            ELSE
                (
                    (lm.tmdb_popularity - b.min_tmdb_popularity)
                    /
                    (b.max_tmdb_popularity - b.min_tmdb_popularity)
                ) * 100
        END AS tmdb_popularity_norm

    FROM log_metrics lm
    CROSS JOIN bounds b
)


SELECT

    title_id AS id,
    title,
    type,
    release_year,

    imdb_score,
    imdb_votes,

    tmdb_score,
    tmdb_popularity,

    ROUND(imdb_score_norm, 2) AS imdb_score_norm,

    ROUND(tmdb_score_norm, 2) AS tmdb_score_norm,

    ROUND(imdb_votes_log_norm, 2) AS imdb_votes_log_norm,

    ROUND(tmdb_popularity_norm, 2) AS tmdb_popularity_norm,


    /*
       Final weighted analytical score
    */

    ROUND(
          (0.35 * imdb_score_norm)
        + (0.25 * tmdb_score_norm)
        + (0.25 * imdb_votes_log_norm)
        + (0.15 * tmdb_popularity_norm),
        2
    ) AS final_score,


    /*
       Rank content from highest score to lowest.
    */

    DENSE_RANK() OVER (
        ORDER BY
              (0.35 * imdb_score_norm)
            + (0.25 * tmdb_score_norm)
            + (0.25 * imdb_votes_log_norm)
            + (0.15 * tmdb_popularity_norm)
        DESC
    ) AS content_rank

FROM normalized;