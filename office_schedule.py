def get_closed_days() -> list[int]:
    """
    Pobiera dane z pliku txt i zwraca listę dni, w których biuro
    jest zamknięte. 0 to poniedziałek, 6 to niedziela.
    """
    closed_days = []
    with open("dni_zamkniete.txt", "r") as file:
        file.readline()
        days = file.readline().strip().lower().split(", ")
        if "poniedziałek" in days:
            closed_days.append(0)
        if "poniedzialek" in days:
            closed_days.append(0)
        if "wtorek" in days:
            closed_days.append(1)
        if "środa" in days:
            closed_days.append(2)
        if "sroda" in days:
            closed_days.append(2)
        if "czwartek" in days:
            closed_days.append(3)
        if "piątek" in days:
            closed_days.append(4)
        if "piatek" in days:
            closed_days.append(4)
        if "sobota" in days:
            closed_days.append(5)
        if "niedziela" in days:
            closed_days.append(6)
    return closed_days


def read_hours() -> tuple[int, int, int]:
    """
    Wczytuje z pliku i zwraca w krotce godziny rozpoczęcia
    intensywnego/zmniejszonego użytkowania biura oraz godziny jego zamknięcia.
    """
    with open("godziny.txt", "r") as file:
        file.readline()
        intensive = int(file.readline().strip())
        file.readline()
        limited = int(file.readline().strip())
        file.readline()
        closed = int(file.readline().strip())
    return (intensive, limited, closed)


def get_hours(period: int) -> list[int]:
    """
    Zwraca listę godzin intensywnego/zmniejszonego użytkowania/zamknięcia biura
    w zależności od przekazanej wartości (zamknięte: 0, intensywne: 1,
    zmniejszone: 2).
    """
    hours = []
    intensive, limited, closed = read_hours()
    if period == 0:
        start = closed
        stop = intensive
    elif period == 1:
        start = intensive
        stop = limited
    else:
        start = limited
        stop = closed
    if start < stop:
        # godziny nie przechodzą przez północ
        hours += [hour for hour in range(start, stop)]
    else:
        # godziny przechodzą przez północ
        hours += [hour for hour in range(start, 24)]
        hours += [hour for hour in range(0, stop)]
    return hours
