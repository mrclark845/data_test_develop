import requests
import xmltodict
from collections import OrderedDict
import csv


class Xml:
    '''
    Basic class to store XML data for conversion to CSV

    '''
    def __init__(self, xml_path):
        self.xml = requests.get(xml_path)
        self.xml_content = xmltodict.parse(self.xml.content)


def unpack_listing(listing):
    '''Unpack nested OrderedDict key and value pairs to a single list of tuples

    TODO account for outer keys, converting to dict can lead to data loss with duplicate key values

    :param listing: Nested OrderedDict result from xmltodict parsing
    :return: list of tuples
    '''

    unpacked_listing = []
    for key, val in dict(listing).iteritems():
        # print key, val, isinstance(val, OrderedDict)
        if isinstance(val, (OrderedDict, dict)):
            data = unpack_listing(val)
            unpacked_listing.extend(data)
        else:
            unpacked_listing.append((key, val))
    return unpacked_listing


def format_csv_listing(unpacked_listing, required_columns):
    '''Accept list of tuples from unpack_listing and format for writing to csv. Use required_columns to control
    outputted keys, basic mapping of row alias to desired row name.

    :param unpacked_listing: list of tuples ex from unpack_listing
    :param required_columns: dict of column names and aliases to include in output. key = col, value = alias
    :return: dict with required columns, formatted values
    '''
    formatted_csv_dict = {}
    keys = unpacked_listing.keys()
    for column, alias in required_columns.iteritems():
        if column in keys:
                formatted_csv_dict[column] = format_listing_value(unpacked_listing[column])
        elif alias in keys:
            formatted_csv_dict[column] = format_listing_value(unpacked_listing[alias])
        else:
            formatted_csv_dict[column] = ''
    return formatted_csv_dict


def format_listing_value(value):
    '''Return formatted values for format_csv_listing. Join list values to string, set None type to blank

    :param value: list, string, numeric or None
    :return: string or numeric
    '''
    if isinstance(value, list):
        return_value = ', '.join(str(item) for item in value if item)
    elif not value:
        return_value = ''
    else:
        return_value = value
    return return_value


def write_to_csv(data, file_path, required_fields):
    '''Write a list of dictionaries to csv

    :param data: list of dictionaries containing row data
    :param file_path: target file
    :param required_fields: required fields used to create data
    :return: none
    '''
    with open(file_path, mode='w') as csv_file:
        fieldnames = required_fields.keys()
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames, quotechar='"')
        writer.writeheader()
        for row_dict in data:
            writer.writerow(row_dict)
