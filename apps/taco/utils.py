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