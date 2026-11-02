from database.db import (
    initialize_database,
    test_connection
)


if __name__ == "__main__":

    test_connection()

    initialize_database()