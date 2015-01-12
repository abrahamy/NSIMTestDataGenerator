# Module:  config.py
# Author:  Abraham Yusuf <yabraham@swglobal.com>
# Created: Jan 9, 2015


class InvalidTestCaseException(Exception):
    pass


class NameConfig(object):
    valid_test_cases = [
        'TEST_MAIDEN_NAME_BLANK',
        'TEST_MAIDEN_NAME_MIXED',
        'TEST_MAIDEN_NAME_ONE',
        'TEST_MAIDEN_NAME_NUMBER',
        'TEST_SURNAME_BLANK',
        'TEST_SURNAME_MIXED',
        'TEST_SURNAME_ONE',
        'TEST_SURNAME_NUMBER',
        'TEST_FIRST_NAME_BLANK',
        'TEST_FIRST_NAME_MIXED',
        'TEST_FIRST_NAME_ONE',
        'TEST_FIRST_NAME_NUMBER',
    ]

    def __init__(self, test_case):
        xpath = {
            'first': 'FirstName',
            'maiden': 'MotherMaidenName',
            'surname': 'Surname'
        }

        if test_case not in self.valid_test_cases:
            raise InvalidTestCaseException()

        self.file_count = 100
        self.type_ = test_case.split('_')[-1].lower()
        self.search = xpath[test_case.split('_')[1].lower()]


class CountConfig(object):
    valid_test_cases = [
        'TEST_MOBILE_COUNT_FIVE',
        'TEST_MOBILE_COUNT_TEN',
        'TEST_MOBILE_COUNT_TWENTY',
        'TEST_MOBILE_COUNT_FIFTY',
        'TEST_MOBILE_COUNT_HUNDRED',
    ]

    def __init__(self, test_case):
        if test_case not in self.valid_test_cases:
            raise InvalidTestCaseException()

        mobile_number_counts = {
            'FIVE': 5, 'TEN': 10, 'TWENTY': 20, 'FIFTY': 50, 'HUNDRED': 100
        }

        self.file_count = 200
        self.add_count = mobile_number_counts[test_case.split('_')[-1]]


class NumberConfig(object):
    valid_test_cases = [
        'TEST_VFC_PRESENT',
        'TEST_VFC_PREVIOUS',
        'TEST_ZMT_PRESENT',
        'TEST_MGT_PRESENT',
        'TEST_MGT_PREVIOUS',
        'TEST_GLO_OLD',
        'TEST_GLO_NEW',
        'TEST_MTN_OLD',
        'TEST_MTN_NEW',
        'TEST_STC_PRESENT',
        'TEST_STC_PREVIOUS',
        'TEST_ANG_NEW',
        'TEST_ETS_NEW'
    ]

    def __init__(self, test_case):
        test_conf = {
            'TEST_VFC_PRESENT': (704, 0, 6999999),
            'TEST_VFC_PREVIOUS': (704, 7000000, 9999999),
            'TEST_ZMT_PRESENT': (707, 0, 9999999),
            'TEST_MGT_PRESENT': (801, 0, 1999999),
            'TEST_MGT_PREVIOUS': (801, 2000000, 9999999),
            'TEST_GLO_OLD': (811, 0, 9999999),
            'TEST_GLO_NEW': (905, 0, 9999999),
            'TEST_MTN_OLD': (814, 0, 9999999),
            'TEST_MTN_NEW': (903, 0, 9999999),
            'TEST_STC_PRESENT': (819, 0, 1999999),
            'TEST_STC_PREVIOUS': (819, 2000000, 9999999),
            'TEST_ANG_NEW': (902, 0, 9999999),
            'TEST_ETS_NEW': (909, 0, 9999999)
        }

        if test_case not in self.valid_test_cases:
            raise InvalidTestCaseException()

        self.search_path = './/NigeriaSIMDemographics/MainMobileNumber'
        if test_case.split('_')[1].lower() in ['ang', 'ets', 'zmt']:
            self.file_count = 1000
        else:
            self.file_count = 500

        self.prefix, self.range_start, self.range_stop = test_conf[test_case]


class DateConfig(object):
    valid_test_cases = [
        'TEST_DOB_HUNDRED',
        'TEST_DOB_TWO_HUNDRED'
    ]

    def __init__(self, test_case):
        if test_case not in self.valid_test_cases:
            raise InvalidTestCaseException()

        self.file_count = 100
        lesser = test_case == self.valid_test_cases[0]
        self.range_start = 1915 if lesser else 1815
        self.range_stop = 2000 if lesser else 1915


def get_config(test_case):
    if test_case in NameConfig.valid_test_cases:
        return NameConfig(test_case)
    elif test_case in CountConfig.valid_test_cases:
        return CountConfig(test_case)
    elif test_case in NumberConfig.valid_test_cases:
        return NumberConfig(test_case)
    elif test_case in DateConfig.valid_test_cases:
        return DateConfig(test_case)
    else:
        raise InvalidTestCaseException()


def get_test_cases():
    test_cases = []

    for class_ in [CountConfig, DateConfig, NameConfig, NumberConfig]:
        test_cases.extend(class_.valid_test_cases)

    return test_cases


def get_file_count():
    return reduce(
        lambda sum_, item: sum_ + item.file_count,
        [get_config(tc) for tc in get_test_cases()], 0
    )
