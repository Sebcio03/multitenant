from django.db import connection


def set_schema(schema: str = "public") -> None:
    with connection.cursor() as cursor:
        cursor.execute(f"SET search_path TO {schema};")
