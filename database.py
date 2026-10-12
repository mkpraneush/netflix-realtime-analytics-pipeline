import mysql.connector
import config


def create_connection():
    connection = mysql.connector.connect(
        host=config.DB_HOST,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        database=config.DB_NAME
    )

    print("MySQL connection successful!")

    return connection


# ==========================================
# VERIFY MYSQL DATA
# ==========================================

def verify_database():

    connection = create_connection()
    cursor = connection.cursor()

    print("\n==========================================")
    print("MYSQL DATA VERIFICATION")
    print("==========================================")

    # --------------------------------------
    # 1. TITLES ROW COUNT
    # --------------------------------------

    cursor.execute("SELECT COUNT(*) FROM titles")

    titles_count = cursor.fetchone()[0]

    print("\n1. Titles row count:", titles_count)


    # --------------------------------------
    # 2. CREDITS ROW COUNT
    # --------------------------------------

    cursor.execute("SELECT COUNT(*) FROM credits")

    credits_count = cursor.fetchone()[0]

    print("2. Credits row count:", credits_count)


    # --------------------------------------
    # 3. DUPLICATE TITLE IDs
    # --------------------------------------

    cursor.execute("""
        SELECT id, COUNT(*)
        FROM titles
        GROUP BY id
        HAVING COUNT(*) > 1
    """)

    duplicate_titles = cursor.fetchall()

    print("\n3. Duplicate title IDs:", len(duplicate_titles))


    # --------------------------------------
    # 4. ORPHAN CREDITS
    # --------------------------------------

    cursor.execute("""
        SELECT COUNT(*)
        FROM credits c
        LEFT JOIN titles t
            ON c.id = t.id
        WHERE t.id IS NULL
    """)

    orphan_credits = cursor.fetchone()[0]

    print("4. Orphan credits:", orphan_credits)


    # --------------------------------------
    # 5. IMPORTANT NULL CHECKS
    # --------------------------------------

    cursor.execute("""
        SELECT COUNT(*)
        FROM titles
        WHERE id IS NULL
    """)

    null_title_id = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM credits
        WHERE person_id IS NULL
    """)

    null_person_id = cursor.fetchone()[0]

    print("\n5. NULL primary keys:")
    print("Title ID NULL:", null_title_id)
    print("Credit person ID NULL:", null_person_id)


    # --------------------------------------
    # 6. SAMPLE TITLES
    # --------------------------------------

    cursor.execute("""
        SELECT id, title, type, release_year
        FROM titles
        LIMIT 5
    """)

    print("\n6. Sample titles:")

    for row in cursor.fetchall():
        print(row)


    # --------------------------------------
    # 7. SAMPLE CREDITS
    # --------------------------------------

    cursor.execute("""
        SELECT person_id, id, name, `character`, role
        FROM credits
        LIMIT 5
    """)

    print("\n7. Sample credits:")

    for row in cursor.fetchall():
        print(row)


    # --------------------------------------
    # FINAL RESULT
    # --------------------------------------

    print("\n==========================================")
    print("VERIFICATION RESULT")
    print("==========================================")

    if (
        titles_count == 5850
        and credits_count == 77713
        and len(duplicate_titles) == 0
        and orphan_credits == 0
        and null_title_id == 0
        and null_person_id == 0
    ):
        print("SUCCESS - MySQL data verification passed!")
    else:
        print("WARNING - Some checks need review.")


    cursor.close()
    connection.close()

    print("\nMySQL connection closed.")


# ==========================================
# RUN
# ==========================================

if __name__ == "__main__":
    verify_database()