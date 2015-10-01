__author__ = 'm'


def rewrite_attributes(self, attribute_names, variables, skip_none=True):
    """
    Rewrite variables specified in attributes list to the object
    :param self: object to rewrite the values to
    :param attribute_names: list of attributes names acceptable by the object
    :param variables: dictionary containing attribute values
    :param skip_none: when true, method will not copy attribute when its None
    """
    for attribute, value in variables.items():
        value = variables[attribute]

        if attribute in attribute_names:

            if skip_none and value is None:
                continue

            self.__setattr__(attribute, value)


def lazy_attributes_compare(self, other, attribute_names, skip_none=True):
    """
    Compare the other object to the self object by testing for equality
    attributes specified in attributes_names list
    :param self: left object to compare
    :param other: right object to compare
    :param attribute_names: list of significant attributes names
    :param skip_none: skip comparison of attributes that value is None in any of
                      the objects
    :return: True if no significant difference has been found, otherwise False
    """
    for attribute in attribute_names:
        self_attribute = self.__getattribute__(attribute)
        other_attribute = other.__getattribute__(attribute)
        if skip_none and (self_attribute is None or other_attribute is None):
            continue
        if self_attribute != other_attribute:
            return False

    return True
