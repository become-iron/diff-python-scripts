# -*- coding: utf-8 -*-
__author__ = "Alex1166, mz15, become-iron"

"""
Напишите программу, которая описывает сигнал треугольной формы, то есть генерирует массив целых чисел, которые будут
являться ординатами некоторой функции, задающей нарастание значения до заданного максимума и уменьшение этого значение
с тем же коэффициентом наклона. В качестве параметров функция должна принимать амплитуду сигнала, период сигнала
(задается через количество дискретных состояний на один период) и количество периодов. Возвращаться должен массив
целых чисел размерностью, заданной третьим аргументом.
"""

dl = 1  # длина отрезка дискретного уровня
accuracy = 2  # точность округления


def get_ordinate(amplitude, period, count_period):
    ordinate = []  # список ординат
    k = amplitude / (period / 4 * dl)  # коэффициент наклона
    ordinate += [k * dl * i for i in range(int(period / 4))]  # находим ординаты первой половины первого труегольника
    ordinate = list(map(lambda x: round(x, accuracy), ordinate))  # округление чисел
    ordinate += list(reversed(ordinate))[:-1]  # добавляем ординаты второй половины первого треугольника
    ordinate += list(map(lambda x: -x, ordinate))  # добавляем ординаты второго треугольника
    ordinate *= count_period  # добавляем все периоды
    return ordinate


def plot(ordinate):
    """
    ordinate - список с ординатами
    """
    import pylab
    abscissa = [i * dl for i in range(len(ordinate))]  # список с абсциссами
    pylab.plot(abscissa, ordinate)
    pylab.show()

if __name__ == '__main__':
    plot(get_ordinate(35, 2130, 6))
