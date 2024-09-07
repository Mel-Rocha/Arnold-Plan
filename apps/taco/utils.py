import psycopg2
from rest_framework.pagination import PageNumberPagination

from config.settings import DATABASE_RETENTION_CONFIG


def get_retention_db_connection():
    connection = psycopg2.connect(
        dbname=DATABASE_RETENTION_CONFIG["DATABASE_RETENTION"],
        user=DATABASE_RETENTION_CONFIG["PG_USER_RETENTION"],
        password=DATABASE_RETENTION_CONFIG["PG_PASSWORD_RETENTION"],
        host=DATABASE_RETENTION_CONFIG["PG_HOST_RETENTION"],
        port=DATABASE_RETENTION_CONFIG["PG_PORT_RETENTION"],
    )
    return connection


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


def fetch_foods(description=None):
    query = "SELECT * FROM CMVColtaco3"
    params = []
    if description:
        query += " WHERE food_description LIKE %s"
        params.append(f'%{description}%')

    with get_retention_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            rows = cursor.fetchall()
            columns = [col[0] for col in cursor.description]

    foods = [dict(zip(columns, row)) for row in rows]
    return foods