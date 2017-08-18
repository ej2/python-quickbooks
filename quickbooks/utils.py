import six
import sys


def build_where_clause(**kwargs):
    where_clause = ""

    if len(kwargs) > 0:
        where = []

        for key, value in kwargs.items():
            if isinstance(value, six.text_type) and sys.version_info[0] == 2:
                # If using python 2, encode unicode as string.
                encoded_value = value.encode('utf-8')
                where.append("{0} = '{1}'".format(key, encoded_value.replace(r"'", r"\'")))
            elif isinstance(value, six.string_types):
                where.append("{0} = '{1}'".format(key, value.replace(r"'", r"\'")))
            else:
                where.append("{0} = {1}".format(key, value))

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
