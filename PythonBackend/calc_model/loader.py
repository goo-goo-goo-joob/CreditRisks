import base64
import io
import os

import calc_model


def get_models(path=''):
    models = {}
    for key, value in calc_model.__dict__.items():
        if isinstance(value, type) and \
                issubclass(value, calc_model.AbstractModel) and \
                value != calc_model.AbstractModel:
            models[key] = value
    result = {}
    for file in os.listdir(path):
        if not file.endswith('.cmodel'):
            continue
        name = file[:-7]
        name, klass = name.split('_')
        with open(os.path.join(path, file), 'r') as f:
            data = base64.b64decode(f.read())
        result[name] = models[klass](name, io.BytesIO(data))
    return result
