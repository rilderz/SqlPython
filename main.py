import sqlite3
from icecream import ic as print


def get_connection(db_name: str):
    try:
        return sqlite3.connect(db_name)
    except Exception as e:
        (f"Error: {e}")
        raise


def create_table(connection):
    query = """
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER,
            email TEXT UNIQUE
        )
    """
    try:
        with connection:
            connection.execute(query)
        print("Table ready")
    except Exception as e:
        print(e)


def insert_user(connection, name: str, age: int, email: str):
    query = "INSERT INTO users (name, age, email) VALUES (?, ?, ?)"
    try:
        with connection:
            connection.execute(query, (name, age, email))
        print(f"User '{name}' added")
    except Exception as e:
        print(e)


def insert_users(connection, users: list[tuple[str, int, str]]):
    query = "INSERT INTO users (name, age, email) VALUES (?, ?, ?)"
    try:
        with connection:
            connection.executemany(query, users)
        print(f"{len(users)} users added")
    except Exception as e:
        print(e)


def delete_user(connection, user_id: int):
    query = "DELETE FROM users WHERE id = ?"
    try:
        with connection:
            connection.execute(query, (user_id,))
        print(f"User {user_id} deleted")
    except Exception as e:
        print(e)


def update_user(connection, user_id: int, email: str):
    query = "UPDATE users SET email = ? WHERE id = ?"
    try:
        with connection:
            connection.execute(query, (email, user_id))
        print(f"User {user_id} updated with new email '{email}'")
    except Exception as e:
        print(e)


def fetch_users(connection):
    query = "SELECT * FROM users"
    try:
        with connection:
            return connection.execute(query).fetchall()
    except Exception as e:
        print(e)
        return []


def main():
    connection = get_connection("subscribe.db")

    try:
        create_table(connection)

        while True:
            print("Options: add | add many | delete | update | search | exit")
            choice = input("Enter option: ").strip().lower()

            if choice == "exit":
                break

            elif choice == "add":
                try:
                    name = input("Name: ")
                    age = int(input("Age: "))
                    email = input("Email: ")
                    insert_user(connection, name, age, email)
                except ValueError:
                    print("Invalid age input")

            elif choice == "add many":
                users = [
                    ("joe", 23, "joe@gmail.com"),
                    ("john", 22, "john@gmail.com"),
                    ("mike", 24, "mike@gmail.com"),
                ]
                insert_users(connection, users)

            elif choice == "delete":
                try:
                    user_id = int(input("User ID: "))
                    delete_user(connection, user_id)
                except ValueError:
                    print("Invalid ID")

            elif choice == "update":
                try:
                    user_id = int(input("User ID: "))
                    email = input("New email: ")
                    update_user(connection, user_id, email)
                except ValueError:
                    print("Invalid ID")

            elif choice == "search":
                users = fetch_users(connection)
                if users:
                    print("\nUsers:")
                    for user in users:
                        print(user)
                else:
                    print("No users found")

            else:
                print("Unknown command")

    finally:
        connection.close()
        print("Connection closed")


if __name__ == "__main__":
    main()
