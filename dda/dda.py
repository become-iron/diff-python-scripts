# -*- coding: utf-8 -*-

def dda(x1, y1, x2, y2):
    x_start = _round(x1)
    y_start = _round(y1)
    x_end = _round(x2)
    y_end = _round(y2)
    L = abs(x_end - x_start) + 1 if abs(x_end - x_start) > abs(y_end - y_start) else abs(y_end - y_start) + 1

    dx = (x_end - x_start) / L  # приращение по x
    dy = (y_end - y_start) / L  # приращение по y
    x, y = x_start, y_start
    values = ((x, y),)
    for i in range(L):
        x += dx
        y += dy
        values += ((_round(x), _round(y)),)

    return values

def _round(number):
    """
    ОКРУГЛЕНИЕ ЧИСЛА В БОЛЬШУЮ СТОРОНУ
    """
    return int((number+0.5)//1)


if __name__ == '__main__':
    # выбор типа построения графика
    plot_pylab = False
    plot_pyplot = True

    # генерация начальых и конечных
    # координат линии
    from random import randint
    values = dda(randint(-10, 30),
                 randint(-10, 30),
                 randint(-10, 30),
                 randint(-10, 30))

    if plot_pylab:
        # построить неразрывный график,
        # опираясь на полученные точки
        import pylab
        pylab.plot([value[0] for value in values], [value[1] for value in values])
        pylab.show()
    elif plot_pyplot:
        import matplotlib.pyplot as plt
        import matplotlib.path as mpath
        circle = mpath.Path.unit_circle()
        plt.plot([value[0] for value in values], [value[1] for value in values], '--r', marker=circle, markersize=10)
        plt.show()
