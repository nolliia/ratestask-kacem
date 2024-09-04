import os
import psycopg2


def create_db_connection():
    try:
        return psycopg2.connect(
            host=os.environ["POSTGRES_DB_HOST"],
            database=os.environ["POSTGRES_DB_NAME"],
            user=os.environ["POSTGRES_USERNAME"],
            password=os.environ["POSTGRES_PASSWORD"],
        )
    except psycopg2.Error as error:
        print(f"Error connecting to the database: {error}")
        return None


def is_valid_port_code(port_code, connection):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT EXISTS(SELECT 1 FROM ports WHERE code = %s);", (port_code,)
        )
        exists = cursor.fetchone()[0]
        return exists


def is_valid_region_slug(slug, connection):
    with connection.cursor() as cursor:
        cursor.execute("SELECT EXISTS(SELECT 1 FROM regions WHERE slug = %s);", (slug,))
        exists = cursor.fetchone()[0]
        return exists


def get_port_codes_for_region(region_slug, connection):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            WITH RECURSIVE region_tree AS (
                SELECT slug, parent_slug
                FROM regions
                WHERE slug = %s

                UNION ALL

                SELECT regions.slug, regions.parent_slug
                FROM regions
                JOIN region_tree ON regions.parent_slug = region_tree.slug
            )
            SELECT ports.code
            FROM ports 
            INNER JOIN region_tree ON ports.parent_slug = region_tree.slug;
            """,
            (region_slug,),
        )
        port_codes = [row[0] for row in cursor.fetchall()]
        return port_codes
