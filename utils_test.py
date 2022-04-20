from utils import plural

def test_plural():
    assert plural('game', 0) == 'games'
    assert plural('game', 1) == 'game'
    assert plural('game', 2) == 'games'
