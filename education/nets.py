# -*- coding: utf-8 -*-


def create_message(string: str, coding='cp1251') -> tuple:
    """
    Возвращает принятую строку в виде 16-, 2-ичных кодов в выбранной кодировке

    Принимает:
        - string (str): строка
        - coding (str): кодировка, по умолчанию 'cp1251'
    Примеры:
        >>> data = create_message('Кошкин В.И.')
        >>> print(*data[0])
        CA EE F8 EA E8 ED 20 C2 2E C8 2E
        >>> print(*data[1])
        11001010 11101110 11111000 11101010 11101000 11101101 100000 11000010 101110 11001000 101110
        >>> print(data[2])
        11 байт (88 бит)
        """
    codes = tuple(ord(sym.encode(coding)) for sym in string)
    hex_ = tuple(str(hex(code)).lstrip('0x').upper() for code in codes)
    bin_ = tuple(str(bin(code)).lstrip('0b') for code in codes)
    result = (
        hex_,
        bin_,
        '{} байт ({} бит)'.format(len(codes), len(codes) * 8)
    )
    return result
