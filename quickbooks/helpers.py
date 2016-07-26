
def qb_date_format(input_date):
    """
    Converts date to quickbooks date format
    :param input_date:
    :return:
    """
    return input_date.strftime("%Y-%m-%d")


def qb_datetime_format(input_date):
    """
    Converts datetime to quickbooks datetime format
    :param input_date:
    :return:
    """
    return input_date.strftime("%Y-%m-%dT%H:%M:%S")


def qb_datetime_utc_offset_format(input_date, utc_offset):
    """
    Converts datetime to quickbooks datetime format including UTC offset
    :param input_date:
    :param utc_offset: Formatted +/-HH:MM example: -08:00
    :return:
    """
    return "{0}{1}".format(qb_datetime_format(input_date), utc_offset)
