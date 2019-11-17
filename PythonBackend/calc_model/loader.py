import base64
import io

import mysql.connector as mariadb

import calc_model


def get_models(host='127.0.0.1', port=3306, user='', password='', database=''):
    connection = mariadb.connect(host=host, port=port, user=user, password=password, database=database)
    cursor = connection.cursor()
    models = {}
    for key, value in calc_model.__dict__.items():
        if isinstance(value, type) and \
                issubclass(value, calc_model.AbstractModel) and \
                value != calc_model.AbstractModel:
            models[key] = value
    cursor.execute('''SELECT * FROM risks.calcModelsView''')
    result = []
    for row in cursor.fetchall():
        name = row[1]
        klass = row[2]
        data = base64.b64decode(row[3])
        result.append(models[klass](name, io.BytesIO(data)))
    cursor.close()
    connection.close()
    return result
