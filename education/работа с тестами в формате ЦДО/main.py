# -*- coding: utf-8 -*-

# Работа с тестами в формате ЦДО


import xml.etree.ElementTree as ET
from collections import OrderedDict


def parse_test(file: str):
    """
    Преобразует ЦДО-теста из формата в XML в dict
    :param file: путь к файлу с тестом
    """
    result = OrderedDict()
    root = ET.parse(file).getroot()

    for frame in root:
        task = frame[0]
        question = task[0].text
        variants = {variant[0].text: variant.attrib.get('Value', False)
                    for variant in task[1]}
        result.update({question: variants})
    return result


def pprint_test(test):
    """
    Красивый вывод теста
    :param test: dict с тестом
    """
    for question in test:
        print(question)
        for variant in test[question]:
            print('+' if test[question][variant] else '-',
                  variant)
        print()

if __name__ == '__main__':
    pprint_test(parse_test('./datasets/TestFrames4.xml'))
