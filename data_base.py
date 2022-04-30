import sqlite3
from contextlib import closing
from datetime import date

from config import config


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


def check_exist_word(word: str) -> bool:
    with closing(sqlite3.connect("db/english.db")) as connection:
        with closing(connection.cursor()) as cursor:
            answer = cursor.execute(
                f"""SELECT EXISTS(
               SELECT word, translation, next_shipping_date, number_of_messages
               FROM english
               WHERE word = {word.capitalize()!r} COLLATE NOCASE
                  or translation = {word.capitalize()!r} COLLATE NOCASE
           ) AS exist"""
            ).fetchone()[0]
    if answer == 0:
        return False
    return True


def insert_new_word(word: str, translation: str, next_shipping_date: date):
    with closing(sqlite3.connect("db/english.db")) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute(
                f"""INSERT INTO english (word, translation, next_shipping_date, number_of_messages)
                    VALUES ({word.capitalize()!r}, {translation.capitalize()!r}, {next_shipping_date.strftime(config.date_format)!r}, 0);"""
            )
            connection.commit()


def update_word(word: str, next_shipping_date: date, number_of_messages: int):
    with closing(sqlite3.connect("db/english.db")) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute(
                f"""update english
                    set next_shipping_date = {next_shipping_date.strftime(config.date_format)!r},
                        number_of_messages = {number_of_messages}
                    where word = {word.capitalize()!r} COLLATE NOCASE
                       or translation = {word.capitalize()!r} COLLATE NOCASE;"""
            )
            connection.commit()


def db_delete_word(word: str):
    with closing(sqlite3.connect("db/english.db")) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute(
                f"""DELETE
                    FROM english
                    WHERE word = {word.capitalize()!r} COLLATE NOCASE
                       or translation = {word.capitalize()!r} COLLATE NOCASE;"""
            )
            connection.commit()
