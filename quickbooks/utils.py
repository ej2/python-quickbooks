import six
import sys


def build_where_clause(**kwargs):
    where_clause = ""
    operator_mappings = {
        'gt': '>',
        'gte': '>=',
        'lt': '<',
        'lte': '<=',
        'in': 'IN',
        'like': 'LIKE',
    }

    if len(kwargs) > 0:
        where = []

        for key, value in kwargs.items():
            parts = key.split('__')
            if len(parts) == 2:
                field = parts[0]
                operator = operator_mappings[parts[1]]
            else:
                field = key
                operator = '='

            if operator == 'IN':
                # Convert iterable to string of quoted values in parenthesis
                # [1, 2, 3] -> "('1', '2', '3')"
                escaped_values = [str(v).replace(r"'", r"\'") for v in value]
                value = "({0})".format(', '.join("'{0}'".format(v) for v in escaped_values))
                where.append("{0} {1} {2}".format(field, operator, value))
            elif isinstance(value, six.text_type) and sys.version_info[0] == 2:
                # If using python 2, encode unicode as string.
                encoded_value = value.encode('utf-8')
                where.append("{0} {1} '{2}'".format(field, operator, encoded_value.replace(r"'", r"\'")))
            elif isinstance(value, six.string_types):
                where.append("{0} {1} '{2}'".format(field, operator, value.replace(r"'", r"\'")))
            else:
                where.append("{0} {1} {2}".format(field, operator, value))

        where_clause = " AND ".join(where)

    return where_clause


def build_choose_clause(choices, field):
    where_clause = ""

    if len(choices) > 0:
        where = []

        for choice in choices:
            if isinstance(choice, six.text_type) and sys.version_info[0] == 2:
                # If using python 2, encode unicode as string.
                encoded_choice = choice.encode('utf-8')
                where.append("'{0}'".format(encoded_choice.replace(r"'", r"\'")))
            elif isinstance(choice, six.string_types):
                where.append("'{0}'".format(choice.replace(r"'", r"\'")))
            else:
                where.append("{0}".format(choice))

        where_clause = ", ".join(where)
        where_clause = "{0} in ({1})".format(field, where_clause)

    return where_clause
