import psycopg2
from psycopg2 import sql
from utils.db_conn import get_db_connection


def create_tables():
    commands = (
        """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            password_hash VARCHAR(128) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS quizzes (
            id SERIAL PRIMARY KEY,
            title VARCHAR(200) NOT NULL,
            description TEXT,
            creator_id INTEGER REFERENCES users(id),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS questions (
            id SERIAL PRIMARY KEY,
            quiz_id INTEGER REFERENCES quizzes(id),
            question_text TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS answers (
            id SERIAL PRIMARY KEY,
            question_id INTEGER REFERENCES questions(id),
            answer_text TEXT NOT NULL,
            is_correct BOOLEAN NOT NULL DEFAULT FALSE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS responses (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id),
            question_id INTEGER REFERENCES questions(id),
            answer_id INTEGER REFERENCES answers(id),
            responded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        # Create tables
        for command in commands:
            cur.execute(command)
        # Close communication with the PostgreSQL database server
        cur.close()
        # Commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
