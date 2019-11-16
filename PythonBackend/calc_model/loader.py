import base64
import io
import os

import mysql.connector as mariadb

import calc_model

mariadb_connection = mariadb.connect(host=os.getenv("DB_HOST"),
                                     port=int(os.getenv("DB_PORT")),
                                     user=os.getenv("DB_USER"),
                                     password=os.getenv("DB_PASSWORD"),
                                     database=os.getenv("DB_DATABASE"))
cursor = mariadb_connection.cursor()

if __name__ == '__main__':
    models = {}
    for key, value in calc_model.__dict__.items():
        if isinstance(value, type) and \
                issubclass(value, calc_model.AbstractModel) and \
                value != calc_model.AbstractModel:
            models[key] = value
    cursor.execute('''SELECT * FROM risks.calcModelsView''')
    for r in cursor.fetchall():
        m = models[r[2]](r[1], io.BytesIO(base64.b64decode(r[3])))
        print(m.name, m.predict_proba(None))
