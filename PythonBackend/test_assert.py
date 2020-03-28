import pickle

import numpy as np
import pandas as pd


def f():
    return 0


def test_function():
    assert f() == 0


def test_model():
    with open('test_data/data.pkl', 'rb') as f:
        clf = pickle.load(f)
    for i in range(100):
        df = pd.DataFrame(np.random.random((1, len(clf.cols))), columns=clf.cols)
        proba = clf.predict_proba(df)
        assert 0 <= proba <= 1
