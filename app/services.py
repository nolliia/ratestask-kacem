import datetime
import json
from typing import List, Tuple, Union
from psycopg2.extensions import connection
from app.utils import (
    create_db_connection,
    is_valid_port_code,
    is_valid_region_slug,
    get_port_codes_for_region,
)


def get_price_averages(
    date_from: str, date_to: str, origin: str, destination: str
) -> Union[str, Tuple[str, int]]:
    if not all([date_from, date_to, origin, destination]):
        return (
            "Error: One or more required parameters (date_from, date_to, origin, destination) are missing.",
            400,
        )

    try:
        start_date = datetime.datetime.strptime(date_from, "%Y-%m-%d").date()
        end_date = datetime.datetime.strptime(date_to, "%Y-%m-%d").date()
    except ValueError:
        return (
            "Error: Invalid date format. Please use YYYY-MM-DD for both date_from and date_to.",
            400,
        )

    if start_date >= end_date:
        return (
            "Error: Invalid date range. The 'date_from' must be earlier than 'date_to'.",
            400,
        )

    if (end_date - start_date).days > 365:
        return "Error: Date range exceeds the maximum allowed period of 365 days.", 400

    connection = create_db_connection()
    if not connection:
        return (
            "Error: Unable to establish a connection to the database. Please try again later.",
            500,
        )

    try:
        origin_port_codes = get_port_codes_helper(origin, connection, "origin")
        destination_port_codes = get_port_codes_helper(
            destination, connection, "destination"
        )

        if origin_port_codes is None and destination_port_codes is None:
            return (
                "Error: Both origin and destination are invalid. Please provide valid port codes or region slugs.",
                400,
            )
        elif origin_port_codes is None:
            return (
                f"Error: Invalid origin '{origin}'. Please provide a valid port code or region slug for the origin.",
                400,
            )
        elif destination_port_codes is None:
            return (
                f"Error: Invalid destination '{destination}'. Please provide a valid port code or region slug for the destination.",
                400,
            )

        prices = fetch_prices(
            start_date, end_date, origin_port_codes, destination_port_codes, connection
        )

        prices_json = [
            {
                "day": row[0].isoformat(),
                "average_price": row[1] if row[1] is not None else None,
            }
            for row in prices
        ]

        return json.dumps(prices_json, sort_keys=False)

    except ValueError as ve:
        return f"Error: {str(ve)}", 400
    except Exception as e:
        return (
            f"An unexpected error occurred: {str(e)}. Please try again or contact support if the problem persists.",
            500,
        )
    finally:
        if connection:
            connection.close()


def get_port_codes_helper(
    location: str, conn: connection, location_type: str
) -> Union[List[str], None]:
    if len(location) <= 5 and location.isupper():
        if not is_valid_port_code(location, conn):
            return None
        return [location]
    else:
        if not is_valid_region_slug(location, conn):
            return None
        codes = get_port_codes_for_region(location, conn)
        return codes if codes else None


def fetch_prices(
    start_date: datetime.date,
    end_date: datetime.date,
    origin_port_codes: List[str],
    destination_port_codes: List[str],
    conn: connection,
) -> List[Tuple[datetime.date, int]]:
    with conn.cursor() as cursor:
        cursor.execute(
            """
            WITH days AS (
                SELECT GENERATE_SERIES(%s::date, %s::date, interval '1 day')::date AS day
            )
            SELECT
                days.day,
                CASE
                    WHEN COUNT(*) >= 3 THEN ROUND(AVG(price))::integer
                    ELSE NULL
                END AS average_price
            FROM
                days
                LEFT JOIN prices ON 
                    days.day = prices.day AND
                    orig_code = ANY(%s) AND
                    dest_code = ANY(%s)
            GROUP BY days.day
            ORDER BY days.day;
            """,
            (start_date, end_date, origin_port_codes, destination_port_codes),
        )
        return cursor.fetchall()
