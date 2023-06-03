from api.database import get_cursor
from datetime import datetime

from typing import List, Dict
from models.TemperaturesList import TemperaturesList
from models.TemperatureModel import TemperatureModel
from models.TemperaturePostModel import TemperaturePostModel
from models.Success import Success

def post_temperature(request: TemperaturePostModel):
    cursor = get_cursor()
    current_ts = datetime.now()

    insert_temperature_sql = '''
        INSERT INTO temperatures (pseudo_table_id, temperature, thermometer_id, ts)
        VALUES (?, ?, ?, ?)
    '''
    for temperature in request.temperatures:
        args = (request.pseudo_table_id, temperature.value, temperature.thermometer_id, current_ts)
        cursor.execute(insert_temperature_sql, args)
    
    cursor.connection.commit()
    cursor.connection.close()

    return Success(success=True)

def remove_pseudo_table(pseudo_table_id: str):
    cursor = get_cursor()
    remove_pseudo_table_sql = '''
    DELETE FROM temperatures WHERE pseudo_table_id = ?
    '''
    cursor.execute(remove_pseudo_table_sql, (pseudo_table_id,))
    cursor.connection.commit()
    cursor.connection.close()

    return Success(success=True) 

def get_temperatures(pseudo_table_id: str):
    cursor = get_cursor()
    select_times_indexes_sql = '''
        SELECT pseudo_table_id, ts FROM temperatures WHERE pseudo_table_id = ? GROUP BY ts
    '''
    cursor.execute(select_times_indexes_sql, (pseudo_table_id,))
    times_indexes: List[str] = map(lambda row: row["ts"], cursor.fetchall())

    result = TemperaturesList()
    result.temps = {}

    for time in times_indexes:
        print(time)
        select_temps_sql = '''
            SELECT temperature, thermometer_id FROM temperatures WHERE pseudo_table_id = ? AND ts = ?
        '''
        args = (pseudo_table_id, time)
        key = time.replace(" ", "T")

        cursor.execute(select_temps_sql, args)
        result.temps[key] = list()

        temps: List[dict] = cursor.fetchall()

        for temp in temps:
            result.temps[key].append(TemperatureModel(thermometer_id=temp["thermometer_id"], value=temp["temperature"]))
        
    cursor.connection.close()
    return result

def get_pseudo_tables():
    cursor = get_cursor()
    get_pseudo_tables_sql = '''
        SELECT pseudo_table_id FROM temperatures WHERE 1 GROUP BY pseudo_table_id
    '''
    cursor.execute(get_pseudo_tables_sql)
    l = list()
    for r in cursor.fetchall():
        l.append(r["pseudo_table_id"])
        
    cursor.connection.close()
    return l