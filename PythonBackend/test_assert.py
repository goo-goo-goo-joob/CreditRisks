from calc_model import RandomModel


def f():
    return 0


def test_function():
    assert f() == 0


def test_random_model():
    m = RandomModel('test_data/data.zip')
    for i in range(100):
        proba = m.predict_proba(None)
        assert 0 <= proba <= 1
