import os
import pickle


def get_models(path=''):
    result = {}
    for file in os.listdir(path):
        if not file.endswith('.pkl'):
            continue
        with open(os.path.join(path, file), 'rb') as f:
            clf = pickle.load(f)
        name = file[:-4]
        result[name] = clf
    return result
