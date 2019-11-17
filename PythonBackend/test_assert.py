from calc_model import RandomModel


def f():
    return 0


def test_function():
    assert f() == 0


def test_random_model():
    with open('test_data/data.zip', 'rb') as f:
        m = RandomModel('Binomial random generator', f)
        for i in range(100):
            proba = m.predict_proba(None)
            assert 0 <= proba <= 1
