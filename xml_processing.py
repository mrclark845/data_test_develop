from xml_utilities import Xml, unpack_listing, format_csv_listing, write_to_csv
import datetime
import os

test_xml = Xml('http://syndication.enterprise.websiteidx.com/feeds/BoojCodeTest.xml')

csv_path = os.path.join(os.path.expanduser('~'), 'desktop/listings.csv')

required_columns = {
    'MlsId': 'MlsId'
    , 'MlsName': 'MlsName'
    , 'DateListed': 'DateListed'
    , 'StreetAddress': 'StreetAddress'
    , 'Price': 'Price'
    , 'Bedrooms': 'Bedrooms'
    , 'Bathrooms': 'Bathrooms'
    , 'Appliances': 'Appliance'
    , 'Rooms': 'Room'
    , 'Description': 'Description'
    #, 'FullBathrooms': 'FullBathrooms'
    }

data = []

for listing in test_xml.xml_content['Listings']['Listing']:
    unpacked_listing = dict(unpack_listing(listing))
    formatted_listing = format_csv_listing(unpacked_listing, required_columns)
    if (datetime.datetime.strptime(unpacked_listing['DateListed'], '%Y-%m-%d %H:%M:%S').year == 2016
            and 'and' in unpacked_listing['Description']):
        formatted_listing['Description'] = formatted_listing['Description'][:200]
        data.append(formatted_listing)

data = sorted(data, key=lambda k: k['DateListed'])

write_to_csv(data, csv_path, required_columns)
