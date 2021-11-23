import MySQLdb


def assign_data(table, row):
    connection = MySQLdb.connect(
        host="localhost",
        user="root",
        password="123456",
        database="shikmanzel",
        charset="utf8mb4",
    )

    try:
        with connection.cursor() as cursor:

            placeholders = ', '.join(['%s'] * len(row))
            columns = ', '.join(row.keys())
            sql = f"INSERT INTO {table} ( {columns} ) VALUES ( {placeholders} )"
            cursor.execute(sql, list(row.values()))
        connection.commit()
        return True

    except MySQLdb.Error as e:
        print(e)
        return False

    finally:
        connection.close()