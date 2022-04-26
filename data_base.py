import sqlite3
from contextlib import closing
from datetime import date


def create_table():
    with closing(sqlite3.connect("db/english.db")) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS english
                    (
                        word               TEXT NOT NULL,
                        translation        TEXT NOT NULL,
                        next_shipping_date         TEXT NOT NULL,
                        number_of_messages INTEGER DEFAULT 0
                    );"""
            )
            connection.commit()


def select_all_rows():
    with closing(sqlite3.connect("db/english.db")) as connection:
        with closing(connection.cursor()) as cursor:
            return cursor.execute(
                """SELECT word, translation, next_shipping_date, number_of_messages
                    FROM english;"""
            ).fetchall()


def insert_new_word(word: str, translation: str, next_shipping_date: date):
    with closing(sqlite3.connect("db/english.db")) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute(
                f"""INSERT INTO english (word, translation, next_shipping_date, number_of_messages)
                    VALUES ({word}, {translation}, {next_shipping_date}, 0);"""
            )


