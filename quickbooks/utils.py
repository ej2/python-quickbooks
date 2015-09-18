import six


def build_where_clause(**kwargs):
    where_clause = ""

    if len(kwargs) > 0:
        where = []

        for key, value in kwargs.items():
            if isinstance(value, six.string_types):
                where.append("{0} = '{1}'".format(key, value.replace("'", "\'")))
            else:
                where.append("{0} = {1}".format(key, value))

        where_clause = " AND ".join(where)

    return where_clause
