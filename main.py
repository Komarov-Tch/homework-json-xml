import json
import os
import xml.etree.ElementTree as ET

from pprint import pprint

file_adress = os.path.join(os.getcwd(), 'formats.json.xml')
JSON_FINE_NAME = 'newsafr.json'
XML_FILE_NAME = 'newsafr.xml'


def json_open(adress: 'file adress json') -> list:
    with open(adress, 'r', encoding='utf-8') as f:
        data = json.load(f)
        result = []
        for text in data['rss']['channel']['items']:
            result.extend(word_filter(text['description']))
    words = {}
    for i in result:
        words[i] = words.get(i, 0) + 1
    result = list(map(lambda w: w[0], sorted(list(words.items()), key=lambda x: -x[1])))
    return result[:10]


def xml_open(adress: 'file adress xml') -> list:
    parser = ET.XMLParser(encoding='utf-8')
    tree = ET.parse(adress, parser)
    root = tree.getroot()
    xml_items = root.findall('channel/item')
    result = []
    for xmli in xml_items:
        result.extend(word_filter(xmli.find('description').text))
    words = {}
    for i in result:
        words[i] = words.get(i, 0) + 1
    result = list(map(lambda w: w[0], sorted(list(words.items()), key=lambda x: -x[1])))
    return result[:10]
    return result


def word_filter(text):
    english_alphabet = set([chr(c) for c in range(ord('a'), ord('z') + 1)])
    russian_alphabet = set([chr(c) for c in range(ord('а'), ord('я') + 1)]
                           + ['ё'])
    alphabet = english_alphabet ^ russian_alphabet
    text = ''.join(filter(lambda c: c in alphabet ^ {' '}, text.lower()))
    return filter(lambda word: len(word) > 6, text.split())


print(json_open(os.path.join(file_adress, JSON_FINE_NAME)))
print(xml_open(os.path.join(file_adress, XML_FILE_NAME)))
