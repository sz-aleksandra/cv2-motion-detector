from office_schedule import read_hours, get_hours, get_closed_days


def test_get_closed_days():
    days = get_closed_days()
    for day in days:
        assert day in [0, 1, 2, 3, 4, 5, 6]


def test_read_hours():
    a, b, c = read_hours()
    assert a != 1.5
    assert b != 2.5
    assert c != 3.5


def test_get_hours(monkeypatch):
    def fake_hours():
        return (7, 17, 23)
    monkeypatch.setattr("office_schedule.read_hours", fake_hours)
    hours = get_hours(0)
    assert hours == [23, 0, 1, 2, 3, 4, 5, 6]
    hours = get_hours(1)
    assert hours == [7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
    hours = get_hours(2)
    assert hours == [17, 18, 19, 20, 21, 22]
