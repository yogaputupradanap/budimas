import psycopg2
import bcrypt


def update_passwords():
    # Database connection parameters
    db_params = {
        "database": "postgres",
        "user": "postgres",
        "password": "HorusBudimas",
        "host": "34.101.94.218",
        "port": "5432"
    }

    try:
        # Connect to database
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()

        # Get all user IDs
        cur.execute("SELECT id FROM users")
        user_ids = cur.fetchall()

        # Update each user with a unique salt
        password = "test"
        for user_id in user_ids:
            # Generate new salt and hash for each user
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

            # Update individual user
            update_query = "UPDATE users SET password = %s WHERE id = %s"
            cur.execute(update_query, (hashed_password.decode('utf-8'), user_id[0]))

        # Commit and close
        conn.commit()
        print(f"Successfully updated {len(user_ids)} user passwords to 'test' with unique hashes")

    except Exception as e:
        print(f"Error updating passwords: {str(e)}")
        conn.rollback()
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


if __name__ == "__main__":
    update_passwords()