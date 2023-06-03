from api.database import get_cursor
from models.Success import Success
import logging

def set_item(key: str, value: str):
    cursor = get_cursor()
    set_setting_sql = '''
        UPDATE settings SET v = ? WHERE k = ?
    '''
    cursor.execute(set_setting_sql, (value, key))
    cursor.connection.commit()
    cursor.connection.close()
    return Success(success=True)

def get_settings():
    logging.warn("WTF IS GOIN ON")
    
    cursor = get_cursor()
    get_settings_sql = '''SELECT k, v FROM settings WHERE 1'''

    print("Executing")
    cursor.execute(get_settings_sql)
    settings = {}

    result = cursor.fetchall()

    for row in result:
        settings[row["k"]] = row["v"]

    cursor.connection.close()

    return settings