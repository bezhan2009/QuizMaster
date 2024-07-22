import psycopg2
from psycopg2 import sql
from utils.db_conn import get_db_connection


def create_tables():
    commands = (
        """
        CREATE SCHEMA IF NOT EXISTS quiz_app;
        """,
        """
        CREATE TABLE IF NOT EXISTS quiz_app.users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            password_hash VARCHAR(256) NOT NULL,
            photo_filename VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS quiz_app.quizzes (
            id SERIAL PRIMARY KEY,
            title VARCHAR(200) NOT NULL,
            description TEXT,
            creator_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (creator_id) REFERENCES quiz_app.users (id) ON DELETE CASCADE
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS quiz_app.questions (
            id SERIAL PRIMARY KEY,
            quiz_id INTEGER NOT NULL,
            question_text TEXT NOT NULL,
            FOREIGN KEY (quiz_id) REFERENCES quiz_app.quizzes (id) ON DELETE CASCADE
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS quiz_app.answers (
            id SERIAL PRIMARY KEY,
            question_id INTEGER NOT NULL,
            answer_text TEXT NOT NULL,
            is_correct BOOLEAN NOT NULL DEFAULT FALSE,
            FOREIGN KEY (question_id) REFERENCES quiz_app.questions (id) ON DELETE CASCADE
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS quiz_app.responses (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL,
            question_id INTEGER NOT NULL,
            answer_id INTEGER NOT NULL,
            responded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES quiz_app.users (id) ON DELETE CASCADE,
            FOREIGN KEY (question_id) REFERENCES quiz_app.questions (id) ON DELETE CASCADE,
            FOREIGN KEY (answer_id) REFERENCES quiz_app.answers (id) ON DELETE CASCADE
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS quiz_app.subjects (
            id SERIAL PRIMARY KEY,
            title VARCHAR(200) NOT NULL,
            description TEXT,
            usage_count INTEGER NOT NULL DEFAULT 0
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS quiz_app.achievements (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL,
            quiz_id INTEGER NOT NULL,
            title VARCHAR(200) NOT NULL,
            description TEXT,
            achieved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES quiz_app.users (id) ON DELETE CASCADE,
            FOREIGN KEY (quiz_id) REFERENCES quiz_app.quizzes (id) ON DELETE CASCADE
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS quiz_app.contacts (
            id SERIAL PRIMARY KEY,
            title VARCHAR(200) NOT NULL
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS quiz_app.user_data (
            user_id INTEGER PRIMARY KEY,
            gender VARCHAR(50) NOT NULL,
            surname VARCHAR(50) NOT NULL,
            name VARCHAR(50) NOT NULL,
            favorite_subject VARCHAR(50) NOT NULL,
            cover_filename VARCHAR(255) NOT NULL,
            achievements TEXT,
            bio TEXT,
            contact_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES quiz_app.users (id) ON DELETE CASCADE,
            FOREIGN KEY (contact_id) REFERENCES quiz_app.contacts (id) ON DELETE SET NULL
        );
        """,
        """
        CREATE INDEX IF NOT EXISTS idx_user_email ON quiz_app.users (email);
        """,
        """
        CREATE INDEX IF NOT EXISTS idx_quiz_creator ON quiz_app.quizzes (creator_id);
        """,
        """
        CREATE INDEX IF NOT EXISTS idx_question_quiz ON quiz_app.questions (quiz_id);
        """,
        """
        CREATE INDEX IF NOT EXISTS idx_answer_question ON quiz_app.answers (question_id);
        """,
        """
        CREATE INDEX IF NOT EXISTS idx_response_user ON quiz_app.responses (user_id);
        """,
        """
        CREATE INDEX IF NOT EXISTS idx_response_question ON quiz_app.responses (question_id);
        """
    )
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        for command in commands:
            cur.execute(command)
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
