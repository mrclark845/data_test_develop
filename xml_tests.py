from xml_utilities import unpack_listing, format_csv_listing, format_listing_value


def test_unpack_listing():
    test_dict = {'outer': {'inner1': 'inner1 value', 'inner2': 'inner2 value'}}
    unpacked_dict = dict(unpack_listing(test_dict))
    assert unpacked_dict.keys().sort() == ['inner2', 'inner1'].sort()
    assert unpacked_dict['inner1'] == 'inner1 value'


def test_format_csv_listing():
    required_cols = {
        'One': 'Uno'
        , 'Two': 'Dos'
        , 'Three': 'Tres'
        }

    data = {'One': 1
            , 'Dos': 2.00
            , 'Tres': ['Three', 'Tres', 'Trois']
            , 'Miercoles': 'Wednesday'}

    formatted_csv_row = format_csv_listing(data, required_cols)

    assert formatted_csv_row == {
                                'One': 1
                                , 'Two': 2.00
                                , 'Three': 'Three, Tres, Trois'
                                }


def test_format_listing_value():
    test_array = format_listing_value([1, None, 2, 3, 5, None])
    test_none = format_listing_value(None)
    test_string = format_listing_value('test value')

    assert test_array == '1, 2, 3, 5'
    assert test_none == ''
    assert test_string == 'test value'


test_format_listing_value()

test_unpack_listing()

test_format_csv_listing()