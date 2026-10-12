import mysql.connector
import config
 
 
# ============================================================
# DATABASE CONNECTION
# ============================================================
 
def create_connection():
    """Create and return a connection to the netflix_analytics MySQL database."""
    connection = mysql.connector.connect(
        host=config.DB_HOST,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        database=config.DB_NAME
    )
    return connection
 
 
# ============================================================
# 1. TOTAL NETFLIX CONTENT
# ============================================================
 
def total_content():
    connection = create_connection()
    cursor = connection.cursor()
 
    try:
        query = "SELECT COUNT(*) FROM titles;"
        cursor.execute(query)
        result = cursor.fetchone()
 
        print("\n=== 1. TOTAL NETFLIX CONTENT ===")
        print(f"Total Netflix Content: {result[0]}")
    finally:
        cursor.close()
        connection.close()
 
 
# ============================================================
# 2. NETFLIX CONTENT BY TYPE
# ============================================================
 
def content_by_type():
    connection = create_connection()
    cursor = connection.cursor()
 
    try:
        query = """
            SELECT type, COUNT(*) AS total
            FROM titles
            GROUP BY type;
        """
        cursor.execute(query)
        results = cursor.fetchall()
 
        print("\n=== 2. NETFLIX CONTENT BY TYPE ===")
        for row in results:
            print(f"{row[0]}: {row[1]}")
    finally:
        cursor.close()
        connection.close()
 
 
# ============================================================
# 3. COMPLETE DATA QUALITY AUDIT
# ============================================================
 
def data_quality_audit():
    connection = create_connection()
    cursor = connection.cursor()
 
    try:
        print("\n=== 3. COMPLETE DATA QUALITY AUDIT ===")
 
        checks = {
            "Invalid content types": """
                SELECT COUNT(*) FROM titles
                WHERE type NOT IN ('MOVIE', 'SHOW');
            """,
            "Invalid release years": """
                SELECT COUNT(*) FROM titles
                WHERE release_year IS NOT NULL
                AND (release_year < 1900 OR release_year > 2100);
            """,
            "Invalid runtime": """
                SELECT COUNT(*) FROM titles
                WHERE runtime IS NOT NULL AND runtime < 0;
            """,
            "Invalid IMDb scores": """
                SELECT COUNT(*) FROM titles
                WHERE imdb_score IS NOT NULL
                AND (imdb_score < 0 OR imdb_score > 10);
            """,
            "Invalid TMDB scores": """
                SELECT COUNT(*) FROM titles
                WHERE tmdb_score IS NOT NULL
                AND (tmdb_score < 0 OR tmdb_score > 10);
            """,
            "Negative IMDb votes": """
                SELECT COUNT(*) FROM titles
                WHERE imdb_votes IS NOT NULL AND imdb_votes < 0;
            """,
            "Negative TMDB popularity": """
                SELECT COUNT(*) FROM titles
                WHERE tmdb_popularity IS NOT NULL AND tmdb_popularity < 0;
            """,
            "Movies with seasons": """
                SELECT COUNT(*) FROM titles
                WHERE type = 'MOVIE' AND seasons IS NOT NULL;
            """,
            "Shows without seasons": """
                SELECT COUNT(*) FROM titles
                WHERE type = 'SHOW' AND seasons IS NULL;
            """,
            "Credits with invalid title ID": """
                SELECT COUNT(*) FROM credits c
                LEFT JOIN titles t ON c.id = t.id
                WHERE t.id IS NULL;
            """,
            "Empty title names": """
                SELECT COUNT(*) FROM titles
                WHERE title IS NULL OR TRIM(title) = '';
            """
        }
 
        for label, query in checks.items():
            cursor.execute(query)
            result = cursor.fetchone()
            print(f"{label}: {result[0]}")
    finally:
        cursor.close()
        connection.close()
 
 
# ============================================================
# 4. NETFLIX CONTENT RELEASED BY YEAR
# ============================================================
 
def content_by_year():
    connection = create_connection()
    cursor = connection.cursor()
 
    try:
        query = """
            SELECT release_year, COUNT(*) AS total
            FROM titles
            WHERE release_year IS NOT NULL
            GROUP BY release_year
            ORDER BY release_year ASC;
        """
        cursor.execute(query)
        results = cursor.fetchall()
 
        print("\n=== 4. NETFLIX CONTENT RELEASED BY YEAR ===")
        for row in results:
            print(f"{row[0]}: {row[1]}")
    finally:
        cursor.close()
        connection.close()
 
 
# ============================================================
# 5. AVERAGE IMDb SCORE
# ============================================================
 
def average_imdb_score():
    connection = create_connection()
    cursor = connection.cursor()
 
    try:
        query = """
            SELECT ROUND(AVG(imdb_score), 2)
            FROM titles
            WHERE imdb_score IS NOT NULL;
        """
        cursor.execute(query)
        result = cursor.fetchone()
 
        print("\n=== 5. AVERAGE IMDb SCORE ===")
        print(f"Average IMDb Score: {result[0]}")
    finally:
        cursor.close()
        connection.close()
 
 
# ============================================================
# 6. TOP 10 HIGHEST RATED TITLES
# ============================================================
 
def top_rated_titles():
    connection = create_connection()
    cursor = connection.cursor()
 
    try:
        query = """
            SELECT title, type, release_year, imdb_score
            FROM titles
            WHERE imdb_score IS NOT NULL
            ORDER BY imdb_score DESC
            LIMIT 10;
        """
        cursor.execute(query)
        results = cursor.fetchall()
 
        print("\n=== 6. TOP 10 HIGHEST RATED TITLES ===")
        for row in results:
            print(f"{row[0]} | {row[1]} | {row[2]} | IMDb Score: {row[3]}")
    finally:
        cursor.close()
        connection.close()
 
 
# ============================================================
# 7. TOP 10 MOST VOTED TITLES
# ============================================================
 
def top_voted_titles():
    connection = create_connection()
    cursor = connection.cursor()
 
    try:
        query = """
            SELECT title, type, release_year, imdb_votes
            FROM titles
            WHERE imdb_votes IS NOT NULL
            ORDER BY imdb_votes DESC
            LIMIT 10;
        """
        cursor.execute(query)
        results = cursor.fetchall()
 
        print("\n=== 7. TOP 10 MOST VOTED TITLES ===")
        for row in results:
            print(f"{row[0]} | {row[1]} | {row[2]} | Votes: {row[3]}")
    finally:
        cursor.close()
        connection.close()
 
 
# ============================================================
# 8. AVERAGE IMDb SCORE BY TYPE
# ============================================================
 
def average_imdb_by_type():
    connection = create_connection()
    cursor = connection.cursor()
 
    try:
        query = """
            SELECT type, ROUND(AVG(imdb_score), 2) AS avg_score
            FROM titles
            WHERE imdb_score IS NOT NULL
            GROUP BY type;
        """
        cursor.execute(query)
        results = cursor.fetchall()
 
        print("\n=== 8. AVERAGE IMDb SCORE BY TYPE ===")
        for row in results:
            print(f"{row[0]}: {row[1]}")
    finally:
        cursor.close()
        connection.close()
 
 
# ============================================================
# 9. TOP 10 YEARS BY CONTENT COUNT
# ============================================================
 
def top_years_by_content():
    connection = create_connection()
    cursor = connection.cursor()
 
    try:
        query = """
            SELECT release_year, COUNT(*) AS total_content
            FROM titles
            WHERE release_year IS NOT NULL
            GROUP BY release_year
            ORDER BY total_content DESC
            LIMIT 10;
        """
        cursor.execute(query)
        results = cursor.fetchall()
 
        print("\n=== 9. TOP 10 YEARS BY CONTENT COUNT ===")
        for row in results:
            print(f"{row[0]}: {row[1]}")
    finally:
        cursor.close()
        connection.close()
 
 
# ============================================================
# 10. CONTENT WITH HIGHEST TMDB POPULARITY
# ============================================================
 
def top_tmdb_popularity():
    connection = create_connection()
    cursor = connection.cursor()
 
    try:
        query = """
            SELECT title, type, tmdb_popularity
            FROM titles
            WHERE tmdb_popularity IS NOT NULL
            ORDER BY tmdb_popularity DESC
            LIMIT 10;
        """
        cursor.execute(query)
        results = cursor.fetchall()
 
        print("\n=== 10. CONTENT WITH HIGHEST TMDB POPULARITY ===")
        for row in results:
            print(f"{row[0]} | {row[1]} | Popularity: {row[2]}")
    finally:
        cursor.close()
        connection.close()
 
 
# ============================================================
# 11. TOP ACTORS BY NUMBER OF TITLES
# ============================================================
 
def top_actors():
    connection = create_connection()
    cursor = connection.cursor()
 
    try:
        query = """
            SELECT c.name, COUNT(DISTINCT c.id) AS total_titles
            FROM credits c
            JOIN titles t ON c.id = t.id
            WHERE c.role = 'ACTOR'
            GROUP BY c.name
            ORDER BY total_titles DESC
            LIMIT 10;
        """
        cursor.execute(query)
        results = cursor.fetchall()
 
        print("\n=== 11. TOP ACTORS BY NUMBER OF TITLES ===")
        for row in results:
            print(f"{row[0]}: {row[1]} titles")
    finally:
        cursor.close()
        connection.close()
 
 
# ============================================================
# 12. TOP DIRECTORS BY NUMBER OF TITLES
# ============================================================
 
def top_directors():
    connection = create_connection()
    cursor = connection.cursor()
 
    try:
        query = """
            SELECT c.name, COUNT(DISTINCT c.id) AS total_titles
            FROM credits c
            JOIN titles t ON c.id = t.id
            WHERE c.role = 'DIRECTOR'
            GROUP BY c.name
            ORDER BY total_titles DESC
            LIMIT 10;
        """
        cursor.execute(query)
        results = cursor.fetchall()
 
        print("\n=== 12. TOP DIRECTORS BY NUMBER OF TITLES ===")
        for row in results:
            print(f"{row[0]}: {row[1]} titles")
    finally:
        cursor.close()
        connection.close()
 
 
# ============================================================
# 13. MOVIE VS SHOW AVERAGE / MIN / MAX RUNTIME
# ============================================================
 
def runtime_summary_by_type():
    connection = create_connection()
    cursor = connection.cursor()
 
    try:
        query = """
            SELECT
                type,
                ROUND(AVG(runtime), 2) AS avg_runtime,
                MIN(runtime) AS min_runtime,
                MAX(runtime) AS max_runtime
            FROM titles
            WHERE runtime IS NOT NULL
            GROUP BY type;
        """
        cursor.execute(query)
        results = cursor.fetchall()
 
        print("\n=== 13. MOVIE VS SHOW AVERAGE / MIN / MAX RUNTIME ===")
        for row in results:
            print(f"{row[0]}: Avg={row[1]} | Min={row[2]} | Max={row[3]}")
    finally:
        cursor.close()
        connection.close()
 
 
# ============================================================
# 14. CONTENT QUALITY SUMMARY
# ============================================================
 
def content_quality_summary():
    connection = create_connection()
    cursor = connection.cursor()
 
    try:
        query = """
            SELECT
                COUNT(*) AS total_titles,
                SUM(CASE WHEN type = 'MOVIE' THEN 1 ELSE 0 END) AS total_movies,
                SUM(CASE WHEN type = 'SHOW' THEN 1 ELSE 0 END) AS total_shows,
                SUM(CASE WHEN imdb_score IS NOT NULL THEN 1 ELSE 0 END) AS with_imdb_score,
                SUM(CASE WHEN imdb_score IS NULL THEN 1 ELSE 0 END) AS without_imdb_score,
                SUM(CASE WHEN tmdb_score IS NOT NULL THEN 1 ELSE 0 END) AS with_tmdb_score,
                SUM(CASE WHEN tmdb_score IS NULL THEN 1 ELSE 0 END) AS without_tmdb_score
            FROM titles;
        """
        cursor.execute(query)
        result = cursor.fetchone()
 
        print("\n=== 14. CONTENT QUALITY SUMMARY ===")
        print(f"Total Titles: {result[0]}")
        print(f"Total Movies: {result[1]}")
        print(f"Total Shows: {result[2]}")
        print(f"Titles With IMDb Score: {result[3]}")
        print(f"Titles Without IMDb Score: {result[4]}")
        print(f"Titles With TMDB Score: {result[5]}")
        print(f"Titles Without TMDB Score: {result[6]}")
    finally:
        cursor.close()
        connection.close()
 
 
# ============================================================
# 15. MISSING VALUES SUMMARY
# ============================================================
 
def missing_values_summary():
    connection = create_connection()
    cursor = connection.cursor()
 
    try:
        query = """
            SELECT
                SUM(CASE WHEN title IS NULL OR TRIM(title) = '' THEN 1 ELSE 0 END) AS missing_title,
                SUM(CASE WHEN description IS NULL OR TRIM(description) = '' THEN 1 ELSE 0 END) AS missing_description,
                SUM(CASE WHEN age_certification IS NULL OR TRIM(age_certification) = '' THEN 1 ELSE 0 END) AS missing_age_certification,
                SUM(CASE WHEN seasons IS NULL THEN 1 ELSE 0 END) AS missing_seasons,
                SUM(CASE WHEN imdb_id IS NULL OR TRIM(imdb_id) = '' THEN 1 ELSE 0 END) AS missing_imdb_id,
                SUM(CASE WHEN imdb_score IS NULL THEN 1 ELSE 0 END) AS missing_imdb_score,
                SUM(CASE WHEN imdb_votes IS NULL THEN 1 ELSE 0 END) AS missing_imdb_votes,
                SUM(CASE WHEN tmdb_popularity IS NULL THEN 1 ELSE 0 END) AS missing_tmdb_popularity,
                SUM(CASE WHEN tmdb_score IS NULL THEN 1 ELSE 0 END) AS missing_tmdb_score
            FROM titles;
        """
        cursor.execute(query)
        result = cursor.fetchone()
 
        print("\n=== 15. MISSING VALUES SUMMARY ===")
        print(f"Missing title: {result[0]}")
        print(f"Missing description: {result[1]}")
        print(f"Missing age_certification: {result[2]}")
        print(f"Missing seasons (expected for movies): {result[3]}")
        print(f"Missing imdb_id: {result[4]}")
        print(f"Missing imdb_score: {result[5]}")
        print(f"Missing imdb_votes: {result[6]}")
        print(f"Missing tmdb_popularity: {result[7]}")
        print(f"Missing tmdb_score: {result[8]}")
    finally:
        cursor.close()
        connection.close()
 
 
# ============================================================
# 16. MOVIE AND SHOW PERCENTAGE
# ============================================================
 
def content_percentage_detailed():
    connection = create_connection()
    cursor = connection.cursor()
 
    try:
        query = """
            SELECT
                type,
                COUNT(*) AS total,
                ROUND((COUNT(*) * 100.0) / (SELECT COUNT(*) FROM titles), 2) AS percentage
            FROM titles
            GROUP BY type;
        """
        cursor.execute(query)
        results = cursor.fetchall()
 
        print("\n=== 16. MOVIE AND SHOW PERCENTAGE ===")
        for row in results:
            print(f"{row[0]}: Count={row[1]} | Percentage={row[2]}%")
    finally:
        cursor.close()
        connection.close()
 
 
# ============================================================
# 17. YEARLY CONTENT TREND
# ============================================================
 
def yearly_content_trend():
    connection = create_connection()
    cursor = connection.cursor()
 
    try:
        query = """
            SELECT
                release_year,
                SUM(CASE WHEN type = 'MOVIE' THEN 1 ELSE 0 END) AS movie_count,
                SUM(CASE WHEN type = 'SHOW' THEN 1 ELSE 0 END) AS show_count,
                COUNT(*) AS total_content
            FROM titles
            WHERE release_year IS NOT NULL
            GROUP BY release_year
            ORDER BY release_year ASC;
        """
        cursor.execute(query)
        results = cursor.fetchall()
 
        print("\n=== 17. YEARLY CONTENT TREND ===")
        for row in results:
            print(f"{row[0]}: Movies={row[1]} | Shows={row[2]} | Total={row[3]}")
    finally:
        cursor.close()
        connection.close()
 
 
# ============================================================
# 18. AVERAGE TMDB SCORE BY TYPE
# ============================================================
 
def average_tmdb_by_type():
    connection = create_connection()
    cursor = connection.cursor()
 
    try:
        query = """
            SELECT type, ROUND(AVG(tmdb_score), 2) AS avg_tmdb_score
            FROM titles
            WHERE tmdb_score IS NOT NULL
            GROUP BY type;
        """
        cursor.execute(query)
        results = cursor.fetchall()
 
        print("\n=== 18. AVERAGE TMDB SCORE BY TYPE ===")
        for row in results:
            print(f"{row[0]}: {row[1]}")
    finally:
        cursor.close()
        connection.close()
 
 
# ============================================================
# 19. TOP 10 HIGHEST RATED MOVIES (WEIGHTED RATING)
# ============================================================
# Uses a Bayesian weighted rating (same idea IMDb itself uses) so that
# titles with very few votes don't outrank titles with a lower score
# but far more votes. m = minimum votes to be treated as "reliable";
# C = the overall average IMDb score across all titles.
 
def top_rated_movies():
    connection = create_connection()
    cursor = connection.cursor()
 
    try:
        m = 1000  # minimum votes threshold — adjust as needed
 
        query = """
            SELECT
                title,
                release_year,
                imdb_score,
                imdb_votes,
                ROUND(
                    (imdb_votes / (imdb_votes + %s)) * imdb_score +
                    (%s / (imdb_votes + %s)) *
                        (SELECT AVG(imdb_score) FROM titles WHERE imdb_score IS NOT NULL),
                    2
                ) AS weighted_score
            FROM titles
            WHERE type = 'MOVIE'
              AND imdb_score IS NOT NULL
              AND imdb_votes IS NOT NULL
            ORDER BY weighted_score DESC
            LIMIT 10;
        """
        cursor.execute(query, (m, m, m))
        results = cursor.fetchall()
 
        print("\n=== 19. TOP 10 HIGHEST RATED MOVIES (WEIGHTED) ===")
        for row in results:
            print(f"{row[0]} | {row[1]} | Raw IMDb: {row[2]} | Votes: {row[3]} | Weighted: {row[4]}")
    finally:
        cursor.close()
        connection.close()
 
 
# ============================================================
# 20. TOP 10 HIGHEST RATED SHOWS (WEIGHTED RATING)
# ============================================================
 
def top_rated_shows():
    connection = create_connection()
    cursor = connection.cursor()
 
    try:
        m = 1000  # minimum votes threshold — adjust as needed
 
        query = """
            SELECT
                title,
                release_year,
                seasons,
                imdb_score,
                imdb_votes,
                ROUND(
                    (imdb_votes / (imdb_votes + %s)) * imdb_score +
                    (%s / (imdb_votes + %s)) *
                        (SELECT AVG(imdb_score) FROM titles WHERE imdb_score IS NOT NULL),
                    2
                ) AS weighted_score
            FROM titles
            WHERE type = 'SHOW'
              AND imdb_score IS NOT NULL
              AND imdb_votes IS NOT NULL
            ORDER BY weighted_score DESC
            LIMIT 10;
        """
        cursor.execute(query, (m, m, m))
        results = cursor.fetchall()
 
        print("\n=== 20. TOP 10 HIGHEST RATED SHOWS (WEIGHTED) ===")
        for row in results:
            print(f"{row[0]} | {row[1]} | Seasons: {row[2]} | Raw IMDb: {row[3]} | Votes: {row[4]} | Weighted: {row[5]}")
    finally:
        cursor.close()
        connection.close()
 
 
# ============================================================
# 21. TOP 10 SHOWS BY NUMBER OF SEASONS
# ============================================================
 
def top_shows_by_seasons():
    connection = create_connection()
    cursor = connection.cursor()
 
    try:
        query = """
            SELECT title, release_year, seasons, imdb_score
            FROM titles
            WHERE type = 'SHOW' AND seasons IS NOT NULL
            ORDER BY seasons DESC
            LIMIT 10;
        """
        cursor.execute(query)
        results = cursor.fetchall()
 
        print("\n=== 21. TOP 10 SHOWS BY NUMBER OF SEASONS ===")
        for row in results:
            print(f"{row[0]} | {row[1]} | Seasons: {row[2]} | IMDb Score: {row[3]}")
    finally:
        cursor.close()
        connection.close()
 
 
# ============================================================
# 22. TOP 10 LONGEST MOVIES
# ============================================================
 
def top_longest_movies():
    connection = create_connection()
    cursor = connection.cursor()
 
    try:
        query = """
            SELECT title, release_year, runtime, imdb_score
            FROM titles
            WHERE type = 'MOVIE' AND runtime IS NOT NULL
            ORDER BY runtime DESC
            LIMIT 10;
        """
        cursor.execute(query)
        results = cursor.fetchall()
 
        print("\n=== 22. TOP 10 LONGEST MOVIES ===")
        for row in results:
            print(f"{row[0]} | {row[1]} | Runtime: {row[2]} min | IMDb Score: {row[3]}")
    finally:
        cursor.close()
        connection.close()
 
 
# ============================================================
# 23. CONTENT BY RELEASE DECADE
# ============================================================
 
def content_by_decade():
    connection = create_connection()
    cursor = connection.cursor()
 
    try:
        query = """
            SELECT
                FLOOR(release_year / 10) * 10 AS decade,
                COUNT(*) AS total_content,
                SUM(CASE WHEN type = 'MOVIE' THEN 1 ELSE 0 END) AS movie_count,
                SUM(CASE WHEN type = 'SHOW' THEN 1 ELSE 0 END) AS show_count
            FROM titles
            WHERE release_year IS NOT NULL
            GROUP BY decade
            ORDER BY decade ASC;
        """
        cursor.execute(query)
        results = cursor.fetchall()
 
        print("\n=== 23. CONTENT BY RELEASE DECADE ===")
        for row in results:
            print(f"{int(row[0])}s: Total={row[1]} | Movies={row[2]} | Shows={row[3]}")
    finally:
        cursor.close()
        connection.close()
 
 
# ============================================================
# 24. TOP 10 GENRES BY CONTENT COUNT
# ============================================================
# NOTE / LIMITATION:
# The `genres` column stores multiple genres in a single TEXT value.
# This is NOT a normalized column, so this query uses a recursive
# CTE to split on commas at query time. Requires MySQL 8.0+.
# This is a query-time workaround, not a substitute for properly
# normalizing genres into their own table (title_id, genre).
 
def top_genres():
    connection = create_connection()
    cursor = connection.cursor()
 
    try:
        query = """
            WITH RECURSIVE genre_split AS (
                SELECT
                    id,
                    TRIM(BOTH '\\'' FROM TRIM(SUBSTRING_INDEX(
                        REPLACE(REPLACE(genres, '[', ''), ']', ''), ',', 1
                    ))) AS genre,
                    TRIM(SUBSTRING(
                        REPLACE(REPLACE(genres, '[', ''), ']', ''),
                        LENGTH(SUBSTRING_INDEX(
                            REPLACE(REPLACE(genres, '[', ''), ']', ''), ',', 1
                        )) + 2
                    )) AS remaining
                FROM titles
                WHERE genres IS NOT NULL AND genres != ''
 
                UNION ALL
 
                SELECT
                    id,
                    TRIM(BOTH '\\'' FROM TRIM(SUBSTRING_INDEX(remaining, ',', 1))) AS genre,
                    TRIM(SUBSTRING(remaining, LENGTH(SUBSTRING_INDEX(remaining, ',', 1)) + 2)) AS remaining
                FROM genre_split
                WHERE remaining != ''
            )
            SELECT genre, COUNT(DISTINCT id) AS total_titles
            FROM genre_split
            WHERE genre IS NOT NULL AND genre != ''
            GROUP BY genre
            ORDER BY total_titles DESC
            LIMIT 10;
        """
        cursor.execute(query)
        results = cursor.fetchall()
 
        print("\n=== 24. TOP 10 GENRES BY CONTENT COUNT ===")
        for row in results:
            print(f"{row[0]}: {row[1]} titles")
    finally:
        cursor.close()
        connection.close()
 
 
# ============================================================
# 25. AVERAGE IMDb SCORE BY RELEASE YEAR
# ============================================================
 
def average_imdb_by_year():
    connection = create_connection()
    cursor = connection.cursor()
 
    try:
        query = """
            SELECT
                release_year,
                ROUND(AVG(imdb_score), 2) AS avg_imdb_score,
                COUNT(*) AS rated_titles
            FROM titles
            WHERE imdb_score IS NOT NULL AND release_year IS NOT NULL
            GROUP BY release_year
            ORDER BY release_year ASC;
        """
        cursor.execute(query)
        results = cursor.fetchall()
 
        print("\n=== 25. AVERAGE IMDb SCORE BY RELEASE YEAR ===")
        for row in results:
            print(f"{row[0]}: Avg Score={row[1]} | Rated Titles={row[2]}")
    finally:
        cursor.close()
        connection.close()
 
 
# ============================================================
# 26. TOP 10 MOST POPULAR TITLES (TMDB POPULARITY + IMDb SCORE)
# ============================================================
 
def top_popular_with_rating():
    connection = create_connection()
    cursor = connection.cursor()
 
    try:
        query = """
            SELECT title, type, tmdb_popularity, imdb_score, imdb_votes
            FROM titles
            WHERE tmdb_popularity IS NOT NULL AND imdb_score IS NOT NULL
            ORDER BY tmdb_popularity DESC
            LIMIT 10;
        """
        cursor.execute(query)
        results = cursor.fetchall()
 
        print("\n=== 26. TOP 10 MOST POPULAR TITLES (TMDB + IMDb) ===")
        for row in results:
            print(f"{row[0]} | {row[1]} | Popularity: {row[2]} | IMDb: {row[3]} | Votes: {row[4]}")
    finally:
        cursor.close()
        connection.close()
 
 
# ============================================================
# 27. TOP 10 ACTORS BY NUMBER OF SHOWS
# ============================================================
 
def top_actors_by_shows():
    connection = create_connection()
    cursor = connection.cursor()
 
    try:
        query = """
            SELECT c.name, COUNT(DISTINCT c.id) AS total_shows
            FROM credits c
            JOIN titles t ON c.id = t.id
            WHERE c.role = 'ACTOR' AND t.type = 'SHOW'
            GROUP BY c.name
            ORDER BY total_shows DESC
            LIMIT 10;
        """
        cursor.execute(query)
        results = cursor.fetchall()
 
        print("\n=== 27. TOP 10 ACTORS BY NUMBER OF SHOWS ===")
        for row in results:
            print(f"{row[0]}: {row[1]} shows")
    finally:
        cursor.close()
        connection.close()
 
 
# ============================================================
# 28. TOP 10 DIRECTORS BY NUMBER OF MOVIES
# ============================================================
 
def top_directors_by_movies():
    connection = create_connection()
    cursor = connection.cursor()
 
    try:
        query = """
            SELECT c.name, COUNT(DISTINCT c.id) AS total_movies
            FROM credits c
            JOIN titles t ON c.id = t.id
            WHERE c.role = 'DIRECTOR' AND t.type = 'MOVIE'
            GROUP BY c.name
            ORDER BY total_movies DESC
            LIMIT 10;
        """
        cursor.execute(query)
        results = cursor.fetchall()
 
        print("\n=== 28. TOP 10 DIRECTORS BY NUMBER OF MOVIES ===")
        for row in results:
            print(f"{row[0]}: {row[1]} movies")
    finally:
        cursor.close()
        connection.close()
 
 
# ============================================================
# 29. RATING COMPARISON: IMDb VS TMDB BY TYPE
# ============================================================
 
def rating_comparison_by_type():
    connection = create_connection()
    cursor = connection.cursor()
 
    try:
        query = """
            SELECT
                type,
                ROUND(AVG(imdb_score), 2) AS avg_imdb_score,
                ROUND(AVG(tmdb_score), 2) AS avg_tmdb_score
            FROM titles
            GROUP BY type;
        """
        cursor.execute(query)
        results = cursor.fetchall()
 
        print("\n=== 29. RATING COMPARISON: IMDb VS TMDB BY TYPE ===")
        for row in results:
            print(f"{row[0]}: Avg IMDb={row[1]} | Avg TMDB={row[2]}")
    finally:
        cursor.close()
        connection.close()
 
 
# ============================================================
# 30. CONTENT PERFORMANCE SUMMARY BY TYPE
# ============================================================
 
def content_performance_summary():
    connection = create_connection()
    cursor = connection.cursor()
 
    try:
        query = """
            SELECT
                type,
                COUNT(*) AS total_content,
                ROUND(AVG(imdb_score), 2) AS average_imdb_score,
                ROUND(AVG(tmdb_score), 2) AS average_tmdb_score,
                ROUND(AVG(runtime), 2) AS average_runtime,
                SUM(imdb_votes) AS total_imdb_votes,
                ROUND(AVG(tmdb_popularity), 2) AS average_tmdb_popularity
            FROM titles
            GROUP BY type;
        """
        cursor.execute(query)
        results = cursor.fetchall()
 
        print("\n=== 30. CONTENT PERFORMANCE SUMMARY BY TYPE ===")
        for row in results:
            print(f"{row[0]}:")
            print(f"  Total Content: {row[1]}")
            print(f"  Avg IMDb Score: {row[2]}")
            print(f"  Avg TMDB Score: {row[3]}")
            print(f"  Avg Runtime: {row[4]}")
            print(f"  Total IMDb Votes: {row[5]}")
            print(f"  Avg TMDB Popularity: {row[6]}")
    finally:
        cursor.close()
        connection.close()
 
 
# ============================================================
# 31. ABOVE-AVERAGE RATED TITLES USING CTE
# ============================================================
 
def above_average_titles():
    connection = create_connection()
    cursor = connection.cursor()
 
    try:
        query = """
            WITH overall_avg AS (
                SELECT ROUND(AVG(imdb_score), 2) AS overall_avg_imdb
                FROM titles
                WHERE imdb_score IS NOT NULL
            )
            SELECT
                t.title,
                t.type,
                t.release_year,
                t.imdb_score,
                t.imdb_votes,
                oa.overall_avg_imdb
            FROM titles t
            CROSS JOIN overall_avg oa
            WHERE t.imdb_score IS NOT NULL
              AND t.imdb_score > oa.overall_avg_imdb
            ORDER BY t.imdb_score DESC, t.imdb_votes DESC
            LIMIT 10;
        """
        cursor.execute(query)
        results = cursor.fetchall()
 
        print("\n=== 31. ABOVE-AVERAGE RATED TITLES (CTE) ===")
        for row in results:
            print(f"{row[0]} | {row[1]} | {row[2]} | IMDb: {row[3]} | Votes: {row[4]} | Overall Avg: {row[5]}")
    finally:
        cursor.close()
        connection.close()
 
 
# ============================================================
# 32. RANK TITLES WITHIN MOVIE AND SHOW CATEGORIES
# ============================================================
 
def rank_titles_by_type():
    connection = create_connection()
    cursor = connection.cursor()
 
    try:
        query = """
            WITH ranked_titles AS (
                SELECT
                    title,
                    type,
                    release_year,
                    imdb_score,
                    imdb_votes,
                    RANK() OVER (
                        PARTITION BY type
                        ORDER BY imdb_score DESC
                    ) AS rating_rank
                FROM titles
                WHERE imdb_score IS NOT NULL
            )
            SELECT
                title,
                type,
                release_year,
                imdb_score,
                imdb_votes,
                rating_rank
            FROM ranked_titles
            WHERE rating_rank <= 10
            ORDER BY type, rating_rank;
        """
        cursor.execute(query)
        results = cursor.fetchall()
 
        print("\n=== 32. RANK TITLES WITHIN MOVIE AND SHOW CATEGORIES ===")
        for row in results:
            print(f"[{row[1]}] Rank {row[5]}: {row[0]} | {row[2]} | IMDb: {row[3]} | Votes: {row[4]}")
    finally:
        cursor.close()
        connection.close()
 
 
# ============================================================
# 33. ACTOR PERFORMANCE ANALYSIS
# ============================================================
 
def actor_performance_analysis():
    connection = create_connection()
    cursor = connection.cursor()
 
    try:
        query = """
            SELECT
                c.name AS actor_name,
                COUNT(DISTINCT t.id) AS title_count,
                ROUND(AVG(t.imdb_score), 2) AS average_imdb_score,
                SUM(t.imdb_votes) AS total_imdb_votes
            FROM credits c
            INNER JOIN titles t ON c.id = t.id
            WHERE c.role = 'ACTOR'
            GROUP BY c.name
            ORDER BY title_count DESC
            LIMIT 10;
        """
        cursor.execute(query)
        results = cursor.fetchall()
 
        print("\n=== 33. ACTOR PERFORMANCE ANALYSIS ===")
        for row in results:
            print(f"{row[0]}: Titles={row[1]} | Avg IMDb={row[2]} | Total Votes={row[3]}")
    finally:
        cursor.close()
        connection.close()
 
 
# ============================================================
# 34. DIRECTOR PERFORMANCE ANALYSIS
# ============================================================
 
def director_performance_analysis():
    connection = create_connection()
    cursor = connection.cursor()
 
    try:
        query = """
            SELECT
                c.name AS director_name,
                COUNT(DISTINCT t.id) AS movie_count,
                ROUND(AVG(t.imdb_score), 2) AS average_imdb_score,
                ROUND(AVG(t.runtime), 2) AS average_runtime,
                SUM(t.imdb_votes) AS total_imdb_votes
            FROM credits c
            INNER JOIN titles t ON c.id = t.id
            WHERE c.role = 'DIRECTOR'
              AND t.type = 'MOVIE'
            GROUP BY c.name
            HAVING COUNT(DISTINCT t.id) > 0
            ORDER BY movie_count DESC
            LIMIT 10;
        """
        cursor.execute(query)
        results = cursor.fetchall()
 
        print("\n=== 34. DIRECTOR PERFORMANCE ANALYSIS ===")
        for row in results:
            print(f"{row[0]}: Movies={row[1]} | Avg IMDb={row[2]} | Avg Runtime={row[3]} | Total Votes={row[4]}")
    finally:
        cursor.close()
        connection.close()
 
 
# ============================================================
# 35. YEAR-OVER-YEAR CONTENT GROWTH
# ============================================================
 
def year_over_year_growth():
    connection = create_connection()
    cursor = connection.cursor()
 
    try:
        query = """
            WITH yearly_content AS (
                SELECT
                    release_year,
                    COUNT(*) AS current_year_content
                FROM titles
                WHERE release_year IS NOT NULL
                GROUP BY release_year
            ),
            yearly_with_lag AS (
                SELECT
                    release_year,
                    current_year_content,
                    LAG(current_year_content) OVER (ORDER BY release_year) AS previous_year_content
                FROM yearly_content
            )
            SELECT
                release_year,
                current_year_content,
                previous_year_content,
                (current_year_content - previous_year_content) AS content_difference,
                ROUND(
                    (current_year_content - previous_year_content) * 100.0
                    / NULLIF(previous_year_content, 0),
                    2
                ) AS growth_percentage
            FROM yearly_with_lag
            ORDER BY release_year ASC;
        """
        cursor.execute(query)
        results = cursor.fetchall()
 
        print("\n=== 35. YEAR-OVER-YEAR CONTENT GROWTH ===")
        for row in results:
            print(f"{row[0]}: Current={row[1]} | Previous={row[2]} | Diff={row[3]} | Growth={row[4]}%")
    finally:
        cursor.close()
        connection.close()
 
 
# ============================================================
# 36. THREE-YEAR ROLLING CONTENT AVERAGE
# ============================================================
 
def rolling_content_average():
    connection = create_connection()
    cursor = connection.cursor()
 
    try:
        query = """
            WITH yearly_content AS (
                SELECT
                    release_year,
                    COUNT(*) AS annual_content
                FROM titles
                WHERE release_year IS NOT NULL
                GROUP BY release_year
            )
            SELECT
                release_year,
                annual_content,
                ROUND(
                    AVG(annual_content) OVER (
                        ORDER BY release_year
                        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
                    ),
                    2
                ) AS three_year_rolling_average
            FROM yearly_content
            ORDER BY release_year ASC;
        """
        cursor.execute(query)
        results = cursor.fetchall()
 
        print("\n=== 36. THREE-YEAR ROLLING CONTENT AVERAGE ===")
        for row in results:
            print(f"{row[0]}: Annual={row[1]} | 3-Yr Rolling Avg={row[2]}")
    finally:
        cursor.close()
        connection.close()
 
 
# ============================================================
# 37. CONTENT AND RATING PERFORMANCE BY DECADE
# ============================================================
# FIX: The previous version grouped by FLOOR(release_year / 10)
# while selecting FLOOR(release_year / 10) * 10 — a mismatched
# expression that MySQL's ONLY_FULL_GROUP_BY does not reliably
# treat as functionally dependent, causing error 1055. This
# version computes the decade once in a CTE (decade_num) and then
# groups/selects that exact same column, removing any ambiguity.
 
def performance_by_decade():
    connection = create_connection()
    cursor = connection.cursor()
 
    try:
        query = """
            WITH decade_calc AS (
                SELECT
                    FLOOR(release_year / 10) * 10 AS decade_num,
                    imdb_score,
                    tmdb_score,
                    runtime
                FROM titles
                WHERE release_year IS NOT NULL
            )
            SELECT
                CONCAT(decade_num, 's') AS decade,
                COUNT(*) AS content_count,
                ROUND(AVG(imdb_score), 2) AS average_imdb_score,
                ROUND(AVG(tmdb_score), 2) AS average_tmdb_score,
                ROUND(AVG(runtime), 2) AS average_runtime
            FROM decade_calc
            GROUP BY decade_num
            ORDER BY decade_num ASC;
        """
        cursor.execute(query)
        results = cursor.fetchall()
 
        print("\n=== 37. CONTENT AND RATING PERFORMANCE BY DECADE ===")
        for row in results:
            print(f"{row[0]}: Count={row[1]} | Avg IMDb={row[2]} | Avg TMDB={row[3]} | Avg Runtime={row[4]}")
    finally:
        cursor.close()
        connection.close()
 
 
# ============================================================
# 38. ANALYTICAL CONTENT POPULARITY SCORE (REVISED)
# ============================================================
# METHODOLOGY:
# This is a PROJECT-SPECIFIC ANALYTICAL SCORE, NOT an official
# Netflix, IMDb, or TMDB score/ranking.
#
# Weighting:
#   IMDb Score       = 35%
#   TMDB Score       = 25%
#   IMDb Votes       = 25%  (log-scaled, then min-max normalized)
#   TMDB Popularity  = 15%  (min-max normalized)
#
# Only titles with all four required inputs present are scored.
 
def content_popularity_score():
    connection = create_connection()
    cursor = connection.cursor()
 
    try:
        query = """
            WITH base_data AS (
                -- Step 1: Restrict to titles where every required metric
                -- is present. A title missing any of the four inputs
                -- cannot be fairly scored, so it is excluded rather than
                -- imputed.
                SELECT
                    title,
                    type,
                    release_year,
                    imdb_score,
                    imdb_votes,
                    tmdb_score,
                    tmdb_popularity,
                    -- Log-scale IMDb votes so a handful of extremely
                    -- high-vote outliers don't dominate the normalization
                    -- range. +1 avoids LOG10(0), which is undefined.
                    LOG10(imdb_votes + 1) AS log_imdb_votes
                FROM titles
                WHERE imdb_score IS NOT NULL
                  AND imdb_votes IS NOT NULL
                  AND tmdb_score IS NOT NULL
                  AND tmdb_popularity IS NOT NULL
            ),
 
            bounds AS (
                -- Step 2: Capture the min/max of the two metrics that
                -- need min-max normalization (log-scaled votes and raw
                -- popularity). IMDb/TMDB scores don't need this step:
                -- they're already on a fixed, known 0-10 scale, so
                -- they're rescaled directly (x10) in the next step
                -- rather than relative to the dataset.
                SELECT
                    MIN(log_imdb_votes)    AS min_log_votes,
                    MAX(log_imdb_votes)    AS max_log_votes,
                    MIN(tmdb_popularity)   AS min_popularity,
                    MAX(tmdb_popularity)   AS max_popularity
                FROM base_data
            ),
 
            normalized AS (
                -- Step 3: Normalize every metric onto a common 0-100
                -- scale.
                SELECT
                    b.title,
                    b.type,
                    b.release_year,
                    b.imdb_score,
                    b.imdb_votes,
                    b.tmdb_score,
                    b.tmdb_popularity,
 
                    -- IMDb score: fixed 0-10 scale -> 0-100 by direct
                    -- rescale.
                    (b.imdb_score * 10) AS normalized_imdb_score,
 
                    -- TMDB score: fixed 0-10 scale -> 0-100 by direct
                    -- rescale.
                    (b.tmdb_score * 10) AS normalized_tmdb_score,
 
                    -- IMDb votes: min-max normalize the LOG-SCALED vote
                    -- value. NULLIF guards against a divide-by-zero if
                    -- every title in the filtered set happened to have
                    -- an identical vote count (min = max). In that edge
                    -- case the normalized value is NULL rather than
                    -- causing an error.
                    (
                        (b.log_imdb_votes - bd.min_log_votes)
                        / NULLIF(bd.max_log_votes - bd.min_log_votes, 0)
                    ) * 100 AS normalized_imdb_votes,
 
                    -- TMDB popularity: straightforward min-max
                    -- normalization. Same divide-by-zero guard as above.
                    (
                        (b.tmdb_popularity - bd.min_popularity)
                        / NULLIF(bd.max_popularity - bd.min_popularity, 0)
                    ) * 100 AS normalized_tmdb_popularity
                FROM base_data b
                CROSS JOIN bounds bd
            ),
 
            scored AS (
                -- Step 4: Combine the four normalized metrics using the
                -- specified weights. Each component is already 0-100,
                -- so the weighted sum stays on a 0-100 scale.
                SELECT
                    title,
                    type,
                    release_year,
                    imdb_score,
                    imdb_votes,
                    tmdb_score,
                    tmdb_popularity,
                    (
                        (normalized_imdb_score       * 0.35) +
                        (normalized_tmdb_score       * 0.25) +
                        (normalized_imdb_votes       * 0.25) +
                        (normalized_tmdb_popularity  * 0.15)
                    ) AS analytical_score
                FROM normalized
                -- Only rank titles where every normalized component
                -- actually resolved to a real number (guards against
                -- the NULLIF edge case above silently producing a NULL
                -- score).
                WHERE normalized_imdb_votes IS NOT NULL
                  AND normalized_tmdb_popularity IS NOT NULL
            )
 
            -- Step 5: Final projection, rounded and sorted.
            SELECT
                title,
                type,
                release_year,
                imdb_score,
                imdb_votes,
                tmdb_score,
                tmdb_popularity,
                ROUND(analytical_score, 2) AS analytical_score
            FROM scored
            ORDER BY analytical_score DESC
            LIMIT 10;
        """
        cursor.execute(query)
        results = cursor.fetchall()
 
        print("\n=== 38. ANALYTICAL CONTENT POPULARITY SCORE (project-specific, not official) ===")
        for row in results:
            print(f"{row[0]} | {row[1]} | {row[2]} | IMDb={row[3]} | Votes={row[4]} | TMDB={row[5]} | Pop={row[6]} | Score={row[7]}")
    finally:
        cursor.close()
        connection.close()
 
# ============================================================
# 39. GENRE PERFORMANCE ANALYSIS
# ============================================================
# Same recursive-CTE genre-splitting technique as #24 (requires
# MySQL 8.0+), extended here to also compute rating/runtime
# performance per individual genre, not just a count.
 
def genre_performance_analysis():
    connection = create_connection()
    cursor = connection.cursor()
 
    try:
        query = """
            WITH RECURSIVE genre_split AS (
                SELECT
                    id,
                    imdb_score,
                    tmdb_score,
                    runtime,
                    TRIM(BOTH '\\'' FROM TRIM(SUBSTRING_INDEX(
                        REPLACE(REPLACE(genres, '[', ''), ']', ''), ',', 1
                    ))) AS genre,
                    TRIM(SUBSTRING(
                        REPLACE(REPLACE(genres, '[', ''), ']', ''),
                        LENGTH(SUBSTRING_INDEX(
                            REPLACE(REPLACE(genres, '[', ''), ']', ''), ',', 1
                        )) + 2
                    )) AS remaining
                FROM titles
                WHERE genres IS NOT NULL AND genres != ''
 
                UNION ALL
 
                SELECT
                    id,
                    imdb_score,
                    tmdb_score,
                    runtime,
                    TRIM(BOTH '\\'' FROM TRIM(SUBSTRING_INDEX(remaining, ',', 1))) AS genre,
                    TRIM(SUBSTRING(remaining, LENGTH(SUBSTRING_INDEX(remaining, ',', 1)) + 2)) AS remaining
                FROM genre_split
                WHERE remaining != ''
            )
            SELECT
                genre,
                COUNT(DISTINCT id) AS title_count,
                ROUND(AVG(imdb_score), 2) AS average_imdb_score,
                ROUND(AVG(tmdb_score), 2) AS average_tmdb_score,
                ROUND(AVG(runtime), 2) AS average_runtime
            FROM genre_split
            WHERE genre IS NOT NULL AND genre != ''
            GROUP BY genre
            ORDER BY title_count DESC
            LIMIT 10;
        """
        cursor.execute(query)
        results = cursor.fetchall()
 
        print("\n=== 39. GENRE PERFORMANCE ANALYSIS ===")
        for row in results:
            print(f"{row[0]}: Titles={row[1]} | Avg IMDb={row[2]} | Avg TMDB={row[3]} | Avg Runtime={row[4]}")
    finally:
        cursor.close()
        connection.close()
 
 
# ============================================================
# 40. FINAL NETFLIX CONTENT PERFORMANCE RANKING
# ============================================================
# METHODOLOGY:
# This is a PROJECT-SPECIFIC ANALYTICAL PERFORMANCE SCORE, NOT an
# official Netflix metric. Reuses the same min-max normalization
# as #38 (each metric rescaled to 0-1, weighted equally at 25%),
# then applies RANK() to produce the final ranking, correctly
# handling tied scores by giving them the same rank.
 
def final_performance_ranking():
    connection = create_connection()
    cursor = connection.cursor()
 
    try:
        query = """
            WITH metric_bounds AS (
                SELECT
                    MIN(imdb_score) AS min_imdb_score, MAX(imdb_score) AS max_imdb_score,
                    MIN(imdb_votes) AS min_imdb_votes, MAX(imdb_votes) AS max_imdb_votes,
                    MIN(tmdb_score) AS min_tmdb_score, MAX(tmdb_score) AS max_tmdb_score,
                    MIN(tmdb_popularity) AS min_tmdb_pop, MAX(tmdb_popularity) AS max_tmdb_pop
                FROM titles
                WHERE imdb_score IS NOT NULL
                  AND imdb_votes IS NOT NULL
                  AND tmdb_score IS NOT NULL
                  AND tmdb_popularity IS NOT NULL
            ),
            scored_titles AS (
                SELECT
                    t.title,
                    t.type,
                    t.release_year,
                    t.imdb_score,
                    t.imdb_votes,
                    t.tmdb_score,
                    t.tmdb_popularity,
                    (
                        ((t.imdb_score - b.min_imdb_score) / NULLIF(b.max_imdb_score - b.min_imdb_score, 0)) * 0.25 +
                        ((t.imdb_votes - b.min_imdb_votes) / NULLIF(b.max_imdb_votes - b.min_imdb_votes, 0)) * 0.25 +
                        ((t.tmdb_score - b.min_tmdb_score) / NULLIF(b.max_tmdb_score - b.min_tmdb_score, 0)) * 0.25 +
                        ((t.tmdb_popularity - b.min_tmdb_pop) / NULLIF(b.max_tmdb_pop - b.min_tmdb_pop, 0)) * 0.25
                    ) * 100 AS performance_score
                FROM titles t
                CROSS JOIN metric_bounds b
                WHERE t.imdb_score IS NOT NULL
                  AND t.imdb_votes IS NOT NULL
                  AND t.tmdb_score IS NOT NULL
                  AND t.tmdb_popularity IS NOT NULL
            ),
            ranked_final AS (
                SELECT
                    RANK() OVER (ORDER BY performance_score DESC) AS content_rank,
                    title,
                    type,
                    release_year,
                    imdb_score,
                    imdb_votes,
                    tmdb_score,
                    tmdb_popularity,
                    ROUND(performance_score, 2) AS performance_score
                FROM scored_titles
            )
            SELECT *
            FROM ranked_final
            ORDER BY content_rank
            LIMIT 20;
        """
        cursor.execute(query)
        results = cursor.fetchall()
 
        print("\n=== 40. FINAL NETFLIX CONTENT PERFORMANCE RANKING (project-specific, not official) ===")
        for row in results:
            print(f"Rank {row[0]}: {row[1]} | {row[2]} | {row[3]} | IMDb={row[4]} | Votes={row[5]} | TMDB={row[6]} | Pop={row[7]} | Score={row[8]}")
    finally:
        cursor.close()
        connection.close()
 
 
# ============================================================
# MAIN EXECUTION BLOCK
# ============================================================
 
if __name__ == "__main__":
    total_content()
    content_by_type()
    data_quality_audit()
    content_by_year()
    average_imdb_score()
    top_rated_titles()
    top_voted_titles()
    average_imdb_by_type()
    top_years_by_content()
    top_tmdb_popularity()
    top_actors()
    top_directors()
    runtime_summary_by_type()
    content_quality_summary()
    missing_values_summary()
    content_percentage_detailed()
    yearly_content_trend()
    average_tmdb_by_type()
    top_rated_movies()
    top_rated_shows()
    top_shows_by_seasons()
    top_longest_movies()
    content_by_decade()
    top_genres()
    average_imdb_by_year()
    top_popular_with_rating()
    top_actors_by_shows()
    top_directors_by_movies()
    rating_comparison_by_type()
    content_performance_summary()
    above_average_titles()
    rank_titles_by_type()
    actor_performance_analysis()
    director_performance_analysis()
    year_over_year_growth()
    rolling_content_average()
    performance_by_decade()
    content_popularity_score()
    genre_performance_analysis()
    final_performance_ranking()