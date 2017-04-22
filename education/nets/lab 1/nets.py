# -*- coding: utf-8 -*-


def create_message(message: str, coding) -> tuple:
    """
    Возвращает принятую строку в виде 16- и 2-ичных кодов в выбранной кодировке
    Перед формулированием сообщения у принятой строки удаляются пробелы в начале
    и в конце, а также производится перевод в верхний регистр.
    Список кодировок в Python: https://docs.python.org/3/library/codecs.html#standard-encodings
    Принимает:
        - string (str): строка
        - coding (str): кодировка
    Пример использования:
        >>> data = create_message('КОШКИН В.И.', 'cp866')
        >>> print(*data[0])
        10001010 10001110 10011000 10001010 10001000 10001101 00100000 10000010 00101110 10001000 00101110
        >>> print(*data[1])
        8A 8E 98 8A 88 8D 20 82 2E 88 2E
        >>> print(data[2])
        11 байт (88 бит)
        """
    codes = message.encode(coding)
    bytes_ = tuple(str(bin(code))[2:].zfill(8) for code in codes)
    hexes = tuple(str(hex(code))[2:].upper().zfill(2) for code in codes)
    return (
        bytes_,
        hexes,
        '{0} байт ({1} бит)'.format(len(codes), len(codes) * 8)
    )


def logic_coding(message: str, coding):
    codes = {
        '0000': '11110',
        '0001': '01001',
        '0010': '10100',
        '0011': '10101',
        '0100': '01010',
        '0101': '01011',
        '0110': '01110',
        '0111': '01111',
        '1000': '10010',
        '1001': '10011',
        '1010': '10110',
        '1011': '10111',
        '1100': '11010',
        '1101': '11011',
        '1110': '11100',
        '1111': '11101',
    }
    bytes_ = tuple(map(lambda x: bin(x)[2:].zfill(8), message.encode(coding)))
    bytes_coded = tuple(codes[byte[0:4]] + codes[byte[4:8]] for byte in bytes_)
    bits_amount = len(bytes_coded) * 10  # количество бит
    mess_len = '{0} байт ({1} бит)'.format(bits_amount / 8, bits_amount)
    _ = ''.join(bytes_coded)
    hexes = tuple(hex(int(_[i:i+20], base=2))[2:].upper() for i in range(0, len(_), 20))
    return (
        bytes_coded,
        tuple(map(lambda x: hex(int(x, base=2))[2:].upper(), bytes_coded)),  # TODO неправильное преобразование
        hexes,  # 16х-коды из 20к битов
        mess_len,
    )


# noinspection PyPep8Naming
def scrambling(message: str, coding, k1=3, k2=5):
    """Скремблирование"""
    # B_i = A_i ⊕ B_(i-k1) ⊕ B_(i-k2)
    A = tuple(map(int, ''.join(map(lambda x: bin(x)[2:].zfill(8), message.encode(coding)))))
    B = []
    for i in range(len(A)):
        o1 = A[i]
        o2 = B[i-k1] if i - k1 >= 0 else 0
        o3 = B[i-k2] if i - k2 >= 0 else 0
        B.append(o1 ^ o2 ^ o3)
    B = list(map(str, B))
    bins = [''.join(B[i: i + 8]) for i in range(0, len(B), 8)]
    return (
        bins,
        tuple(map(lambda x: hex(int(x, base=2))[2:].upper().zfill(2), bins)),
    )


def plot(syms: tuple or list, hexes: tuple or list, bits: tuple or list, plot_name=None):
    """
    Выводит графики для физических кодирований NRZ, RZ, M-II
    Принимает:
        - plot_name
        - syms: список символов
        - hexes: список 16-ричных кодов
        - bits: список 2-ичных кодов (int)
    """
    # TODO
    import numpy as np
    import matplotlib.pyplot as plt

    plots_counter = 0

    def shift_y(ys, k):
        """Смещение графика по y"""
        dy = 1.5  # расстояние между графиками
        return [y + k * dy for y in ys]

    # название графика
    if plot_name:
        fig = plt.figure()
        fig.suptitle(plot_name, fontsize=10)

    # сетка, оси
    for p in range(len(bits)):
        plt.axvline(p, color='.5', linewidth=0.5, ymax=0.92)
    for p in range(len(bits) // 8 + 1):
        plt.axvline(p * 8, color='.5', linewidth=1.2)
    for p in [0.5, -1, -2.5]:
        plt.axhline(p, color='.5', linewidth=0.5)

    # надписи битов
    for tbit, bit in enumerate(syms):
        plt.text(3.7+tbit*8, 1.6, bit)
    for tbit, bit in enumerate(hexes):
        plt.text(3.6+tbit*8, 1.4, bit)
    for tbit, bit in enumerate(bits):
        plt.text(tbit+0.3, 1.2, str(bit))

    # NRZ
    nrz = (np.arange(0, len(bits), 1), bits)
    plt.step(*nrz, label='NRZ', where='post', linewidth=2)
    plots_counter += 1

    # RZ
    bits_ = []
    for bit in bits:
        bits_.append(bit)
        bits_.append(0.5)
    rz = (np.arange(0, len(bits), 0.5), shift_y(bits_, -plots_counter))
    plt.step(*rz, label='RZ', where='post', linewidth=2)
    plots_counter += 1

    # M-II
    bits_ = []
    for bit in bits:
        if bit == 0:
            bits_.append(0)
            bits_.append(1)
        else:
            bits_.append(1)
            bits_.append(0)
    manch = (np.arange(0, len(bits), 0.5), shift_y(bits_, -plots_counter))
    plt.step(*manch, label='M-II', where='post', linewidth=2)

    plt.ylim([-3.2, 1.8])  # ограничение графика по y
    plt.gca().axis('off')  # убрать подписи осей

    # легенда
    plt.legend(bbox_to_anchor=(0.28, 1.02, 0.45, .102), loc=3, ncol=3, mode="expand", borderaxespad=0.)

    # сохранение изображение в файл
    if plot_name:
       plt.savefig('{}.png'.format(plot_name.replace(r'/', '')))
    plt.show()


def magic(message: str, coding='cp1251', k1=3, k2=5):
    """Делает магию"""
    # k1, k2 - коэф-ты полинома для скремблирования
    limit = 4  # ограничение количества байтов для построения графика

    message = message.strip().upper()
    bytes_, hexes, mess_len = create_message(message=message, coding=coding)
    bytes_coded, hexes_coded, strange_hexes_coded, mess_coded_len = logic_coding(message=message, coding=coding)
    bytes_scr, hexes_scr = scrambling(message=message, coding=coding, k1=k1, k2=k2)

    print('КОДИРОВАНИЕ ({0})'.format(coding))
    print('Исходная строка:\n', message)
    print('Двоичное представление:\n', *bytes_)
    print('Шестнадцатиричное представление:\n', *hexes)
    print('Длина исходного сообщения:\n', mess_len)
    print('-' * 50)

    print('ЛОГИЧЕСКОЕ КОДИРОВАНИЕ 4B/5B')
    print('Двоичное представление:\n', *bytes_coded)
    print('Шестнадцатиричное представление:\n', *strange_hexes_coded)
    print('Длина сообщения:\n', mess_coded_len)
    print('-' * 50)

    print('СКРЕМБЛИРОВАНИЕ ({0}, {1})'.format(k1, k2))
    print('Двоичное представление:\n', *bytes_scr)
    print('Шестнадцатиричное представление:\n', *hexes_scr)

    plot(list(message)[:limit], hexes[:limit], list(map(int, ''.join(bytes_)))[:limit * 8],
         'КОДИРОВАНИЕ')
    plot(list(message)[:limit], hexes_coded[:limit], list(map(int, ''.join(bytes_coded)))[:limit * 8],
         'ЛОГИЧЕСКОЕ КОДИРОВАНИЕ 4B/5B')
    plot(list(message)[:limit], hexes_scr[:limit], list(map(int, ''.join(bytes_scr)))[:limit * 8],
         'СКРЕМБЛИРОВАНИЕ ({0}, {1})'.format(k1, k2))


if __name__ == '__main__':
    magic('ФАМИЛИЯ И.О.', 'cp866', 3, 5)
