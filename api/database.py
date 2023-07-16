import sqlite3

def get_cursor():
    con = sqlite3.connect('measurement.db')
    con.row_factory = lambda c, r: dict([(col[0], r[idx]) for idx, col in enumerate(c.description)])

    cursor = con.cursor()

    return cursor