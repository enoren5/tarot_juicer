""" NOTE: This is a quick script, I have made no attempt at error checking,
exception handling or security.  It uses straight forward SQL with argparse
added only as convienece to the user.  I could have just done this with one
command.

This script is a generic field injector that will add a missing
field to a given sqlite3 database > table.  Why? Because I am lazy and
django makemigrations, migrate fails to add a field which has been added
to a model if the database already exists with current data'
"""
import argparse
import sqlite3

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="injects missing table field into sqlite3")
    parser.add_argument('database', help='the database file e.g. db.sqlite3')
    parser.add_argument('table', help='the database table')
    parser.add_argument('field', help='field to add')
    parser.add_argument('datatype', help='the datatype definition')
    arguments = parser.parse_args()
    db_connection = sqlite3.connect(arguments.database)
    cursor = db_connection.cursor()
    sql = f"ALTER TABLE {arguments.table} ADD {arguments.field} {arguments.datatype}"
    cursor.execute(sql)
    db_connection.commit()
    db_connection.close()